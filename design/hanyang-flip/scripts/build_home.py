"""홈페이지 3시안 → home/home-{1,2,3}.html  (톤: 상세페이지 확정안과 같은 A+C 리믹스)

  1 영상 히어로형   — 첫 화면 전체 시네마틱 다크 히어로 + 겹쳐 올라오는 바로가기 4칸
  2 공지·포털형     — 밝은 분할 히어로(헤드라인 | 공지·일정 카드) + 다크 강의 레일
  3 바로가기 허브형 — 첫 화면이 벤토 타일 허브(다크 히어로 타일 + 바로가기·수치·일정 타일)

스타일 바탕은 build_detail 의 CSS_A(라이트 본문) + CSS_DK(다크 밴드)를 그대로 쓰고,
홈 전용 블록만 CSS_HOME 으로 더합니다.
"""

from pathlib import Path

from build_detail import CSS_A, CSS_DK, thumb
from site_kit import C, IMG_JS, PLAY, emblem_ph, head, icon, img, logo

OUT = Path(__file__).resolve().parent.parent / "home"
DETAIL = "../detail/detail-final.html"

SLOGAN = ["수업을 뒤집으면,", "배움이 깊어집니다"]
HOME_SUB = "HY FLIP 은 교수님의 강의를 플립러닝 영상 콘텐츠로 만드는 한양 플립러닝 콘텐츠 개발 사업입니다."
MENU = [("사업소개", f"{DETAIL}#about"), ("제작절차", f"{DETAIL}#process"), ("스튜디오", f"{DETAIL}#studio"),
        ("제작사례", f"{DETAIL}#cases"), ("공지사항", "#notice")]
QUICK = [("arrow", "제작 신청", "5분이면 끝나는 온라인 신청"), ("calendar", "스튜디오 예약", "원하는 날짜·시간 선택"),
         ("down", "제작 가이드 PDF", "준비물·촬영 팁 한 번에"), ("help", "자주 묻는 질문", "비용·저작권·수정 안내")]
VALUES = [("전문 제작", "방송 PD·촬영감독·편집자가 한 팀으로 강의 영상 제작 전 과정을 맡습니다."),
          ("교수설계 컨설팅", "수업 전 영상과 수업 중 활동이 맞물리도록 차시 구성을 함께 설계합니다."),
          ("AI 후반작업", "AI 자막·더빙·요약·챕터 분할로 더 빠르게, 더 많은 학습자에게 닿습니다.")]

QHREF = {"제작 신청": f"{DETAIL}#apply", "스튜디오 예약": "../booking/booking.html", "자주 묻는 질문": f"{DETAIL}#faq"}

CSS_HOME = """
.lang{font:700 12.5px/1 var(--sans);letter-spacing:.1em;border:1px solid currentColor;padding:8px 9px;border-radius:2px;opacity:.85;flex:none}
.lang:hover{opacity:1} .nav .lang{color:var(--navy)} .nav-dk .lang{color:#fff}
@media (max-width:520px){.nav .brand small,.nav-dk .brand small{display:none} .nav .btn.sm,.nav-dk .btn.sm{white-space:nowrap;padding:10px 12px;font-size:13px} .lang{padding:8px 8px;font-size:12px}}
.dk-hero.tall{min-height:900px} .dk-hero.tall .w{padding-bottom:150px}
.quick{display:grid;grid-template-columns:repeat(4,1fr);background:#fff;box-shadow:0 24px 48px rgba(10,46,85,.14);position:relative;z-index:3;margin-top:-80px}
.quick a{padding:32px 28px;border-right:1px solid var(--line);display:flex;flex-direction:column;gap:12px;transition:.2s}
.quick a:last-child{border-right:0} .quick a:hover{background:var(--ivory)}
.quick .ic{color:var(--navy)} .quick b{font:700 19px/1.3 var(--serif);color:var(--deep)} .quick span{font-size:14px;color:var(--muted)}
.quick .go{color:var(--gold);margin-top:6px}
.dk-band .stats{border-color:rgba(255,255,255,.16)} .dk-band .stat+.stat{border-left-color:rgba(255,255,255,.16)}
.dk-band .stat b,.dk-band .stat i{color:#E2C77F} .dk-band .stat span{color:#9FB0C8;border-top-color:var(--gold)}
.dk-band .note{color:#6f819c}
.cases.four{grid-template-columns:repeat(4,1fr);gap:20px}
.dk-band .case h3{color:#fff} .dk-band .case span{color:#9FB0C8}
.more{display:flex;justify-content:flex-end;margin-top:28px} .more a{display:inline-flex;gap:8px;align-items:center;font-weight:700;color:var(--navy)}
.dk-band .more a{color:#E2C77F}
.board{display:grid;grid-template-columns:1.4fr 1fr;gap:56px}
.bh{display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid var(--deep);padding-bottom:14px}
.bh h3{font:900 26px/1.3 var(--serif);color:var(--deep)} .bh a{font-size:14px;color:var(--muted)}
.ntc li{list-style:none;display:grid;grid-template-columns:56px 1fr 52px;gap:16px;padding:18px 0;border-bottom:1px solid var(--line);align-items:center}
.ntc .tag{font:700 12px/1 var(--sans);color:var(--navy);border:1px solid currentColor;padding:6px 0;text-align:center;border-radius:2px}
.ntc .tag.행사{color:var(--gold)} .ntc .tag.안내{color:var(--muted)}
.ntc .t{font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap} .ntc time{color:var(--muted);font-size:14px;text-align:right}
.sched li{list-style:none;display:grid;grid-template-columns:92px 1fr;gap:16px;padding:16px 0;border-bottom:1px dashed var(--line);align-items:baseline}
.sched b{font:700 16px/1.4 var(--serif);color:var(--navy)} .sched li:first-child b{color:var(--gold)}
.sched li:first-child span::after{content:"다음 일정";margin-left:8px;font:700 11px/1 var(--sans);color:#fff;background:var(--gold);padding:3px 6px;border-radius:2px;vertical-align:2px}
.btn.play{gap:12px} .btn.play .pc{width:34px;height:34px;border-radius:50%;border:1px solid rgba(255,255,255,.6);display:grid;place-items:center;margin:-8px 0}
/* 2 공지·포털형 */
.portal{padding:72px 0 104px;background:linear-gradient(var(--ivory),#fff)}
.portal .w{display:grid;grid-template-columns:1.05fr 1fr;gap:56px;align-items:start}
.portal h1{font:900 56px/1.25 var(--serif);color:var(--deep);margin:20px 0 0}
.portal .sub{font-size:18px;color:#3a4356;max-width:500px}
.portal .btns{display:flex;gap:12px;margin:32px 0 40px;flex-wrap:wrap}
.portal .ph{aspect-ratio:16/8}
.pcard{background:#fff;border:1px solid var(--line);box-shadow:0 16px 40px rgba(10,46,85,.08);padding:28px 32px}
.pcard + .pcard{margin-top:16px}
.pcard.navy{background:var(--deep);border-color:var(--deep);color:#fff}
.pcard.navy .bh{border-bottom-color:var(--gold)} .pcard.navy .bh h3{color:#fff} .pcard.navy .bh a{color:#9FB0C8}
.pcard.navy .sched li{border-bottom-color:rgba(255,255,255,.14)} .pcard.navy .sched b{color:#E2C77F} .pcard.navy .sched li:first-child b{color:#fff}
.pcard .bh h3{font-size:22px}
.rail{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:16px;scrollbar-color:var(--gold) transparent}
.rail .case{flex:0 0 360px;scroll-snap-align:start}
.mini-steps{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--deep)}
.mini-steps div{padding:32px 28px 8px 0} .mini-steps div+div{padding-left:28px;border-left:1px solid var(--line)}
.mini-steps .n{font:900 40px/1 var(--serif);color:var(--gold)} .mini-steps h3{font:700 22px/1.4 var(--serif);color:var(--deep);margin:16px 0 6px}
.mini-steps p{color:var(--muted);font-size:15px}
/* 3 허브형 */
.hub{padding:40px 0 104px}
.hub-grid{display:grid;grid-template-columns:2fr 1fr 1fr;grid-template-rows:repeat(3,212px);gap:14px}
.hub-hero{grid-row:1/4;position:relative;overflow:hidden;color:#fff;padding:48px;display:flex;flex-direction:column;justify-content:flex-end;background:#071A31}
.hub-hero > .ph{position:absolute;inset:0}
.hub-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(7,26,49,.97) 0%,rgba(7,26,49,.7) 45%,rgba(7,26,49,.15) 100%)}
.hub-hero > :not(.ph){position:relative;z-index:2}
.hub-hero h1{font:900 52px/1.22 var(--serif);margin:20px 0 16px} .hub-hero h1 span{color:#E2C77F}
.hub-hero p{color:#c9d5e5;max-width:460px} .hub-hero .btns{display:flex;gap:12px;margin-top:28px;flex-wrap:wrap}
.tile{border:1px solid var(--line);padding:24px;display:flex;flex-direction:column;justify-content:space-between;background:#fff;transition:.2s}
.tile:hover{border-color:var(--navy)}
.tile .top{display:flex;justify-content:space-between;align-items:flex-start;color:var(--navy)}
.tile b{font:700 21px/1.3 var(--serif);color:var(--deep);display:block} .tile span{font-size:13.5px;color:var(--muted)}
.tile.gold{background:var(--gold);border-color:var(--gold)} .tile.gold .top,.tile.gold b{color:#0A1B30} .tile.gold span{color:#3d3214}
.tile.navy{background:var(--navy);border-color:var(--navy)} .tile.navy .top,.tile.navy b{color:#fff} .tile.navy span{color:#c9d6e8}
.tile .mini{display:flex;gap:22px} .tile .mini strong{font:900 34px/1 var(--serif);color:var(--navy)} .tile .mini em{font-style:normal;font-size:12px;color:var(--muted);display:block;margin-top:6px}
@media (max-width:960px){
  .dk-hero.tall{min-height:640px} .dk-hero.tall .w{padding-bottom:88px}
  .quick{grid-template-columns:1fr 1fr;margin-top:-40px} .quick a{padding:22px 18px;border-bottom:1px solid var(--line)} .quick a:nth-child(2n){border-right:0}
  .quick b{font-size:17px}
  .cases.four{grid-template-columns:1fr 1fr;gap:20px 12px}
  .board{grid-template-columns:1fr;gap:48px}
  .ntc li{grid-template-columns:48px 1fr;gap:6px 12px} .ntc time{grid-column:2;text-align:left;font-size:13px}
  .portal{padding:40px 0 64px} .portal .w{grid-template-columns:1fr;gap:36px} .portal h1{font-size:36px}
  .pcard{padding:22px 20px}
  .rail .case{flex-basis:78%}
  .mini-steps{grid-template-columns:1fr 1fr} .mini-steps div,.mini-steps div+div{padding:24px 12px 12px 0;border-left:0}
  .hub{padding:20px 0 64px}
  .hub-grid{grid-template-columns:1fr 1fr;grid-template-rows:auto;grid-auto-rows:160px;gap:10px}
  .hub-hero{grid-row:auto;grid-column:1/-1;min-height:480px;padding:28px 22px} .hub-hero h1{font-size:34px}
  .tile{padding:18px} .tile b{font-size:17px} .tile .mini strong{font-size:26px}
}
"""


def nav(dark):
    links = "".join(f'<a href="{h}">{t}</a>' for t, h in MENU)
    cls = "nav-dk" if dark else "nav"
    return (f'<header class="{cls}"><div class="w">'
            f'<a class="brand" href="#">{logo("mark", 40)}<span><b>HY FLIP</b><small>한양 플립러닝 콘텐츠 개발 사업</small></span></a>'
            f'<nav>{links}</nav>{emblem_ph()}<a class="btn gold sm" href="{DETAIL}#apply">제작 신청</a>'
            f'<a class="lang" href="home-en.html" lang="en" title="English">EN</a></div></header>')


def footer():
    return (f'<footer><div class="w"><span class="brand">{logo("seal", 44)}'
            f'<span><b style="font:900 18px var(--serif);letter-spacing:.06em;display:block">HY FLIP 사업단</b>'
            f'<small style="color:#9fb3cc">{C["contact"]} (예시)</small></span></span>{emblem_ph()}'
            f'<p>{C["notice"]}</p></div></footer>')


def notices(n=5):
    rows = "".join(f'<li><span class="tag {k}">{k}</span><a class="t" href="#">{t}</a><time>{d}</time></li>'
                   for k, t, d in C["notices"][:n])
    return f'<div class="bh"><h3>공지사항</h3><a href="#">전체 보기 +</a></div><ul class="ntc">{rows}</ul>'


def schedule():
    rows = "".join(f"<li><b>{d}</b><span>{t}</span></li>" for d, t in C["schedule"])
    return f'<div class="bh"><h3>이번 학기 일정</h3><a href="#">2026-1학기</a></div><ul class="sched">{rows}</ul>'


def values():
    return "".join(f'<li><div class="num">0{i}</div><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(VALUES, 1))


def lectures(n=4):
    return "".join(f'<article class="case">{thumb(k)}<h3>{t}</h3><span>{m}</span></article>' for k, t, m in C["cases"][:n])


def stats():
    return "".join(f'<div class="stat"><b>{v}</b><i>{u}</i><span>{l}</span></div>' for v, u, l in C["stats"])


def sh(no, title, lead=""):
    return (f'<div class="sh"><div class="no">{no}</div><div><h2>{title}</h2>'
            f'{f"<p>{lead}</p>" if lead else ""}</div></div>')


def css():
    return CSS_A + CSS_DK + CSS_HOME


PLAY_BTN = f'<a class="btn wline play" href="#"><span class="pc">{PLAY}</span>사업 소개 영상 보기</a>'


# ── 1 영상 히어로형 ──────────────────────────────────────────────────
def home_1():
    quick = "".join(f'<a href="{QHREF.get(t, "#")}">{icon(i, 30)}<b>{t}</b><span>{d}</span><span class="go">{icon("arrow", 18)}</span></a>'
                    for i, t, d in QUICK)
    return head("HY FLIP 홈 1", css()) + f"""<body>
{nav(True)}
<section class="dk-hero tall">{img('studio-hero', label='studio-hero (교수 촬영 장면 · 풀블리드)')}<div class="w">
  <div class="rec"><i></i>NOW RECRUITING · 2026 HY FLIP</div>
  <h1>{SLOGAN[0]}<br><span>{SLOGAN[1]}</span></h1>
  <p class="sub">{HOME_SUB}</p>
  <div class="btns"><a class="btn gold" href="{DETAIL}#apply">제작 신청하기 {icon('arrow', 18)}</a>{PLAY_BTN}</div>
</div></section>
<div class="w"><nav class="quick" aria-label="바로가기">{quick}</nav></div>

<section class="s" id="about"><div class="w">
  {sh('ABOUT', 'HY FLIP 이 하는 일', '교수님은 강의에만 집중하세요. 나머지는 세 가지 전문성으로 함께합니다.')}
  <ul class="who">{values()}</ul>
</div></section>

<section class="dk-band"><div class="w">
  {sh('RESULTS', '숫자로 보는 HY FLIP')}
  <div class="stats">{stats()}</div>
  <p class="note">※ 예시 수치입니다.</p>
</div></section>

<section class="s"><div class="w">
  {sh('NEW', '최신 제작 강의')}
  <div class="cases four">{lectures()}</div>
  <div class="more"><a href="{DETAIL}#cases">제작 사례 더 보기 {icon('arrow', 18)}</a></div>
</div></section>

<section class="s alt" id="notice"><div class="w board">
  <div>{notices()}</div><div>{schedule()}</div>
</div></section>
{footer()}
{IMG_JS}
</body></html>
"""


# ── 2 공지·포털형 ────────────────────────────────────────────────────
def home_2():
    steps = "".join(f'<div><div class="n">{n}</div><h3>{t}</h3><p>소요 {dur}</p></div>' for n, t, _, dur, _ in C["steps"])
    return head("HY FLIP 홈 2", css()) + f"""<body>
{nav(False)}
<section class="portal"><div class="w">
  <div>
    <div class="eyebrow">{C['eyebrow']}</div>
    <h1>{SLOGAN[0]}<br>{SLOGAN[1]}</h1>
    <div class="rule"></div>
    <p class="sub">{HOME_SUB}</p>
    <div class="btns"><a class="btn primary" href="{DETAIL}#apply">제작 신청하기 {icon('arrow', 18)}</a>
      <a class="btn ghost" href="{DETAIL}">사업 자세히 보기</a></div>
    {img('studio-hero', label='studio-hero (교수 촬영 장면)')}
  </div>
  <div id="notice">
    <div class="pcard">{notices()}</div>
    <div class="pcard navy">{schedule()}</div>
  </div>
</div></section>

<section class="dk-band"><div class="w">
  {sh('NEW', '최신 제작 강의', '옆으로 넘겨 더 보기 →')}
  <div class="rail">{lectures()}</div>
</div></section>

<section class="s" id="about"><div class="w">
  {sh('ABOUT', 'HY FLIP 이 하는 일')}
  <ul class="who">{values()}</ul>
</div></section>

<section class="s alt"><div class="w">
  {sh('PROCESS', '제작은 4단계, 평균 6주', '신청부터 LMS 탑재까지 담당 PD 가 함께합니다.')}
  <div class="mini-steps">{steps}</div>
  <div class="more"><a href="{DETAIL}#process">제작 절차 자세히 {icon('arrow', 18)}</a></div>
</div></section>

<section class="dk-cta">{img('campus-dusk', label='campus-dusk (캠퍼스 야경)')}{logo('seal', 620, 'seal-wm')}<div class="w">
  <div class="eyebrow">APPLY</div>
  <h2>{C['cta_h']}</h2><p>{C['cta_p']}</p>
  <div class="btns"><a class="btn gold" href="{DETAIL}#apply">제작 신청하기 {icon('arrow', 18)}</a>{PLAY_BTN}</div>
</div></section>
{footer()}
{IMG_JS}
</body></html>
"""


# ── 3 바로가기 허브형 ────────────────────────────────────────────────
def home_3():
    (i1, t1, d1), (i2, t2, d2), (i3, t3, d3), (i4, t4, d4) = QUICK
    nd, nt = C["schedule"][0]
    s0, s1 = C["stats"][0], C["stats"][2]
    quotes = "".join(f'<blockquote>“{q}”<cite>— {w} (예시)</cite></blockquote>' for q, w in C["quotes"])
    return head("HY FLIP 홈 3", css()) + f"""<body>
{nav(False)}
<section class="hub"><div class="w"><div class="hub-grid">
  <div class="hub-hero">{img('studio-hero', label='studio-hero (교수 촬영 장면)')}
    <div class="rec"><i></i>NOW RECRUITING · 2026 HY FLIP</div>
    <h1>{SLOGAN[0]}<br><span>{SLOGAN[1]}</span></h1>
    <p>{HOME_SUB}</p>
    <div class="btns"><a class="btn gold" href="{DETAIL}#apply">제작 신청하기 {icon('arrow', 18)}</a>{PLAY_BTN}</div>
  </div>
  <a class="tile gold" href="{DETAIL}#apply"><div class="top">{icon(i1, 28)}{icon('arrow', 22)}</div><div><b>{t1}</b><span>{d1}</span></div></a>
  <a class="tile" href="../booking/booking.html"><div class="top">{icon(i2, 28)}{icon('arrow', 22)}</div><div><b>{t2}</b><span>{d2}</span></div></a>
  <a class="tile" href="#"><div class="top">{icon(i3, 28)}{icon('arrow', 22)}</div><div><b>{t3}</b><span>{d3}</span></div></a>
  <a class="tile" href="{DETAIL}#faq"><div class="top">{icon(i4, 28)}{icon('arrow', 22)}</div><div><b>{t4}</b><span>{d4}</span></div></a>
  <div class="tile"><span>숫자로 보는 HY FLIP (예시)</span><div class="mini">
    <div><strong>{s0[0]}</strong><em>{s0[2]}</em></div><div><strong>{s1[0]}</strong><em>{s1[2]}</em></div></div></div>
  <a class="tile navy" href="#notice"><div class="top">{icon('calendar', 28)}<span style="color:#E2C77F;font-weight:700">다음 일정</span></div>
    <div><b>{nd} {nt}</b><span>이번 학기 전체 일정 보기</span></div></a>
</div></div></section>

<section class="s alt" id="notice"><div class="w board">
  <div>{notices()}</div><div>{schedule()}</div>
</div></section>

<section class="s" id="cases"><div class="w">
  {sh('CASES', '먼저 시작한 교수님들')}
  <div class="cases four">{lectures()}</div>
  <div class="quotes">{quotes}</div>
</div></section>

<section class="dk-cta">{img('campus-dusk', label='campus-dusk (캠퍼스 야경)')}{logo('seal', 620, 'seal-wm')}<div class="w">
  <div class="eyebrow">APPLY</div>
  <h2>{C['cta_h']}</h2><p>{C['cta_p']}</p>
  <div class="btns"><a class="btn gold" href="{DETAIL}#apply">제작 신청하기 {icon('arrow', 18)}</a>
    <a class="btn wline" href="{DETAIL}">사업 자세히 보기</a></div>
  <small>{C['contact']} (예시)</small>
</div></section>
{footer()}
{IMG_JS}
</body></html>
"""


# ── 확정안: 1 + 2 — 영상 히어로 + 바로가기, 바로 아래 공지·일정 카드(포털) ─────────
def home_final():
    quick = "".join(f'<a href="{QHREF.get(t, "#")}">{icon(i, 30)}<b>{t}</b><span>{d}</span><span class="go">{icon("arrow", 18)}</span></a>'
                    for i, t, d in QUICK)
    return head("HY FLIP 홈페이지", css()) + f"""<body>
{nav(True)}
<section class="dk-hero tall">{img('studio-hero', label='studio-hero (교수 촬영 장면 · 풀블리드)')}<div class="w">
  <div class="rec"><i></i>NOW RECRUITING · 2026 HY FLIP</div>
  <h1>{SLOGAN[0]}<br><span>{SLOGAN[1]}</span></h1>
  <p class="sub">{HOME_SUB}</p>
  <div class="btns"><a class="btn gold" href="{DETAIL}#apply">제작 신청하기 {icon('arrow', 18)}</a>{PLAY_BTN}</div>
</div></section>
<div class="w"><nav class="quick" aria-label="바로가기">{quick}</nav></div>

<section class="s" id="notice" style="padding-top:88px"><div class="w board">
  <div class="pcard">{notices()}</div>
  <div class="pcard navy">{schedule()}</div>
</div></section>

<section class="s alt" id="about"><div class="w">
  {sh('ABOUT', 'HY FLIP 이 하는 일', '교수님은 강의에만 집중하세요. 나머지는 세 가지 전문성으로 함께합니다.')}
  <ul class="who">{values()}</ul>
  <div class="more"><a href="{DETAIL}">사업 자세히 보기 {icon('arrow', 18)}</a></div>
</div></section>

<section class="dk-band"><div class="w">
  {sh('RESULTS', '숫자로 보는 HY FLIP')}
  <div class="stats">{stats()}</div>
  <p class="note">※ 예시 수치입니다.</p>
</div></section>

<section class="s"><div class="w">
  {sh('NEW', '최신 제작 강의')}
  <div class="cases four">{lectures()}</div>
  <div class="more"><a href="{DETAIL}#cases">제작 사례 더 보기 {icon('arrow', 18)}</a></div>
</div></section>

<section class="dk-cta">{img('campus-dusk', label='campus-dusk (캠퍼스 야경)')}{logo('seal', 620, 'seal-wm')}<div class="w">
  <div class="eyebrow">APPLY</div>
  <h2>{C['cta_h']}</h2><p>{C['cta_p']}</p>
  <div class="btns"><a class="btn gold" href="{DETAIL}#apply">제작 신청하기 {icon('arrow', 18)}</a>
    <a class="btn wline" href="{DETAIL}">사업 자세히 보기</a></div>
  <small>{C['contact']} (예시)</small>
</div></section>
{footer()}
{IMG_JS}
</body></html>
"""


def main():
    OUT.mkdir(exist_ok=True)
    for k, fn in {"1": home_1, "2": home_2, "3": home_3, "final": home_final}.items():
        (OUT / f"home-{k}.html").write_text(fn(), encoding="utf-8")
        print(f"home/home-{k}.html")


if __name__ == "__main__":
    main()
