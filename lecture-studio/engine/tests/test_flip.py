"""플립러닝 프로필 단위 시험 — 영상·모델 없이 돈다.   실행: python -m pytest engine/tests  (또는 python engine/tests/test_flip.py)"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ls import pipeline, review, s4_text, s8_slides, s9_chapters, s10_trim  # noqa: E402
from ls.job import KINDS  # noqa: E402


def _frames(n=120, seed=1):
    """초당 2장 · 60초. 오른쪽 위 카메라 창은 늘 움직이고, 20초·40초에 슬라이드가 바뀐다."""
    rng = np.random.default_rng(seed)
    f = np.full((n, s8_slides.SH, s8_slides.SW), 40, np.int16)
    f[:, 5:30, 160:188] = rng.integers(0, 255, (n, 25, 28))          # 카메라 창 (계속 바뀜)
    f[40:, 30:90, 10:120] = 200                                        # 20초: 새 슬라이드
    f[60:, 95:100, 10:60] = 255                                        # 30초: 글머리 한 줄 (작은 변화)
    f[80:, :, :150] = 120                                              # 40초: 새 슬라이드
    return f


def test_slides_ignore_camera_and_find_changes():
    fr = _frames()
    live = s8_slides.live_mask(fr)
    assert live[15, 170] and not live[60, 60]                          # 카메라 창만 '늘 움직임'
    ev, motion = s8_slides.detect(fr, s8_slides.SENS["normal"], live)
    kinds = [(e["t"], e["kind"]) for e in ev]
    assert kinds == [(20.0, "slide"), (30.0, "build"), (40.0, "slide")], kinds
    assert motion == []


def test_slides_static_video_has_no_events():
    fr = _frames()[:35]                                                 # 전환 전 17초만
    ev, _ = s8_slides.detect(fr, s8_slides.SENS["normal"], s8_slides.live_mask(fr))
    assert ev == []


def test_chapter_types():
    assert s9_chapters._classify("안녕하세요 오늘은 수요와 공급을 함께 살펴봅니다", 0, 4, 0)[0] == "도입"
    assert s9_chapters._classify("예를 들어 실제로 시장에서 있었던 사례를 보면", 1, 4, 0)[0] == "사례"
    assert s9_chapters._classify("이 개념은 가격과 수량의 관계입니다", 1, 4, 0)[0] == "개념"
    assert s9_chapters._classify("코드를 실행해 보겠습니다", 2, 4, 0.6)[0] == "시연"
    assert s9_chapters._classify("정리하면 핵심은 균형 가격입니다. 다음 시간에", 3, 4, 0)[0] == "정리"


def test_text_cuts_ng_retake_filler():
    segs = [  # 실제 녹화 중 잡담(3분50초 샘플 대본) + 다시 말하기 + 군말
        {"start": 10.0, "end": 14.0, "text": "결국 좋은 교수법이란"},
        {"start": 14.5, "end": 17.0, "text": "왜 PPT를 안 넘겨? 아니야."},
        {"start": 17.5, "end": 20.0, "text": "야 미치겠다 형 아 나 내가 다 있어"},
        {"start": 30.0, "end": 33.0, "text": "수요가 늘면 가격이 오릅니다"},
        {"start": 34.0, "end": 37.0, "text": "수요가 늘면 가격이 오릅니다. 그래서"},
        {"start": 40.0, "end": 41.0, "text": "음 어"},
        {"start": 42.0, "end": 45.0, "text": "공급 곡선은 오른쪽 위로 향합니다"},
    ]
    cuts = s10_trim.text_cuts(segs)
    got = [(c["kind"], c["text"][:6]) for c in cuts]
    ng = [c for c in cuts if c["kind"] == "NG·혼잣말 의심"]
    assert len(ng) == 1 and ng[0]["text"].startswith("왜 PPT를") and "미치겠다" in ng[0]["text"]   # 이어진 잡담 = 한 덩어리
    assert ng[0]["a"] == 14.3 and ng[0]["b"] == 20.3
    assert ("다시 말하기", "수요가 늘면") in got
    assert ("군말", "음 어") in got
    assert not any(c["text"].startswith("공급 곡선") or c["text"].startswith("결국") for c in cuts)


def test_ng_block_absorbs_short_chatter_between_and_at_end():
    segs = [  # 3분50초 샘플의 실제 받아쓰기 끝부분
        {"start": 203.5, "end": 209.4, "text": "과거에 효과적이었던 교수 방법이 지금도 똑같이 효과적이라고 보기는 어렵습니다."},
        {"start": 210.3, "end": 216.7, "text": "결국 좋은 교수법이란... 왜 ppg를 안 넘겨? 아니야 다음 거에다 넘기는 거야"},
        {"start": 217.9, "end": 220.1, "text": "아 이거 다 돼있어 이거는 지금 아이"},
        {"start": 220.6, "end": 229.0, "text": "아이씨 아 나 앞까지 해 미안해 아니야 내가 지금 이거 넘기는 거 다시! 야 미치겠다 형"},
        {"start": 230.6, "end": 233.0, "text": "내가 다 있어"},
    ]
    ng = [c for c in s10_trim.text_cuts(segs) if c["kind"] == "NG·혼잣말 의심"]
    assert len(ng) == 1 and abs(ng[0]["a"] - 210.1) < 1e-6 and abs(ng[0]["b"] - 233.3) < 1e-6, ng
    # NG 앞의 강의 문장은 묶지 않는다
    short_before = [{"start": 0, "end": 2, "text": "네 좋습니다"}, {"start": 2.5, "end": 5, "text": "잠깐만 다시 할게요"}]
    ng2 = [c for c in s10_trim.text_cuts(short_before) if c["kind"] == "NG·혼잣말 의심"]
    assert len(ng2) == 1 and ng2[0]["a"] == 2.3


def test_question_regex_keeps_thinking_time():
    assert s10_trim.QUESTION.search("좋은 가르침이란 과연 무엇일까?")
    assert s10_trim.QUESTION.search("여러분은 어떻게 생각하나요")
    assert not s10_trim.QUESTION.search("가격이 오릅니다.")


def test_stale_ai_text_is_detected():
    segs = [{"text": t} for t in ["안녕하십니까", "한양대학교 교육혁신처의 이종호입니다", "먼저 바쁘신 가운데 감사드립니다",
                                  "아울러 뜻깊은 자리를 마련해 주셔서", "그 과정에서 늘 품고 있던 질문"]]
    good = {"segments": [{"id": i, "parts": [{"ko": s["text"]}]} for i, s in enumerate(segs)]}
    assert s4_text.mismatched(segs, good) == []
    shifted = {"segments": [{"id": i, "parts": [{"ko": segs[i + 1]["text"]}]} for i in range(len(segs) - 1)]}
    assert len(s4_text.mismatched(segs, shifted)) >= 3               # 한 칸씩 밀린 예전 결과 → 대부분 불일치


def test_tmap_shifts_after_cuts():
    rm = [[10.0, 13.0], [20.0, 22.0]]
    assert review.tmap(5, rm) == 5
    assert review.tmap(11, rm) is None                                  # 잘린 구간 안
    assert review.tmap(15, rm) == 12
    assert review.tmap(30, rm) == 25
    assert review._tmap_start(11, rm) == 10                             # 시작점은 잘린 구간 끝으로


def test_core_contract_kept():
    # 숏폼(①) 세션과 공유하는 코어: 기존 이름·단계 순서·시그니처 유지, 프로필은 추가만
    assert pipeline.NAMES == ["ingest", "clean", "asr", "text", "study", "outputs", "print"]
    assert pipeline.PROFILES["default"] is pipeline.STAGES
    flip = [s[0] for s in pipeline.PROFILES["flip"]]
    assert flip[:3] == ["ingest", "clean", "asr"] and flip[-2:] == ["outputs", "print"]
    assert {"major", "general", "language", "special", "event", "flip"} <= set(KINDS)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok ", name)
