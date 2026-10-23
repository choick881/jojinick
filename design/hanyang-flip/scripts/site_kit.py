"""상세페이지·홈페이지 공통 재료: 확정 로고, 문구(콘텐츠), 아이콘, 이미지 자리표시.

확정 로고 체계 (로고 2차 선택)
  - seal : D 인장 속 모노그램 → 공문·명판·푸터
  - mark : A 모노그램 Regular → 웹 헤더·영상
  - tile : E 페이지 타일     → SNS·앱 아이콘
문구의 수치·후기·연락처는 모두 예시입니다 (※ 표기).
"""

from build_logos_r2 import NEW, a_mark

_n = [0]


def _uid(p):
    _n[0] += 1
    return f"{p}{_n[0]}"


def logo(kind, size=40, cls=""):
    fn = {"seal": NEW["D"]["svg"], "tile": NEW["E"]["svg"], "mark": lambda uid: a_mark()}[kind]
    return (f'<svg class="logo-{kind} {cls}" viewBox="0 0 120 120" width="{size}" height="{size}" '
            f'aria-hidden="true">{fn(_uid(kind))}</svg>')


def emblem_ph(cls=""):
    return f'<span class="emblem-ph {cls}" title="실제 교표는 공식 파일로 교체">UNIVERSITY<br>EMBLEM</span>'


def img(name, cls="", ratio=None, label=None):
    """GPT 이미지 자리. assets/<name>.png 가 있으면 자동으로 표시, 없으면 그라디언트 + 라벨."""
    st = f' style="aspect-ratio:{ratio}"' if ratio else ""
    lab = label or name
    return f'<div class="ph {cls}" data-img="../assets/{name}.png" data-label="GPT 실사 · {lab}"{st}></div>'


IMG_JS = """<script>
document.querySelectorAll('[data-img]').forEach(function (el) {
  var i = new Image();
  i.onload = function () { el.style.backgroundImage = 'url(' + i.src + ')'; el.classList.add('has-img'); };
  i.src = el.dataset.img;
});
</script>"""

PH_CSS = """
:root{--mark:#0E4A84;--accent:#C8A24A;--knock:#fff}
.ph{position:relative;background:linear-gradient(135deg,#123d6b 0%,#0e4a84 45%,#2f6aa3 100%);background-size:cover;background-position:center;overflow:hidden}
.ph::before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 70% 30%,rgba(255,255,255,.16),transparent 55%),
  repeating-linear-gradient(135deg,rgba(255,255,255,.035) 0 14px,transparent 14px 28px)}
.ph::after{content:attr(data-label);position:absolute;left:12px;bottom:10px;font:500 11px/1.4 'Noto Sans KR',sans-serif;color:rgba(255,255,255,.75);
  letter-spacing:.04em;background:rgba(0,0,0,.18);padding:2px 8px;border-radius:2px}
.ph.has-img::before,.ph.has-img::after{display:none}
.emblem-ph{display:inline-flex;align-items:center;justify-content:center;text-align:center;border:1px dashed currentColor;opacity:.6;
  font:700 8px/1.15 'Noto Sans KR',sans-serif;letter-spacing:.08em;width:56px;height:36px;border-radius:2px}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800;900'
         '&family=Noto+Serif+KR:wght@500;700;900&display=swap" rel="stylesheet">')


def head(title, css, lang="ko"):
    return (f'<!doctype html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>{title}</title>\n'
            f'{FONTS}\n<style>{PH_CSS}{css}</style>\n</head>\n')


# ── 아이콘 (선, currentColor) ─────────────────────────────────────────
_IC = {
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "cc": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M10.5 10.2a2.2 2.2 0 1 0 0 3.6M17 10.2a2.2 2.2 0 1 0 0 3.6"/>',
    "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21"/>',
    "doc": '<path d="M7 3h7l4 4v14H7zM14 3v4h4M10 12h5M10 16h5"/>',
    "chapters": '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="5" cy="6" r="1.2"/><circle cx="5" cy="12" r="1.2"/><circle cx="5" cy="18" r="1.2"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "down": '<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "camera": '<rect x="3" y="7" width="13" height="10" rx="1.5"/><path d="M16 10.5l5-3v9l-5-3z"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="1.5"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "book": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5zM4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>',
    "help": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .9-1 1.7M12 17h.01"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
}


def icon(name, size=24, cls=""):
    return (f'<svg class="ic {cls}" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_IC[name]}</svg>')


PLAY = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M8 5.5v13l10.5-6.5z"/></svg>'

# ── 콘텐츠 (모든 시안 공통) ───────────────────────────────────────────
C = {
    "eyebrow": "2026 한양 플립러닝 콘텐츠 개발 사업",
    "h1": ["강의실 밖에서", "시작되는 수업"],
    "sub": "교수님은 강의만 하세요. 기획 · 촬영 · 편집 · AI 자막까지 HY FLIP 이 함께합니다.",
    "cta1": "제작 신청하기",
    "cta2": "사업 안내서 받기",
    "facts": [("모집 기간", "2026. 11. 01 – 11. 30"), ("지원 대상", "학부 전공·교양 담당 교수"), ("지원 내용", "기획·촬영·편집 전액 지원")],
    "nav": ["사업소개", "제작절차", "스튜디오", "AI 활용", "제작사례", "FAQ"],
    "flip": {
        "title": "플립러닝이란?",
        "lead": "설명은 영상으로 먼저, 강의실에서는 토론과 실습을. 수업의 순서를 '뒤집어' 배움의 깊이를 바꾸는 방식입니다.",
        "rows": [("수업 전", "예습 없음 · 교재 읽기", "짧은 강의 영상으로 개념 학습"),
                 ("수업 중", "교수 설명 듣기 (일방향)", "토론 · 실습 · 문제 해결 (양방향)"),
                 ("수업 후", "혼자 과제 해결", "심화 학습 · 피드백 반영")],
    },
    "who": [("영상 촬영이 처음이라 막막한 교수님", "카메라 앞에 서는 법부터 함께 준비합니다."),
            ("토론·실습 중심으로 수업을 바꾸고 싶은 교수님", "교수설계 전문가가 수업 흐름을 같이 설계합니다."),
            ("기존 강의안을 영상 자산으로 남기고 싶은 교수님", "PPT 와 강의 노트만 있으면 시작할 수 있어요.")],
    "steps": [("01", "신청", "온라인 신청서 작성", "1일", "강의계획서"),
              ("02", "기획", "교수설계 컨설팅 · 차시 구성 · 대본 정리", "1–2주", "강의안 · PPT"),
              ("03", "촬영", "전문 스튜디오 촬영 · 프롬프터 지원", "회당 2시간", "촬영일 일정만"),
              ("04", "편집·검수", "AI 자막 · 그래픽 · 최종 검수 후 LMS 탑재", "2–3주", "검수 1회")],
    "studio": [("studio-hero", "강의 촬영 스튜디오", "방음 설계 · 프롬프터 · 3점 조명"),
               ("chroma", "크로마키 스튜디오", "가상 강의실 합성"),
               ("lightboard", "라이트보드", "판서하며 정면 촬영"),
               ("prompter", "프롬프터", "대본을 보며 자연스럽게"),
               ("camera", "4K 시네마 카메라", "선명한 화질 · 2캠 동시 촬영"),
               ("smartboard", "전자칠판", "PPT 위에 바로 필기"),
               ("editing", "편집·후반작업실", "전문 편집자 상주")],
    "ai": [("cc", "AI 자막 (한/영)", "촬영 당일 초벌 자막 생성 → 사람이 최종 교정"),
           ("mic", "AI 다국어 더빙", "교수님 목소리 톤으로 영어·중국어 버전 제작"),
           ("doc", "요약 · 퀴즈 자동 생성", "차시별 핵심 요약과 확인 퀴즈를 함께 제공"),
           ("chapters", "챕터 자동 분할", "주제가 바뀌는 지점마다 목차를 달아 복습이 쉬움")],
    "cases": [("thumb-1", "데이터로 읽는 경영학 원론", "경영대학 · 12차시"),
              ("thumb-2", "공학수학 I — 라이트보드 강의", "공과대학 · 15차시"),
              ("thumb-3", "글로벌 커뮤니케이션 영어", "국제학부 · 10차시"),
              ("thumb-4", "AI 시대의 미디어 리터러시", "교양 · 8차시")],
    "quotes": [("촬영이 처음이라 걱정했는데, 기획 단계에서 강의안을 함께 다듬어 주셔서 카메라 앞이 오히려 편했습니다.", "공과대학 김OO 교수"),
               ("설명은 영상에 맡기고 수업 시간에 토론을 하니, 학생들 질문이 눈에 띄게 늘었어요.", "경영대학 이OO 교수")],
    "stats": [("120", "강좌", "제작 강좌"), ("45", "명", "참여 교수"), ("4.7", "/5", "학습자 만족도"), ("18,000", "+", "누적 수강")],
    "faq": [("촬영은 얼마나 걸리나요?", "15분 분량 영상 1편 기준 약 2시간입니다. 프롬프터가 있어 대본을 외우지 않으셔도 됩니다."),
            ("비용이 드나요?", "사업에 선정된 교수님은 기획·촬영·편집 비용을 전액 지원받습니다. (예시)"),
            ("완성된 영상의 저작권은 누구에게 있나요?", "협약에 따라 교수님과 대학이 함께 보유하며, 교내 LMS 와 공개 강좌에 활용됩니다."),
            ("편집본을 고칠 수 있나요?", "검수 단계에서 2회까지 무상 수정이 가능합니다.")],
    "cta_h": "다음 학기, 수업을 뒤집어 보세요",
    "cta_p": "신청서 작성은 5분이면 충분합니다. 담당 PD 가 일주일 안에 연락드립니다.",
    "contact": "HY FLIP 사업단 · 02-0000-0000 · hyflip@example.ac.kr",
    "notice": "※ 본 페이지는 제안용 디자인 시안이며, 수치·후기·연락처는 예시입니다. 한양대학교 공식 교표·로고가 아닙니다.",
    "notices": [("공지", "2026학년도 2학기 플립러닝 콘텐츠 제작 교수 모집", "10.28"),
                ("안내", "스튜디오 정기 점검 일정 안내 (11/3–11/4)", "10.24"),
                ("행사", "플립러닝 수업 설계 워크숍 참가 신청", "10.17"),
                ("공지", "AI 자막·더빙 서비스 시범 운영 결과 공유", "10.10"),
                ("안내", "제작 가이드북 2026 개정판 배포", "10.02")],
    "schedule": [("11.01", "제작 신청 접수 시작"), ("11.30", "신청 마감"), ("12.10", "선정 결과 발표"),
                 ("12월–1월", "기획 컨설팅 · 촬영"), ("2월", "편집 · 검수 · LMS 탑재")],
}
