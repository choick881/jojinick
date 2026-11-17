"""플립러닝 프로필 단위 시험 — 영상·모델 없이 돈다.   실행: python -m pytest engine/tests  (또는 python engine/tests/test_flip.py)"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ls import pipeline, review, s8_slides, s9_chapters, s10_trim  # noqa: E402
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
    assert ("NG·혼잣말 의심", "왜 PPT를") in got
    assert ("NG·혼잣말 의심", "야 미치겠다") in got
    assert ("다시 말하기", "수요가 늘면") in got
    assert ("군말", "음 어") in got
    assert not any(c["text"].startswith("공급 곡선") or c["text"].startswith("결국") for c in cuts)


def test_question_regex_keeps_thinking_time():
    assert s10_trim.QUESTION.search("좋은 가르침이란 과연 무엇일까?")
    assert s10_trim.QUESTION.search("여러분은 어떻게 생각하나요")
    assert not s10_trim.QUESTION.search("가격이 오릅니다.")


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
