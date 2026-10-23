"""프로젝트 허브 → design/hanyang-flip/index.html

로고·상세페이지·홈페이지·이미지 갤러리·메타 프롬프트를 한 장에서 열어 보는 목차 페이지입니다.
  python scripts/build_index.py
"""

import json
from pathlib import Path

from site_kit import head, logo

ROOT = Path(__file__).resolve().parent.parent

CSS = """
:root{--navy:#0E4A84;--deep:#0A2E55;--gold:#C8A24A;--ink:#1A2233;--muted:#5B6475;--line:#E3E6EC;--ivory:#F7F5F0;
  --serif:'Noto Serif KR',Georgia,serif;--sans:'Noto Sans KR',system-ui,sans-serif}
*{box-sizing:border-box;margin:0}
body{background:#fff;color:var(--ink);font:400 16px/1.7 var(--sans);word-break:keep-all;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.w{max-width:1200px;margin:0 auto;padding:0 40px}
.top{background:var(--deep);color:#fff;padding:72px 0 64px;--mark:#fff;--accent:var(--gold)}
.top .w{display:grid;grid-template-columns:auto 1fr;gap:32px;align-items:center}
.eyebrow{font:700 12px/1 var(--sans);letter-spacing:.2em;color:var(--gold)}
h1{font:900 44px/1.25 var(--serif);margin:14px 0 12px} .top p{color:#c9d6e8;max-width:680px}
.sum{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid var(--line)}
.sum div{padding:28px 24px 28px 0} .sum div+div{padding-left:24px;border-left:1px solid var(--line)}
.sum dt{font:700 12px/1 var(--sans);letter-spacing:.14em;color:var(--gold)}
.sum dd{font:700 18px/1.45 var(--serif);color:var(--deep);margin-top:10px} .sum dd small{display:block;font:400 13px/1.6 var(--sans);color:var(--muted);margin-top:4px}
section{padding:64px 0 8px} h2{font:900 28px/1.3 var(--serif);color:var(--deep);margin-bottom:6px}
.lead{color:var(--muted);margin-bottom:24px}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{border:1px solid var(--line);display:flex;flex-direction:column;transition:.2s;background:#fff}
.card:hover{border-color:var(--navy);transform:translateY(-2px)}
.card .shot{aspect-ratio:16/10;background:var(--ivory) center top/cover no-repeat;border-bottom:1px solid var(--line)}
.card .b{padding:16px 18px 18px} .card b{display:block;font:700 17px/1.4 var(--serif);color:var(--deep)}
.card span{font-size:13.5px;color:var(--muted)}
.tag{display:inline-block;font:700 11px/1 var(--sans);color:#fff;background:var(--navy);padding:4px 7px;border-radius:2px;margin-right:6px;vertical-align:2px}
.tag.alt{background:#fff;color:var(--muted);border:1px solid var(--line)}
.files{display:grid;grid-template-columns:repeat(2,1fr);gap:0 32px}
.files a{display:flex;justify-content:space-between;gap:12px;padding:14px 0;border-bottom:1px solid var(--line)}
.files a span{color:var(--muted);font-size:14px}
.kw{margin:64px 0 0;background:var(--ivory);padding:28px 32px;border-left:3px solid var(--gold)}
.kw b{color:var(--navy)}
footer{padding:48px 0 64px;color:var(--muted);font-size:13px}
@media (max-width:900px){.w{padding:0 20px}.top .w{grid-template-columns:1fr}h1{font-size:32px}
  .sum{grid-template-columns:1fr 1fr}.sum div,.sum div+div{padding:20px 12px 20px 0;border-left:0}
  .cards{grid-template-columns:1fr 1fr}.files{grid-template-columns:1fr}}
@media (max-width:520px){.cards{grid-template-columns:1fr}}
"""


def card(href, shot, title, desc, tag="확정"):
    cls = "tag" if tag == "확정" else "tag alt"
    style = f' style="background-image:url({shot})"' if (ROOT / shot).exists() else ""
    return (f'<a class="card" href="{href}"><div class="shot"{style}></div>'
            f'<div class="b"><b><span class="{cls}">{tag}</span>{title}</b><span>{desc}</span></div></a>')


def main():
    items = json.loads((ROOT / "assets/manifest.json").read_text(encoding="utf-8"))
    made = sum((ROOT / "assets" / it["file"]).exists() for it in items)
    photo = f"{made} / {len(items)}장 반영" if made else f"{len(items)}장 생성 완료 · 원본 받기 대기"
    finals = "".join([
        card("logo/logo-board-r2.html", "shots/logo-board-r2-desktop.png", "로고 체계",
             "D 인장(공문·명판) · A 모노그램(웹·영상) · E 타일(SNS·앱)"),
        card("detail/detail-final.html", "shots/detail-final-desktop.png", "사업 상세페이지",
             "A+C 리믹스 — 밝은 아카데믹 본문 + 시네마틱 다크 밴드"),
        card("home/home-final.html", "shots/home-final-desktop.png", "홈페이지",
             "영상 히어로 + 바로가기 + 공지·일정 카드"),
        card("home/home-en.html", "shots/home-en-desktop.png", "English Homepage (영문 홈)",
             "외국인 교수자·유학생용 — 영어·다국어 콘텐츠 개발 서비스 · KO/EN 전환"),
        card("booking/booking.html", "shots/booking-desktop.png", "스튜디오 예약 (교수용)",
             "빈 시간 선택 → AI 사전 검토 → 규칙 충족 시 자동 확정"),
        card("booking/admin.html", "shots/admin-desktop.png", "예약 관리 (담당자용)",
             "예외만 확인 — AI 사유·대안·안내문 초안 · 가동률 · 자동화 기록"),
        card("proposal/proposal.pdf", "shots/proposal-p1.png", "AI 학습조직 과제 제안서",
             "Edu-Tech AI Lab 제출용 A4 3쪽"),
    ])
    drafts = "".join([
        card("logo/logo-board.html", "shots/logo-board-desktop.png", "로고 1차 시안", "A Page Flip · B Academic Seal · C Play Flip", "시안"),
        card("detail/detail-A.html", "shots/detail-A-desktop.png", "상세 A 클래식", "명조 · 아이보리 · 골드 라인", "시안"),
        card("detail/detail-B.html", "shots/detail-B-desktop.png", "상세 B 모던 그리드", "고딕 · 카드 · 벤토", "시안"),
        card("detail/detail-C.html", "shots/detail-C-desktop.png", "상세 C 시네마틱", "다크 네이비 · 필름 스트립", "시안"),
        card("home/home-1.html", "shots/home-1-desktop.png", "홈 1 영상 히어로형", "풀스크린 다크 히어로", "시안"),
        card("home/home-2.html", "shots/home-2-desktop.png", "홈 2 공지·포털형", "헤드라인 | 공지·일정", "시안"),
        card("home/home-3.html", "shots/home-3-desktop.png", "홈 3 바로가기 허브형", "벤토 타일 허브", "시안"),
    ])
    files = "".join(f'<a href="{h}">{t}<span>{d}</span></a>' for h, t, d in [
        ("prompts/00_design-system.md", "00 디자인 규칙", "색·글꼴·여백 — Claude Design 첫 메시지"),
        ("prompts/01_logo.md", "01 로고 메타 프롬프트", "모노그램 3시안 + 목업 프롬프트"),
        ("prompts/02_detail-page.md", "02 상세페이지 메타 프롬프트", "섹션 구성 + 사진 프롬프트"),
        ("prompts/03_homepage.md", "03 홈페이지 메타 프롬프트", "메뉴·구성 + 3시안 요청"),
        ("prompts/references.md", "레퍼런스 조사", "국내외 대학 스튜디오 사이트 7곳"),
        ("proposal/studio-booking.pdf", "스튜디오 예약·승인 자동화 개선방안", "A4 3쪽 — 구글 캘린더 → AI 예약·자동 승인"),
        ("README.md", "README", "다시 만들기·이미지 자동화 사용법"),
    ])
    page = head("HY FLIP 프로젝트", CSS) + f"""<body>
<header class="top"><div class="w">{logo('seal', 140)}<div>
  <div class="eyebrow">HY FLIP · PROJECT HUB</div>
  <h1>한양 플립러닝 콘텐츠 개발 사업<br>디자인 프로젝트</h1>
  <p>로고 → 사업 상세페이지 → 홈페이지 순서로 문답을 거쳐 확정한 결과물과 비교 시안, 메타 프롬프트를 한곳에 모았습니다.</p>
</div></div></header>
<main class="w">
  <dl class="sum">
    <div><dt>LOGO</dt><dd>3단 로고 체계<small>D 인장 · A 모노그램 · E 타일</small></dd></div>
    <div><dt>DETAIL</dt><dd>A+C 리믹스<small>아카데믹 + 시네마틱</small></dd></div>
    <div><dt>HOME</dt><dd>영상 히어로 + 포털<small>바로가기 · 공지 · 일정</small></dd></div>
    <div><dt>PHOTO</dt><dd>GPT 실사 이미지<small>{photo}</small></dd></div>
  </dl>
  <section><h2>확정 결과물</h2><p class="lead">카드를 누르면 실제 페이지가 열립니다 (데스크톱·모바일 대응).</p><div class="cards">{finals}</div></section>
  <section><h2>비교 시안</h2><p class="lead">확정 전에 함께 검토한 시안들입니다.</p><div class="cards">{drafts}</div></section>
  <section><h2>이미지 · 문서</h2><p class="lead"><a href="assets/gallery.html" style="color:var(--navy);font-weight:700">GPT 실사 이미지 갤러리 열기 →</a></p>
    <div class="files">{files}</div></section>
  <div class="kw">🔑 <b>핵심 키워드</b> — HY FLIP · 신뢰·아카데믹 · 남색 #0E4A84 + 골드 #C8A24A · H 기둥 = F 기둥 모노그램 ·
    인장/모노그램/타일 3단 체계 · 밝은 본문 + 시네마틱 다크 밴드 · 교표는 자리표시</div>
</main>
<footer class="w">※ 제안·포트폴리오용 디자인 시안입니다. 수치·후기·연락처는 예시이며, 한양대학교 공식 교표·로고가 아닙니다.</footer>
</body></html>
"""
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    print(f"index.html (사진 {made}/{len(items)})")


if __name__ == "__main__":
    main()
