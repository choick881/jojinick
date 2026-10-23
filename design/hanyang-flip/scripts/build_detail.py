"""사업 상세페이지 3시안 → detail/detail-{A,B,C}.html

  A Classic Academic  — 흰/아이보리, 명조 헤드라인, 얇은 골드 라인, 대학 출판물 같은 정돈감
  B Modern Grid       — 고딕 중심, 카드·벤토 그리드, 큰 단계 번호
  C Cinematic Studio  — 딥네이비 다크, 풀블리드 실사, 영화 크레딧 같은 타이포
"""

from pathlib import Path

from site_kit import C, IMG_JS, PLAY, emblem_ph, head, icon, img, logo

OUT = Path(__file__).resolve().parent.parent / "detail"


def faq_items(cls="faq"):
    return "".join(f'<details class="{cls}"><summary>{q}{icon("plus", 20, "pm")}</summary><p>{a}</p></details>'
                   for q, a in C["faq"])


def nav_links():
    ids = ["about", "process", "studio", "ai", "cases", "faq"]
    return "".join(f'<a href="#{i}">{t}</a>' for i, t in zip(ids, C["nav"]))


# ═══════════════════════════════════════════════════════════════════
# A. Classic Academic
# ═══════════════════════════════════════════════════════════════════
CSS_A = """
:root{--navy:#0E4A84;--deep:#0A2E55;--ink:#1A2233;--muted:#5B6475;--gold:#C8A24A;--ivory:#F7F5F0;--line:#E3E6EC;
  --serif:'Noto Serif KR',Georgia,serif;--sans:'Noto Sans KR',system-ui,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:#fff;color:var(--ink);font:400 17px/1.75 var(--sans);-webkit-font-smoothing:antialiased;word-break:keep-all}
a{color:inherit;text-decoration:none}
.w{max-width:1200px;margin:0 auto;padding:0 48px}
.nav{position:sticky;top:0;z-index:10;background:rgba(255,255,255,.96);border-bottom:1px solid var(--line);backdrop-filter:blur(6px)}
.nav .w{display:flex;align-items:center;gap:28px;height:76px}
.brand{display:flex;align-items:center;gap:12px;color:var(--navy)}
.brand b{font:900 21px/1 var(--serif);letter-spacing:.06em;display:block}
.brand small{font-size:11px;color:var(--muted);letter-spacing:.02em}
.nav nav{display:flex;gap:26px;margin-left:auto;font-size:15px;color:#3a4356}
.nav nav a:hover{color:var(--navy)}
.nav .emblem-ph{color:var(--muted)}
.btn{display:inline-flex;align-items:center;gap:8px;font:700 15px/1 var(--sans);padding:16px 26px;border-radius:2px;border:1px solid var(--navy);transition:.2s}
.btn.primary{background:var(--navy);color:#fff} .btn.primary:hover{background:var(--deep)}
.btn.ghost{color:var(--navy)} .btn.ghost:hover{background:var(--ivory)}
.btn.sm{padding:11px 18px;font-size:14px}
.eyebrow{font:700 12px/1 var(--sans);letter-spacing:.2em;color:var(--gold);text-transform:uppercase}
.hero{padding:96px 0 104px}
.hero .w{display:grid;grid-template-columns:1.1fr .9fr;gap:72px;align-items:center}
.hero h1{font:900 60px/1.22 var(--serif);color:var(--deep);margin:22px 0 0;letter-spacing:-.01em}
.rule{width:64px;height:2px;background:var(--gold);margin:32px 0}
.hero p.sub{font-size:19px;color:#3a4356;max-width:520px}
.hero .btns{display:flex;gap:12px;margin-top:36px;flex-wrap:wrap}
.facts{display:grid;grid-template-columns:repeat(3,auto);gap:28px;margin-top:48px;padding-top:28px;border-top:1px solid var(--line)}
.facts dt{font-size:12px;color:var(--muted);letter-spacing:.06em} .facts dd{font-weight:700;color:var(--deep);font-size:15px}
.frame{position:relative} .frame::before{content:"";position:absolute;inset:22px -22px -22px 22px;border:1px solid var(--gold)}
.frame .ph{position:relative;aspect-ratio:4/5}
section.s{padding:120px 0} section.alt{background:var(--ivory)}
.sh{display:grid;grid-template-columns:220px 1fr;gap:48px;margin-bottom:56px}
.sh .no{font:700 13px/1.6 var(--sans);color:var(--gold);letter-spacing:.18em;border-top:2px solid var(--navy);padding-top:14px}
.sh h2{font:900 40px/1.3 var(--serif);color:var(--deep)}
.sh p{color:var(--muted);margin-top:14px;max-width:640px}
.flip{display:grid;grid-template-columns:.9fr 1.1fr;gap:56px;align-items:stretch}
.flip .ph{min-height:420px}
table.cmp{width:100%;border-collapse:collapse;font-size:16px}
.cmp th,.cmp td{text-align:left;padding:20px 16px;border-bottom:1px solid var(--line);vertical-align:top}
.cmp thead th{font:700 13px/1 var(--sans);letter-spacing:.1em;color:var(--muted);border-bottom:2px solid var(--deep)}
.cmp thead th.on{color:var(--navy)}
.cmp td:first-child{font:700 15px/1.6 var(--serif);color:var(--deep);width:96px}
.cmp td.on{color:var(--navy);font-weight:700;background:rgba(14,74,132,.04)}
.who{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-top:1px solid var(--deep)}
.who li{list-style:none;padding:36px 32px 8px 0;border-right:1px solid var(--line)} .who li+li{padding-left:32px} .who li:last-child{border-right:0}
.who .num{font:900 44px/1 var(--serif);color:var(--gold)}
.who h3{font:700 21px/1.45 var(--serif);color:var(--deep);margin:18px 0 10px}
.who p{color:var(--muted);font-size:16px}
.steps{border-top:1px solid var(--deep)}
.step{display:grid;grid-template-columns:120px 1fr 1.2fr 220px;gap:32px;padding:34px 0;border-bottom:1px solid var(--line);align-items:baseline}
.step .n{font:900 48px/1 var(--serif);color:var(--navy)}
.step h3{font:700 24px/1.3 var(--serif);color:var(--deep)} .step .dur{display:block;font:500 13px/1 var(--sans);color:var(--muted);margin-top:10px}
.step .prep{font-size:14px;color:var(--muted);border-left:2px solid var(--gold);padding-left:14px}
.step .prep b{display:block;font-size:11px;letter-spacing:.14em;color:var(--gold)}
.studio{display:grid;grid-template-columns:repeat(3,1fr);gap:40px 28px}
.studio figure .ph{aspect-ratio:4/3}
.studio figure:first-child{grid-column:span 2;grid-row:span 2} .studio figure:first-child .ph{aspect-ratio:auto;height:calc(100% - 64px);min-height:360px}
.studio figcaption{padding-top:14px} .studio figcaption b{font:700 18px/1.4 var(--serif);color:var(--deep);display:block} .studio figcaption span{font-size:14px;color:var(--muted)}
.ai{display:grid;grid-template-columns:repeat(2,1fr);gap:0;border-top:1px solid var(--deep)}
.ai li{list-style:none;display:grid;grid-template-columns:56px 1fr;gap:20px;padding:36px 32px 36px 0;border-bottom:1px solid var(--line)}
.ai li:nth-child(even){padding-left:32px;border-left:1px solid var(--line)}
.ai .ic{color:var(--navy);width:40px;height:40px}
.ai h3{font:700 20px/1.4 var(--serif);color:var(--deep);margin-bottom:6px} .ai p{color:var(--muted);font-size:16px}
.cases{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.case .ph{aspect-ratio:16/9} .case .ph .play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:1;width:52px;height:52px;border-radius:50%;background:rgba(255,255,255,.92);color:var(--navy);display:grid;place-items:center}
.case h3{font:700 18px/1.45 var(--serif);color:var(--deep);margin-top:16px} .case span{font-size:14px;color:var(--muted)}
.quotes{display:grid;grid-template-columns:1fr 1fr;gap:56px;margin-top:72px}
.quotes blockquote{font:500 22px/1.65 var(--serif);color:var(--deep);border-left:2px solid var(--gold);padding-left:28px}
.quotes cite{display:block;font:500 14px/1 var(--sans);color:var(--muted);font-style:normal;margin-top:18px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--deep);border-bottom:1px solid var(--line)}
.stat{padding:44px 24px 40px 0} .stat+.stat{padding-left:28px;border-left:1px solid var(--line)}
.stat b{font:900 64px/1 var(--serif);color:var(--navy)} .stat i{font:700 20px/1 var(--serif);color:var(--navy);font-style:normal;margin-left:4px}
.stat span{display:block;margin-top:16px;font-size:15px;color:var(--muted);padding-top:14px;border-top:2px solid var(--gold);width:48px;white-space:nowrap}
.note{font-size:13px;color:var(--muted);margin-top:18px}
.faq-wrap{max-width:860px;border-top:1px solid var(--deep)}
details.faq{border-bottom:1px solid var(--line)}
details.faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:20px;padding:26px 0;font:700 19px/1.5 var(--serif);color:var(--deep)}
details.faq summary::-webkit-details-marker{display:none}
details.faq .pm{color:var(--gold);flex:none;transition:.2s} details.faq[open] .pm{transform:rotate(45deg)}
details.faq p{padding:0 48px 28px 0;color:#3a4356}
.cta{background:var(--deep);color:#fff;padding:120px 0;position:relative;overflow:hidden}
.cta .wm{position:absolute;right:-80px;top:50%;transform:translateY(-50%);opacity:.08;--mark:#fff;--accent:#fff}
.cta .w{position:relative}
.cta h2{font:900 48px/1.3 var(--serif);max-width:720px} .cta p{color:#c9d6e8;margin:20px 0 40px;max-width:560px}
.cta .btn.gold{background:var(--gold);border-color:var(--gold);color:var(--deep)} .cta .btn.line{border-color:rgba(255,255,255,.5);color:#fff}
.cta .contact{margin-top:48px;font-size:14px;color:#9fb3cc}
footer{background:#07213e;color:#9fb3cc;padding:48px 0;font-size:13px}
footer .w{display:flex;align-items:center;gap:20px;flex-wrap:wrap} footer .brand{color:#fff;--mark:#fff;--accent:var(--gold)}
footer .emblem-ph{color:#9fb3cc} footer p{margin-left:auto;max-width:520px;text-align:right}
@media (max-width:960px){
  .w{padding:0 20px} .nav nav,.nav .emblem-ph{display:none} .nav .w{height:64px}
  .hero{padding:56px 0 72px} .hero .w{grid-template-columns:1fr;gap:56px} .hero h1{font-size:38px}
  .facts{grid-template-columns:1fr;gap:14px} .frame::before{inset:14px -10px -14px 10px}
  section.s{padding:72px 0} .sh{grid-template-columns:1fr;gap:16px;margin-bottom:36px} .sh h2{font-size:30px}
  .flip{grid-template-columns:1fr;gap:28px} .flip .ph{min-height:240px}
  .cmp th,.cmp td{padding:14px 8px;font-size:14px} .cmp td:first-child{width:64px;white-space:nowrap}
  .who{grid-template-columns:1fr} .who li,.who li+li{padding:28px 0;border-right:0;border-bottom:1px solid var(--line)}
  .step{grid-template-columns:64px 1fr;gap:12px 16px} .step .n{font-size:34px} .step p,.step .prep{grid-column:2}
  .studio{grid-template-columns:1fr 1fr;gap:28px 14px} .studio figure:first-child{grid-column:span 2;grid-row:auto}
  .studio figure:first-child .ph{height:auto;min-height:0;aspect-ratio:4/3}
  .ai{grid-template-columns:1fr} .ai li,.ai li:nth-child(even){padding:28px 0;border-left:0}
  .cases{grid-template-columns:1fr} .quotes{grid-template-columns:1fr;gap:36px;margin-top:48px} .quotes blockquote{font-size:18px}
  .stats{grid-template-columns:1fr 1fr} .stat,.stat+.stat{padding:28px 12px 28px 0;border-left:0} .stat b{font-size:44px}
  .cta{padding:80px 0} .cta h2{font-size:32px} footer p{margin-left:0;text-align:left}
}
"""


def a_sh(no, title, lead=""):
    """A 스타일 섹션 제목 (번호 라벨 + 명조 제목 + 설명)."""
    return (f'<div class="sh"><div class="no">{no}</div><div><h2>{title}</h2>'
            f'{f"<p>{lead}</p>" if lead else ""}</div></div>')


def a_parts(studio_n=6):
    """A 스타일 본문 조각들 — page_a 와 page_final 이 함께 씀."""
    C_ = C
    facts = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in C_["facts"])
    rows = "".join(f'<tr><td>{a}</td><td>{b}</td><td class="on">{c}</td></tr>' for a, b, c in C_["flip"]["rows"])
    who = "".join(f'<li><div class="num">0{i}</div><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(C_["who"], 1))
    steps = "".join(
        f'<div class="step"><div class="n">{n}</div><h3>{t}<span class="dur">소요 {dur}</span></h3>'
        f'<p>{d}</p><div class="prep"><b>교수님 준비물</b>{prep}</div></div>'
        for n, t, d, dur, prep in C_["steps"])
    studio = "".join(f'<figure>{img(k)}<figcaption><b>{t}</b><span>{d}</span></figcaption></figure>'
                     for k, t, d in C_["studio"][:studio_n])
    ai = "".join(f'<li>{icon(i, 40)}<div><h3>{t}</h3><p>{d}</p></div></li>' for i, t, d in C_["ai"])
    cases = "".join(f'<article class="case">{thumb(k)}<h3>{t}</h3><span>{m}</span></article>' for k, t, m in C_["cases"][:3])
    quotes = "".join(f'<blockquote>“{q}”<cite>— {who_} (예시)</cite></blockquote>' for q, who_ in C_["quotes"])
    stats = "".join(f'<div class="stat"><b>{v}</b><i>{u}</i><span>{l}</span></div>' for v, u, l in C_["stats"])
    return facts, rows, who, steps, studio, ai, cases, quotes, stats


def page_a():
    C_ = C
    facts, rows, who, steps, studio, ai, cases, quotes, stats = a_parts()
    sh = a_sh

    return head("HY FLIP 상세 A", CSS_A) + f"""<body>
<header class="nav"><div class="w">
  <a class="brand" href="#">{logo('seal', 46)}<span><b>HY FLIP</b><small>한양 플립러닝 콘텐츠 개발 사업</small></span></a>
  <nav>{nav_links()}</nav>{emblem_ph()}
  <a class="btn primary sm" href="#apply">제작 신청</a>
</div></header>

<section class="hero"><div class="w">
  <div>
    <div class="eyebrow">{C_['eyebrow']}</div>
    <h1>{C_['h1'][0]}<br>{C_['h1'][1]}</h1>
    <div class="rule"></div>
    <p class="sub">{C_['sub']}</p>
    <div class="btns"><a class="btn primary" href="#apply">{C_['cta1']} {icon('arrow', 18)}</a>
      <a class="btn ghost" href="#">{icon('down', 18)} {C_['cta2']}</a></div>
    <dl class="facts">{facts}</dl>
  </div>
  <div class="frame">{img('studio-hero', label='studio-hero (교수 촬영 장면)')}</div>
</div></section>

<section class="s alt" id="about"><div class="w">
  {sh('01 — ABOUT', C_['flip']['title'], C_['flip']['lead'])}
  <div class="flip">{img('flipped-class', label='flipped-class (토론 수업)')}
    <table class="cmp"><thead><tr><th></th><th>기존 수업</th><th class="on">플립러닝</th></tr></thead><tbody>{rows}</tbody></table>
  </div>
</div></section>

<section class="s"><div class="w">
  {sh('02 — FOR YOU', '이런 교수님께 권합니다')}
  <ul class="who">{who}</ul>
</div></section>

<section class="s alt" id="process"><div class="w">
  {sh('03 — PROCESS', '제작은 이렇게 진행됩니다', '신청부터 LMS 탑재까지 평균 6주. 교수님이 직접 하실 일은 굵게 표시된 준비물뿐입니다.')}
  <div class="steps">{steps}</div>
</div></section>

<section class="s" id="studio"><div class="w">
  {sh('04 — STUDIO', '전문 스튜디오와 장비', '방송 수준의 촬영 환경을 교수님 일정에 맞춰 예약해 드립니다.')}
  <div class="studio">{studio}</div>
</div></section>

<section class="s alt" id="ai"><div class="w">
  {sh('05 — AI', 'AI 로 더 빠르고, 더 넓게', '반복 작업은 AI 가, 최종 품질은 사람이 책임집니다.')}
  <ul class="ai">{ai}</ul>
</div></section>

<section class="s" id="cases"><div class="w">
  {sh('06 — CASES', '먼저 시작한 교수님들')}
  <div class="cases">{cases}</div>
  <div class="quotes">{quotes}</div>
</div></section>

<section class="s alt"><div class="w">
  {sh('07 — RESULTS', '숫자로 보는 HY FLIP')}
  <div class="stats">{stats}</div>
  <p class="note">※ 예시 수치입니다. 실제 사업 실적으로 교체됩니다.</p>
</div></section>

<section class="s" id="faq"><div class="w">
  {sh('08 — FAQ', '자주 묻는 질문')}
  <div class="faq-wrap">{faq_items()}</div>
</div></section>

<section class="cta" id="apply">{logo('seal', 560, 'wm')}<div class="w">
  <div class="eyebrow">APPLY</div>
  <h2>{C_['cta_h']}</h2><p>{C_['cta_p']}</p>
  <div class="btns" style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn gold" href="#">{C_['cta1']} {icon('arrow', 18)}</a>
    <a class="btn line" href="#">{icon('down', 18)} {C_['cta2']}</a></div>
  <div class="contact">{C_['contact']} (예시)</div>
</div></section>

<footer><div class="w">
  <span class="brand">{logo('seal', 40)}<b style="font:900 18px var(--serif);letter-spacing:.06em">HY FLIP</b></span>{emblem_ph()}
  <p>{C_['notice']}</p>
</div></footer>
{IMG_JS}
</body></html>
"""


def thumb(k, cls=""):
    """사례 썸네일: 이미지 자리 + 가운데 재생 버튼."""
    return img(k, cls).replace("></div>", f'><span class="play">{PLAY}</span></div>', 1)


# ═══════════════════════════════════════════════════════════════════
# B. Modern Grid
# ═══════════════════════════════════════════════════════════════════
CSS_B = """
:root{--navy:#0E4A84;--deep:#0A2E55;--ink:#121A2A;--muted:#5B6475;--gold:#C8A24A;--soft:#F3F5F8;--line:#E1E5EC;
  --sans:'Noto Sans KR',system-ui,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:#fff;color:var(--ink);font:400 16px/1.7 var(--sans);-webkit-font-smoothing:antialiased;word-break:keep-all}
a{color:inherit;text-decoration:none}
.w{max-width:1240px;margin:0 auto;padding:0 40px}
.nav{position:sticky;top:0;z-index:10;background:#fff;border-bottom:1px solid var(--line)}
.nav .w{display:flex;align-items:center;gap:32px;height:72px}
.brand{display:flex;align-items:center;gap:10px} .brand b{font:900 22px/1 var(--sans);letter-spacing:.04em;color:var(--navy)}
.nav nav{display:flex;gap:4px;margin-left:auto}
.nav nav a{font-size:14.5px;font-weight:500;padding:8px 14px;border-radius:999px;color:#374055} .nav nav a:hover{background:var(--soft)}
.nav .emblem-ph{color:var(--muted)}
.btn{display:inline-flex;align-items:center;gap:8px;font:700 15px/1 var(--sans);padding:17px 26px;border-radius:4px;transition:.2s}
.btn.primary{background:var(--navy);color:#fff} .btn.primary:hover{background:var(--deep)}
.btn.soft{background:var(--soft);color:var(--navy)} .btn.sm{padding:12px 18px;font-size:14px}
.pill{display:inline-flex;align-items:center;gap:8px;font:700 13px/1 var(--sans);color:var(--navy);background:var(--soft);padding:9px 14px;border-radius:999px}
.pill i{width:7px;height:7px;border-radius:50%;background:var(--gold)}
.hero{padding:80px 0 40px}
.hero-top{display:grid;grid-template-columns:1fr 340px;gap:48px;align-items:end}
.hero h1{font:900 76px/1.12 var(--sans);letter-spacing:-.035em;margin-top:24px;color:var(--ink)}
.hero h1 em{font-style:normal;color:var(--navy);background:linear-gradient(transparent 78%,rgba(200,162,74,.55) 78%)}
.hero .sub{font-size:18px;color:#3d475b;margin-top:24px;max-width:600px}
.hero .btns{display:flex;gap:10px;margin-top:32px;flex-wrap:wrap}
.factlist{border-top:2px solid var(--ink)}
.factlist div{display:flex;justify-content:space-between;gap:12px;padding:16px 0;border-bottom:1px solid var(--line);font-size:14px}
.factlist dt{color:var(--muted)} .factlist dd{font-weight:700;text-align:right}
.hero-img{margin-top:56px;position:relative}
.hero-img .ph{aspect-ratio:21/8;border-radius:8px} .hero-img .ph::after{bottom:auto;top:12px;left:auto;right:12px}
.chips{position:absolute;left:24px;bottom:24px;display:flex;gap:8px;flex-wrap:wrap;z-index:2}
.chips span{background:rgba(255,255,255,.94);color:var(--ink);font:700 13px/1 var(--sans);padding:10px 14px;border-radius:999px;display:flex;gap:6px;align-items:center}
.chips .ic{color:var(--navy)}
section.s{padding:112px 0} section.soft{background:var(--soft)}
.sh{display:flex;justify-content:space-between;align-items:end;gap:40px;margin-bottom:48px;flex-wrap:wrap}
.sh .k{font:800 13px/1 var(--sans);color:var(--navy);letter-spacing:.14em}
.sh h2{font:900 44px/1.25 var(--sans);letter-spacing:-.03em;margin-top:14px}
.sh p{max-width:440px;color:var(--muted)}
.ba{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.ba .card{border-radius:8px;padding:36px;background:#fff;border:1px solid var(--line)}
.ba .card.on{background:var(--navy);color:#fff;border-color:var(--navy)}
.ba .tag{font:800 12px/1 var(--sans);letter-spacing:.16em;color:var(--muted)} .ba .on .tag{color:var(--gold)}
.ba h3{font:900 28px/1.3 var(--sans);margin:12px 0 24px;letter-spacing:-.02em}
.ba .row{display:grid;grid-template-columns:84px 1fr;gap:12px;padding:16px 0;border-top:1px solid var(--line)}
.ba .on .row{border-color:rgba(255,255,255,.18)}
.ba .row b{font-size:13px;color:var(--muted)} .ba .on .row b{color:#a9c0dc}
.ba .on .row span{font-weight:700}
.who{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.who .card{border:1px solid var(--line);border-radius:8px;padding:32px;background:#fff}
.who .ck{width:44px;height:44px;border-radius:50%;background:var(--navy);color:#fff;display:grid;place-items:center}
.who h3{font:800 20px/1.45 var(--sans);margin:22px 0 8px;letter-spacing:-.01em} .who p{color:var(--muted);font-size:15px}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;counter-reset:s}
.step{position:relative;background:#fff;border:1px solid var(--line);border-radius:8px;padding:28px;display:flex;flex-direction:column}
.step .n{font:900 72px/1 var(--sans);color:transparent;-webkit-text-stroke:1.5px var(--navy);letter-spacing:-.04em}
.step h3{font:900 24px/1.3 var(--sans);margin:22px 0 8px} .step p{color:#3d475b;font-size:15px;flex:1}
.step .dur{display:inline-block;margin-top:18px;font:700 12px/1 var(--sans);background:var(--soft);color:var(--navy);padding:8px 10px;border-radius:4px;align-self:flex-start}
.step .prep{margin-top:18px;padding-top:16px;border-top:1px dashed var(--line);font-size:13px;color:var(--muted)}
.step .prep b{color:var(--gold);margin-right:6px}
.step:not(:last-child)::after{content:"";position:absolute;right:-16px;top:58px;width:12px;height:12px;border-top:2px solid var(--navy);border-right:2px solid var(--navy);transform:rotate(45deg);z-index:1;background:transparent}
.bento{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:230px;gap:16px}
.bento figure{position:relative;border-radius:8px;overflow:hidden}
.bento figure .ph{position:absolute;inset:0}
.bento figure:nth-child(1){grid-column:span 2;grid-row:span 2}
.bento figure:nth-child(6),.bento figure:nth-child(7){grid-column:span 2}
.bento figcaption{position:absolute;left:0;right:0;top:0;padding:18px 20px;color:#fff;background:linear-gradient(rgba(6,24,46,.65),transparent);z-index:1}
.bento figcaption b{display:block;font:800 17px/1.4 var(--sans)} .bento figcaption span{font-size:13px;opacity:.85}
.ai{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.ai .card{background:#fff;border-radius:8px;padding:28px;border:1px solid var(--line)}
.ai .icw{width:56px;height:56px;border-radius:12px;background:var(--soft);color:var(--navy);display:grid;place-items:center}
.ai h3{font:800 19px/1.4 var(--sans);margin:22px 0 8px} .ai p{font-size:15px;color:var(--muted)}
.ai .bar{height:6px;border-radius:3px;background:var(--soft);margin-top:22px;overflow:hidden}
.ai .bar i{display:block;height:100%;background:linear-gradient(90deg,var(--navy),#3f7cc0)}
.cases{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.case .ph{aspect-ratio:16/10;border-radius:8px}
.play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:1;width:52px;height:52px;border-radius:50%;background:rgba(255,255,255,.94);color:var(--navy);display:grid;place-items:center}
.case h3{font:800 17px/1.45 var(--sans);margin-top:14px} .case span{font-size:13px;color:var(--muted)}
.quotes{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:40px}
.quotes blockquote{background:var(--soft);border-radius:8px;padding:32px;font:500 18px/1.7 var(--sans)}
.quotes blockquote::before{content:"“";display:block;font:900 56px/0.6 Georgia,serif;color:var(--gold);margin:10px 0 8px}
.quotes cite{display:block;font-size:13px;color:var(--muted);font-style:normal;margin-top:14px}
.statband{background:var(--navy);color:#fff;border-radius:12px;padding:56px;display:grid;grid-template-columns:repeat(4,1fr);gap:24px}
.statband div+div{border-left:1px solid rgba(255,255,255,.18);padding-left:32px}
.statband b{font:900 60px/1 var(--sans);letter-spacing:-.03em} .statband i{font:700 22px/1 var(--sans);font-style:normal;color:var(--gold);margin-left:4px}
.statband span{display:block;font-size:14px;color:#b9cbe2;margin-top:12px}
.note{font-size:13px;color:var(--muted);margin-top:14px}
.faqgrid{display:grid;grid-template-columns:360px 1fr;gap:64px}
.faqgrid h2{font:900 44px/1.25 var(--sans);letter-spacing:-.03em;margin-top:14px} .faqgrid p.l{color:var(--muted);margin-top:16px}
details.faq{border:1px solid var(--line);border-radius:8px;margin-bottom:12px;background:#fff}
details.faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:16px;padding:22px 24px;font:800 17px/1.5 var(--sans)}
details.faq summary::-webkit-details-marker{display:none}
details.faq .pm{color:var(--navy);flex:none;transition:.2s} details.faq[open] .pm{transform:rotate(45deg)}
details.faq p{padding:0 24px 22px;color:#3d475b}
.cta-card{background:var(--deep);color:#fff;border-radius:16px;padding:72px;display:grid;grid-template-columns:1fr auto;gap:40px;align-items:center;position:relative;overflow:hidden}
.cta-card .tilewm{position:absolute;right:-60px;bottom:-90px;opacity:.1;--mark:#fff;--accent:#fff;--knock:var(--deep)}
.cta-card h2{font:900 44px/1.25 var(--sans);letter-spacing:-.03em} .cta-card p{color:#b9cbe2;margin-top:14px}
.cta-card .btns{display:flex;flex-direction:column;gap:10px;position:relative}
.cta-card .btn.gold{background:var(--gold);color:var(--deep)} .cta-card .btn.out{border:1px solid rgba(255,255,255,.4);color:#fff}
.cta-card small{display:block;margin-top:28px;color:#8fa6c4;font-size:13px}
footer{border-top:1px solid var(--line);padding:40px 0;font-size:13px;color:var(--muted)}
footer .w{display:flex;align-items:center;gap:18px;flex-wrap:wrap} footer p{margin-left:auto;max-width:540px;text-align:right}
@media (max-width:1000px){
  .w{padding:0 20px} .nav nav,.nav .emblem-ph{display:none} .nav .w{height:64px} .nav .btn{margin-left:auto}
  .hero{padding:48px 0 24px} .hero-top{grid-template-columns:1fr;gap:36px} .hero h1{font-size:42px}
  .hero-img{margin-top:36px} .hero-img .ph{aspect-ratio:4/3} .chips{left:12px;bottom:12px;right:12px}
  section.s{padding:72px 0} .sh h2,.faqgrid h2{font-size:32px}
  .ba,.who,.quotes{grid-template-columns:1fr} .ba .card{padding:26px}
  .steps{grid-template-columns:1fr 1fr;gap:12px} .step::after{display:none} .step .n{font-size:52px} .step{padding:20px}
  .bento{grid-template-columns:1fr 1fr;grid-auto-rows:160px;gap:10px}
  .ai{grid-template-columns:1fr 1fr;gap:10px} .ai .card{padding:20px}
  .cases{grid-template-columns:1fr 1fr;gap:20px 12px}
  .statband{grid-template-columns:1fr 1fr;padding:32px 24px;gap:28px 16px} .statband div+div{border-left:0;padding-left:0} .statband b{font-size:40px}
  .faqgrid{grid-template-columns:1fr;gap:28px}
  .cta-card{grid-template-columns:1fr;padding:40px 24px} .cta-card h2{font-size:30px}
  footer p{margin-left:0;text-align:left}
}
@media (max-width:520px){ .steps,.ai{grid-template-columns:1fr} .hero h1{font-size:36px} }
"""


def page_b():
    facts = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in C["facts"])
    before = "".join(f'<div class="row"><b>{a}</b><span>{b}</span></div>' for a, b, _ in C["flip"]["rows"])
    after = "".join(f'<div class="row"><b>{a}</b><span>{c}</span></div>' for a, _, c in C["flip"]["rows"])
    who = "".join(f'<div class="card"><div class="ck">{icon("check", 22)}</div><h3>{t}</h3><p>{d}</p></div>'
                  for t, d in C["who"])
    steps = "".join(f'<div class="step"><div class="n">{n}</div><h3>{t}</h3><p>{d}</p><span class="dur">소요 {dur}</span>'
                    f'<div class="prep"><b>준비물</b>{prep}</div></div>' for n, t, d, dur, prep in C["steps"])
    bento = "".join(f'<figure>{img(k)}<figcaption><b>{t}</b><span>{d}</span></figcaption></figure>'
                    for k, t, d in C["studio"])
    bars = [92, 78, 85, 88]
    ai = "".join(f'<div class="card"><div class="icw">{icon(i, 28)}</div><h3>{t}</h3><p>{d}</p>'
                 f'<div class="bar"><i style="width:{b}%"></i></div></div>' for (i, t, d), b in zip(C["ai"], bars))
    cases = "".join(f'<article class="case">{thumb(k)}<h3>{t}</h3><span>{m}</span></article>' for k, t, m in C["cases"])
    quotes = "".join(f'<blockquote>{q}<cite>{w} (예시)</cite></blockquote>' for q, w in C["quotes"])
    stats = "".join(f'<div><b>{v}</b><i>{u}</i><span>{l}</span></div>' for v, u, l in C["stats"])

    def sh(k, title, lead=""):
        return f'<div class="sh"><div><div class="k">{k}</div><h2>{title}</h2></div>{f"<p>{lead}</p>" if lead else ""}</div>'

    return head("HY FLIP 상세 B", CSS_B) + f"""<body>
<header class="nav"><div class="w">
  <a class="brand" href="#">{logo('tile', 36)}<b>HY FLIP</b></a>
  <nav>{nav_links()}</nav>{emblem_ph()}
  <a class="btn primary sm" href="#apply">제작 신청</a>
</div></header>

<section class="hero"><div class="w">
  <div class="hero-top">
    <div>
      <span class="pill"><i></i>{C['eyebrow']}</span>
      <h1>{C['h1'][0]}<br><em>{C['h1'][1]}</em></h1>
      <p class="sub">{C['sub']}</p>
      <div class="btns"><a class="btn primary" href="#apply">{C['cta1']} {icon('arrow', 18)}</a>
        <a class="btn soft" href="#">{icon('down', 18)} {C['cta2']}</a></div>
    </div>
    <dl class="factlist">{facts}</dl>
  </div>
  <div class="hero-img">{img('studio-hero', label='studio-hero (교수 촬영 장면)')}
    <div class="chips"><span>{icon('camera', 16)} 4K 전문 스튜디오</span><span>{icon('cc', 16)} AI 자막·더빙</span><span>{icon('book', 16)} 교수설계 컨설팅</span></div>
  </div>
</div></section>

<section class="s" id="about"><div class="w">
  {sh('ABOUT', C['flip']['title'], C['flip']['lead'])}
  <div class="ba">
    <div class="card"><div class="tag">BEFORE</div><h3>기존 수업</h3>{before}</div>
    <div class="card on"><div class="tag">AFTER · FLIPPED</div><h3>플립러닝</h3>{after}</div>
  </div>
</div></section>

<section class="s soft"><div class="w">
  {sh('FOR YOU', '이런 교수님께 권합니다')}
  <div class="who">{who}</div>
</div></section>

<section class="s" id="process"><div class="w">
  {sh('PROCESS', '4단계, 평균 6주', '신청부터 LMS 탑재까지. 교수님은 준비물만 챙기시면 나머지는 HY FLIP 이 진행합니다.')}
  <div class="steps">{steps}</div>
</div></section>

<section class="s soft" id="studio"><div class="w">
  {sh('STUDIO', '전문 스튜디오와 장비', '방송 수준의 촬영 환경을 교수님 일정에 맞춰 예약해 드립니다.')}
  <div class="bento">{bento}</div>
</div></section>

<section class="s" id="ai"><div class="w">
  {sh('AI', 'AI 로 더 빠르고, 더 넓게', '반복 작업은 AI 가, 최종 품질은 사람이 책임집니다. (막대: 작업 시간 단축률 예시)')}
  <div class="ai">{ai}</div>
</div></section>

<section class="s soft" id="cases"><div class="w">
  {sh('CASES', '먼저 시작한 교수님들')}
  <div class="cases">{cases}</div>
  <div class="quotes">{quotes}</div>
</div></section>

<section class="s"><div class="w">
  {sh('RESULTS', '숫자로 보는 HY FLIP')}
  <div class="statband">{stats}</div>
  <p class="note">※ 예시 수치입니다. 실제 사업 실적으로 교체됩니다.</p>
</div></section>

<section class="s soft" id="faq"><div class="w faqgrid">
  <div><div class="sh" style="margin:0"><div><div class="k">FAQ</div><h2>자주 묻는 질문</h2></div></div>
    <p class="l">더 궁금한 점은 사업단으로 문의해 주세요.<br>{C['contact']} (예시)</p></div>
  <div>{faq_items()}</div>
</div></section>

<section class="s" id="apply"><div class="w">
  <div class="cta-card">{logo('tile', 420, 'tilewm')}
    <div style="position:relative"><span class="pill" style="background:rgba(255,255,255,.1);color:#fff"><i></i>APPLY</span>
      <h2 style="margin-top:20px">{C['cta_h']}</h2><p>{C['cta_p']}</p><small>{C['contact']} (예시)</small></div>
    <div class="btns"><a class="btn gold" href="#">{C['cta1']} {icon('arrow', 18)}</a><a class="btn out" href="#">{icon('down', 18)} {C['cta2']}</a></div>
  </div>
</div></section>

<footer><div class="w">
  <span class="brand">{logo('tile', 30)}<b style="font-size:18px">HY FLIP</b></span>{emblem_ph()}
  <p>{C['notice']}</p>
</div></footer>
{IMG_JS}
</body></html>
"""


# ═══════════════════════════════════════════════════════════════════
# C. Cinematic Studio
# ═══════════════════════════════════════════════════════════════════
CSS_C = """
:root{--bg:#071A31;--bg2:#0A2442;--card:#0E2C50;--navy:#0E4A84;--gold:#C8A24A;--gold2:#E2C77F;--txt:#EEF2F8;--muted:#9FB0C8;--line:rgba(255,255,255,.12);
  --serif:'Noto Serif KR',Georgia,serif;--sans:'Noto Sans KR',system-ui,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--txt);font:400 17px/1.75 var(--sans);-webkit-font-smoothing:antialiased;word-break:keep-all}
a{color:inherit;text-decoration:none}
.w{max-width:1200px;margin:0 auto;padding:0 48px}
.nav{position:absolute;top:0;left:0;right:0;z-index:10}
.nav .w{display:flex;align-items:center;gap:28px;height:88px;--mark:#fff;--accent:var(--gold)}
.brand{display:flex;align-items:center;gap:12px} .brand b{font:900 20px/1 var(--serif);letter-spacing:.1em}
.nav nav{display:flex;gap:26px;margin-left:auto;font-size:14.5px;color:#d5deea}
.nav .emblem-ph{color:#d5deea}
.btn{display:inline-flex;align-items:center;gap:10px;font:700 15px/1 var(--sans);padding:17px 28px;border-radius:2px;transition:.2s}
.btn.gold{background:var(--gold);color:#0A1B30} .btn.gold:hover{background:var(--gold2)}
.btn.ghost{border:1px solid rgba(255,255,255,.45);color:#fff} .btn.ghost:hover{background:rgba(255,255,255,.08)}
.btn.sm{padding:11px 18px;font-size:14px} .btn.outg{border:1px solid var(--gold);color:var(--gold2)}
.hero{position:relative;min-height:820px;display:flex;align-items:flex-end;overflow:hidden;padding-top:120px}
.hero > .ph{position:absolute;inset:0}
.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(7,26,49,.96) 0%,rgba(7,26,49,.78) 42%,rgba(7,26,49,.15) 100%),
  linear-gradient(0deg,rgba(7,26,49,1) 0%,transparent 40%)}
.hero .w{position:relative;z-index:2;width:100%;padding-bottom:64px}
.rec{display:inline-flex;align-items:center;gap:10px;font:700 12px/1 var(--sans);letter-spacing:.24em;color:#d5deea}
.rec i{width:9px;height:9px;border-radius:50%;background:#E5484D;box-shadow:0 0 0 4px rgba(229,72,77,.2)}
.hero h1{font:900 72px/1.18 var(--serif);margin:26px 0 24px;letter-spacing:-.01em}
.hero h1 span{color:var(--gold2)}
.hero .sub{font-size:19px;color:#c9d5e5;max-width:540px}
.hero .btns{display:flex;gap:12px;margin-top:40px;flex-wrap:wrap}
.credits{display:grid;grid-template-columns:repeat(3,1fr);margin-top:72px;border-top:1px solid var(--line)}
.credits div{padding:22px 24px 0 0} .credits div+div{padding-left:28px;border-left:1px solid var(--line)}
.credits dt{font:700 11px/1 var(--sans);letter-spacing:.22em;color:var(--gold);text-transform:uppercase}
.credits dd{font:500 16px/1.5 var(--serif);margin-top:10px}
section.s{padding:128px 0} section.alt{background:var(--bg2)}
.sh{margin-bottom:60px;max-width:760px}
.sh .k{font:700 12px/1 var(--sans);letter-spacing:.3em;color:var(--gold)}
.sh h2{font:900 46px/1.3 var(--serif);margin-top:18px} .sh p{color:var(--muted);margin-top:16px}
.flip{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}
.flip .ph{aspect-ratio:4/5;border-radius:2px}
.scene{padding:28px 0;border-top:1px solid var(--line)} .scene:last-child{border-bottom:1px solid var(--line)}
.scene .t{font:700 12px/1 var(--sans);letter-spacing:.24em;color:var(--gold)}
.scene h3{font:700 23px/1.4 var(--serif);margin:12px 0 6px}
.scene p{color:var(--muted);font-size:15px} .scene p s{color:#6f819c}
.who li{list-style:none;display:grid;grid-template-columns:120px 1fr 1fr;gap:32px;align-items:baseline;padding:40px 0;border-top:1px solid var(--line)}
.who li:last-child{border-bottom:1px solid var(--line)}
.who .num{font:900 64px/1 var(--serif);color:transparent;-webkit-text-stroke:1px var(--gold)}
.who h3{font:700 26px/1.4 var(--serif)} .who p{color:var(--muted)}
.strip{position:relative;background:#030C18;padding:34px 0;border-radius:4px}
.strip::before,.strip::after{content:"";position:absolute;left:16px;right:16px;height:10px;
  background:repeating-linear-gradient(90deg,rgba(255,255,255,.22) 0 14px,transparent 14px 30px);border-radius:2px}
.strip::before{top:12px} .strip::after{bottom:12px}
.frames{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding:0 16px}
.frame{background:var(--card);padding:28px 24px;min-height:300px;display:flex;flex-direction:column;border-radius:2px}
.frame .take{font:700 11px/1 var(--sans);letter-spacing:.24em;color:var(--gold)}
.frame .n{font:900 56px/1 var(--serif);margin:18px 0 6px;color:#fff}
.frame h3{font:700 24px/1.3 var(--serif)} .frame p{color:var(--muted);font-size:15px;margin-top:10px;flex:1}
.frame .meta{font-size:13px;color:#c9d5e5;border-top:1px solid var(--line);padding-top:14px;margin-top:16px}
.frame .meta b{color:var(--gold2);font-weight:700;margin-right:6px}
.studio{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}
.studio figure{position:relative;grid-column:span 2} .studio figure .ph{aspect-ratio:4/3;border-radius:2px}
.studio figure:nth-child(1),.studio figure:nth-child(2){grid-column:span 3} .studio figure:nth-child(1) .ph,.studio figure:nth-child(2) .ph{aspect-ratio:16/10}
.studio figure:nth-child(6),.studio figure:nth-child(7){grid-column:span 3} .studio figure:nth-child(6) .ph,.studio figure:nth-child(7) .ph{aspect-ratio:16/8}
.studio figcaption{position:absolute;left:0;right:0;bottom:0;padding:48px 20px 16px;background:linear-gradient(transparent,rgba(3,12,24,.9));z-index:1}
.studio figcaption b{font:700 18px/1.4 var(--serif);display:block} .studio figcaption span{font-size:13px;color:#c9d5e5}
.studio .ph::after{bottom:auto;top:10px}
.ai{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--line);border:1px solid var(--line)}
.ai div{background:var(--bg);padding:36px 28px}
.ai .ic{color:var(--gold);width:36px;height:36px}
.ai h3{font:700 20px/1.4 var(--serif);margin:24px 0 8px} .ai p{color:var(--muted);font-size:15px}
.cases{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:16px}
.case .ph{aspect-ratio:16/10;border-radius:2px} .case:first-child .ph{aspect-ratio:16/11.3}
.play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:1;width:60px;height:60px;border-radius:50%;
  border:1px solid rgba(255,255,255,.7);background:rgba(7,26,49,.35);color:#fff;display:grid;place-items:center;backdrop-filter:blur(2px)}
.case h3{font:700 19px/1.45 var(--serif);margin-top:16px} .case span{font-size:13px;color:var(--muted)}
.quotes{display:grid;grid-template-columns:1fr 1fr;gap:64px;margin-top:88px}
.quotes blockquote{font:500 25px/1.6 var(--serif);position:relative;padding-top:44px}
.quotes blockquote::before{content:"“";position:absolute;top:-6px;left:-4px;font:900 88px/1 var(--serif);color:var(--gold)}
.quotes cite{display:block;font:500 14px/1 var(--sans);color:var(--muted);font-style:normal;margin-top:22px;letter-spacing:.04em}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;text-align:center}
.stats b{font:900 76px/1 var(--serif);color:var(--gold2)} .stats i{font:700 22px/1 var(--serif);font-style:normal;color:var(--gold);margin-left:4px}
.stats span{display:block;font:700 12px/1 var(--sans);letter-spacing:.24em;color:var(--muted);margin-top:18px}
.note{font-size:13px;color:#6f819c;margin-top:36px;text-align:center}
.faq-wrap{max-width:880px}
details.faq{border-top:1px solid var(--line)} details.faq:last-child{border-bottom:1px solid var(--line)}
details.faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:20px;padding:28px 0;font:700 20px/1.5 var(--serif)}
details.faq summary::-webkit-details-marker{display:none}
details.faq .pm{color:var(--gold);flex:none;transition:.2s} details.faq[open] .pm{transform:rotate(45deg)}
details.faq p{padding:0 48px 28px 0;color:var(--muted)}
.cta{position:relative;min-height:600px;display:flex;align-items:center;overflow:hidden;text-align:center}
.cta > .ph{position:absolute;inset:0}
.cta::after{content:"";position:absolute;inset:0;background:rgba(5,18,36,.78)}
.cta .w{position:relative;z-index:1;width:100%}
.cta h2{font:900 56px/1.3 var(--serif)} .cta p{color:#c9d5e5;margin:22px auto 44px;max-width:560px}
.cta .btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.cta small{display:block;margin-top:44px;color:var(--muted);font-size:14px}
footer{background:#030C18;padding:56px 0;font-size:13px;color:#6f819c}
footer .w{display:flex;align-items:center;gap:20px;flex-wrap:wrap;--mark:#fff;--accent:var(--gold)}
footer .brand{color:#fff} footer .emblem-ph{color:#6f819c} footer p{margin-left:auto;max-width:520px;text-align:right}
@media (max-width:1000px){
  .w{padding:0 20px} .nav nav,.nav .emblem-ph{display:none} .nav .w{height:72px} .nav .btn{margin-left:auto}
  .hero{min-height:720px} .hero h1{font-size:40px} .hero .sub{font-size:17px}
  .credits{grid-template-columns:1fr;margin-top:44px} .credits div,.credits div+div{padding:16px 0 0;border-left:0}
  section.s{padding:80px 0} .sh h2{font-size:32px} .sh{margin-bottom:40px}
  .flip{grid-template-columns:1fr;gap:36px} .flip .ph{aspect-ratio:4/3}
  .who li{grid-template-columns:72px 1fr;gap:8px 16px;padding:28px 0} .who .num{font-size:44px} .who p{grid-column:2} .who h3{font-size:21px}
  .frames{grid-template-columns:1fr 1fr} .frame{min-height:0;padding:20px}
  .studio{grid-template-columns:1fr 1fr;gap:10px} .studio figure,.studio figure:nth-child(1),.studio figure:nth-child(2){grid-column:span 1}
  .studio figure:nth-child(1){grid-column:span 2}
  .studio figure:nth-child(6),.studio figure:nth-child(7){grid-column:span 1} .studio figure:nth-child(6) .ph,.studio figure:nth-child(7) .ph{aspect-ratio:4/3}
  .studio figcaption{padding:32px 12px 10px} .studio figcaption b{font-size:15px} .studio figcaption span{display:none}
  .ai{grid-template-columns:1fr 1fr} .ai div{padding:24px 18px}
  .cases{grid-template-columns:1fr} .quotes{grid-template-columns:1fr;gap:48px;margin-top:56px} .quotes blockquote{font-size:20px}
  .stats{grid-template-columns:1fr 1fr;gap:44px 12px} .stats b{font-size:48px}
  .cta h2{font-size:34px} footer p{margin-left:0;text-align:left}
}
@media (max-width:520px){ .frames,.ai{grid-template-columns:1fr} }
"""


def page_c():
    credits = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in C["facts"])
    scenes = "".join(f'<div class="scene"><div class="t">SCENE 0{i} · {a}</div><h3>{c}</h3><p>기존: <s>{b}</s></p></div>'
                     for i, (a, b, c) in enumerate(C["flip"]["rows"], 1))
    who = "".join(f'<li><div class="num">0{i}</div><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(C["who"], 1))
    frames = "".join(f'<div class="frame"><div class="take">TAKE {n}</div><div class="n">{n}</div><h3>{t}</h3><p>{d}</p>'
                     f'<div class="meta"><b>소요</b>{dur}<br><b>준비물</b>{prep}</div></div>'
                     for n, t, d, dur, prep in C["steps"])
    studio = "".join(f'<figure>{img(k)}<figcaption><b>{t}</b><span>{d}</span></figcaption></figure>' for k, t, d in C["studio"])
    ai = "".join(f'<div>{icon(i, 36)}<h3>{t}</h3><p>{d}</p></div>' for i, t, d in C["ai"])
    cases = "".join(f'<article class="case">{thumb(k)}<h3>{t}</h3><span>{m}</span></article>' for k, t, m in C["cases"][:3])
    quotes = "".join(f'<blockquote>{q}<cite>— {w} (예시)</cite></blockquote>' for q, w in C["quotes"])
    stats = "".join(f'<div><b>{v}</b><i>{u}</i><span>{l}</span></div>' for v, u, l in C["stats"])

    def sh(k, title, lead=""):
        return f'<div class="sh"><div class="k">{k}</div><h2>{title}</h2>{f"<p>{lead}</p>" if lead else ""}</div>'

    return head("HY FLIP 상세 C", CSS_C) + f"""<body>
<header class="nav"><div class="w">
  <a class="brand" href="#">{logo('seal', 48)}<b>HY FLIP</b></a>
  <nav>{nav_links()}</nav>{emblem_ph()}
  <a class="btn outg sm" href="#apply">제작 신청</a>
</div></header>

<section class="hero">{img('studio-hero', label='studio-hero (교수 촬영 장면 · 풀블리드)')}<div class="w">
  <div class="rec"><i></i>REC · HY FLIP STUDIO</div>
  <h1>{C['h1'][0]}<br><span>{C['h1'][1]}</span></h1>
  <p class="sub">{C['sub']}</p>
  <div class="btns"><a class="btn gold" href="#apply">{C['cta1']} {icon('arrow', 18)}</a><a class="btn ghost" href="#">{icon('down', 18)} {C['cta2']}</a></div>
  <dl class="credits">{credits}</dl>
</div></section>

<section class="s" id="about"><div class="w flip">
  <div>{sh('ABOUT · FLIPPED LEARNING', C['flip']['title'], C['flip']['lead'])}{scenes}</div>
  {img('flipped-class', label='flipped-class (토론 수업)')}
</div></section>

<section class="s alt"><div class="w">
  {sh('FOR YOU', '이런 교수님께 권합니다')}
  <ul class="who">{who}</ul>
</div></section>

<section class="s" id="process"><div class="w">
  {sh('PRODUCTION', '촬영은 네 번의 테이크로', '신청부터 LMS 탑재까지 평균 6주. 교수님은 준비물만 챙기시면 됩니다.')}
  <div class="strip"><div class="frames">{frames}</div></div>
</div></section>

<section class="s alt" id="studio"><div class="w">
  {sh('STUDIO', '방송 수준의 촬영 환경', '전문 PD·편집자가 상주하는 스튜디오를 교수님 일정에 맞춰 예약해 드립니다.')}
  <div class="studio">{studio}</div>
</div></section>

<section class="s" id="ai"><div class="w">
  {sh('POST-PRODUCTION · AI', 'AI 로 더 빠르고, 더 넓게', '반복 작업은 AI 가, 최종 품질은 사람이 책임집니다.')}
  <div class="ai">{ai}</div>
</div></section>

<section class="s alt" id="cases"><div class="w">
  {sh('NOW SHOWING', '먼저 시작한 교수님들')}
  <div class="cases">{cases}</div>
  <div class="quotes">{quotes}</div>
</div></section>

<section class="s"><div class="w">
  <div class="sh" style="margin:0 auto 64px;text-align:center"><div class="k">RESULTS</div><h2>숫자로 보는 HY FLIP</h2></div>
  <div class="stats">{stats}</div>
  <p class="note">※ 예시 수치입니다. 실제 사업 실적으로 교체됩니다.</p>
</div></section>

<section class="s alt" id="faq"><div class="w">
  {sh('FAQ', '자주 묻는 질문')}
  <div class="faq-wrap">{faq_items()}</div>
</div></section>

<section class="cta" id="apply">{img('campus-dusk', label='campus-dusk (캠퍼스 야경)')}<div class="w">
  <div class="sh" style="margin:0 auto;max-width:none"><div class="k">APPLY</div></div>
  <h2 style="margin-top:18px">{C['cta_h']}</h2><p>{C['cta_p']}</p>
  <div class="btns"><a class="btn gold" href="#">{C['cta1']} {icon('arrow', 18)}</a><a class="btn ghost" href="#">{icon('down', 18)} {C['cta2']}</a></div>
  <small>{C['contact']} (예시)</small>
</div></section>

<footer><div class="w">
  <span class="brand">{logo('seal', 40)}<b>HY FLIP</b></span>{emblem_ph()}
  <p>{C['notice']}</p>
</div></footer>
{IMG_JS}
</body></html>
"""


# ═══════════════════════════════════════════════════════════════════
# 확정안: A + C 리믹스 — A 의 라이트 본문 + C 의 다크 밴드(히어로·제작절차·CTA)
# C 에서 가져온 스타일은 .dk- 접두사로만 추가해 A 클래스와 충돌하지 않게 함
# ═══════════════════════════════════════════════════════════════════
CSS_DK = """
.nav-dk{position:absolute;top:0;left:0;right:0;z-index:10}
.nav-dk .w{display:flex;align-items:center;gap:28px;height:88px;--mark:#fff;--accent:var(--gold);color:#fff}
.nav-dk .brand{color:#fff} .nav-dk .brand small{color:#b9c8dc}
.nav-dk nav{display:flex;gap:26px;margin-left:auto;font-size:15px;color:#d5deea} .nav-dk .emblem-ph{color:#d5deea}
.btn.gold{background:var(--gold);border-color:var(--gold);color:#0A1B30} .btn.gold:hover{background:#E2C77F}
.btn.wline{border-color:rgba(255,255,255,.45);color:#fff} .btn.wline:hover{background:rgba(255,255,255,.08)}
.dk-hero{position:relative;min-height:860px;display:flex;align-items:flex-end;overflow:hidden;padding-top:128px;background:#071A31;color:#EEF2F8}
.dk-hero > .ph{position:absolute;inset:0}
.dk-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(7,26,49,.96) 0%,rgba(7,26,49,.78) 42%,rgba(7,26,49,.12) 100%),
  linear-gradient(0deg,rgba(7,26,49,1) 0%,transparent 42%)}
.dk-hero .w{position:relative;z-index:2;width:100%;padding-bottom:64px}
.rec{display:inline-flex;align-items:center;gap:10px;font:700 12px/1 var(--sans);letter-spacing:.24em;color:#d5deea}
.rec i{width:9px;height:9px;border-radius:50%;background:#E5484D;box-shadow:0 0 0 4px rgba(229,72,77,.2)}
.dk-hero h1{font:900 72px/1.18 var(--serif);margin:26px 0 24px;color:#fff} .dk-hero h1 span{color:#E2C77F}
.dk-hero .sub{font-size:19px;color:#c9d5e5;max-width:540px}
.dk-hero .btns{display:flex;gap:12px;margin-top:40px;flex-wrap:wrap}
.credits{display:grid;grid-template-columns:repeat(3,1fr);margin-top:72px;border-top:1px solid rgba(255,255,255,.14)}
.credits div{padding:22px 24px 0 0} .credits div+div{padding-left:28px;border-left:1px solid rgba(255,255,255,.14)}
.credits dt{font:700 11px/1 var(--sans);letter-spacing:.22em;color:var(--gold)} .credits dd{font:500 16px/1.5 var(--serif);margin-top:10px}
.dk-band{background:#071A31;color:#EEF2F8;padding:128px 0}
.dk-band .sh .no{border-top-color:var(--gold)} .dk-band .sh h2{color:#fff} .dk-band .sh p{color:#9FB0C8}
.dk-strip{position:relative;background:#030C18;padding:34px 0;border-radius:4px}
.dk-strip::before,.dk-strip::after{content:"";position:absolute;left:16px;right:16px;height:10px;
  background:repeating-linear-gradient(90deg,rgba(255,255,255,.22) 0 14px,transparent 14px 30px);border-radius:2px}
.dk-strip::before{top:12px} .dk-strip::after{bottom:12px}
.dk-frames{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding:0 16px}
.dk-frame{background:#0E2C50;padding:28px 24px;min-height:300px;display:flex;flex-direction:column;border-radius:2px}
.dk-frame .take{font:700 11px/1 var(--sans);letter-spacing:.24em;color:var(--gold)}
.dk-frame .n{font:900 56px/1 var(--serif);margin:18px 0 6px;color:#fff}
.dk-frame h3{font:700 24px/1.3 var(--serif);color:#fff} .dk-frame p{color:#9FB0C8;font-size:15px;margin-top:10px;flex:1}
.dk-frame .meta{font-size:13px;color:#c9d5e5;border-top:1px solid rgba(255,255,255,.12);padding-top:14px;margin-top:16px}
.dk-frame .meta b{color:#E2C77F;margin-right:6px}
.bento{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:230px;gap:16px}
.bento figure{position:relative;overflow:hidden}
.bento figure .ph{position:absolute;inset:0}
.bento figure:nth-child(1){grid-column:span 2;grid-row:span 2}
.bento figure:nth-child(6),.bento figure:nth-child(7){grid-column:span 2}
.bento figcaption{position:absolute;left:0;right:0;bottom:0;padding:56px 20px 16px;color:#fff;background:linear-gradient(transparent,rgba(6,24,46,.6) 40%,rgba(6,24,46,.94));z-index:1;text-shadow:0 1px 2px rgba(0,0,0,.35)}
.bento figcaption b{display:block;font:700 18px/1.4 var(--serif)} .bento figcaption span{font-size:13px;opacity:.85}
.bento .ph::after{bottom:auto;top:10px}
.dk-cta{position:relative;min-height:620px;display:flex;align-items:center;overflow:hidden;text-align:center;color:#fff;background:#071A31}
.dk-cta > .ph{position:absolute;inset:0}
.dk-cta::after{content:"";position:absolute;inset:0;background:rgba(5,18,36,.8)}
.dk-cta .seal-wm{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);opacity:.07;z-index:1;--mark:#fff;--accent:#fff}
.dk-cta .w{position:relative;z-index:2;width:100%}
.dk-cta h2{font:900 56px/1.3 var(--serif);margin-top:18px} .dk-cta p{color:#c9d5e5;margin:22px auto 44px;max-width:560px}
.dk-cta .btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.dk-cta small{display:block;margin-top:44px;color:#9FB0C8;font-size:14px}
@media (max-width:960px){
  .nav-dk nav,.nav-dk .emblem-ph{display:none} .nav-dk .w{height:72px} .nav-dk .btn{margin-left:auto}
  .dk-hero{min-height:720px;padding-top:112px} .dk-hero h1{font-size:40px} .dk-hero .sub{font-size:17px}
  .credits{grid-template-columns:1fr;margin-top:44px} .credits div,.credits div+div{padding:16px 0 0;border-left:0}
  .dk-band{padding:80px 0}
  .dk-frames{grid-template-columns:1fr 1fr} .dk-frame{min-height:0;padding:20px}
  .bento{grid-template-columns:1fr 1fr;grid-auto-rows:150px;gap:10px} .bento figcaption{padding:32px 12px 10px} .bento figcaption span{display:none}
  .bento figcaption b{font-size:15px}
  .dk-cta h2{font-size:34px}
}
@media (max-width:520px){ .dk-frames{grid-template-columns:1fr} }
"""


def page_final():
    _, rows, who, _, studio, ai, cases, quotes, stats = a_parts(studio_n=7)
    credits = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in C["facts"])
    frames = "".join(f'<div class="dk-frame"><div class="take">TAKE {n}</div><div class="n">{n}</div><h3>{t}</h3><p>{d}</p>'
                     f'<div class="meta"><b>소요</b>{dur}<br><b>준비물</b>{prep}</div></div>'
                     for n, t, d, dur, prep in C["steps"])
    sh = a_sh
    return head("HY FLIP 상세페이지", CSS_A + CSS_DK) + f"""<body>
<header class="nav-dk"><div class="w">
  <a class="brand" href="#">{logo('seal', 48)}<span><b>HY FLIP</b><small>한양 플립러닝 콘텐츠 개발 사업</small></span></a>
  <nav>{nav_links()}</nav>{emblem_ph()}
  <a class="btn gold sm" href="#apply">제작 신청</a>
</div></header>

<section class="dk-hero">{img('studio-hero', label='studio-hero (교수 촬영 장면 · 풀블리드)')}<div class="w">
  <div class="rec"><i></i>REC · HY FLIP STUDIO</div>
  <h1>{C['h1'][0]}<br><span>{C['h1'][1]}</span></h1>
  <p class="sub">{C['sub']}</p>
  <div class="btns"><a class="btn gold" href="#apply">{C['cta1']} {icon('arrow', 18)}</a><a class="btn wline" href="#">{icon('down', 18)} {C['cta2']}</a></div>
  <dl class="credits">{credits}</dl>
</div></section>

<section class="s" id="about"><div class="w">
  {sh('01 — ABOUT', C['flip']['title'], C['flip']['lead'])}
  <div class="flip">{img('flipped-class', label='flipped-class (토론 수업)')}
    <table class="cmp"><thead><tr><th></th><th>기존 수업</th><th class="on">플립러닝</th></tr></thead><tbody>{rows}</tbody></table>
  </div>
</div></section>

<section class="s alt"><div class="w">
  {sh('02 — FOR YOU', '이런 교수님께 권합니다')}
  <ul class="who">{who}</ul>
</div></section>

<section class="dk-band" id="process"><div class="w">
  {sh('03 — PRODUCTION', '촬영은 네 번의 테이크로', '신청부터 LMS 탑재까지 평균 6주. 교수님은 준비물만 챙기시면 됩니다.')}
  <div class="dk-strip"><div class="dk-frames">{frames}</div></div>
</div></section>

<section class="s" id="studio"><div class="w">
  {sh('04 — STUDIO', '전문 스튜디오와 장비', '방송 수준의 촬영 환경을 교수님 일정에 맞춰 예약해 드립니다.')}
  <div class="bento">{studio}</div>
</div></section>

<section class="s alt" id="ai"><div class="w">
  {sh('05 — AI', 'AI 로 더 빠르고, 더 넓게', '반복 작업은 AI 가, 최종 품질은 사람이 책임집니다.')}
  <ul class="ai">{ai}</ul>
</div></section>

<section class="s" id="cases"><div class="w">
  {sh('06 — CASES', '먼저 시작한 교수님들')}
  <div class="cases">{cases}</div>
  <div class="quotes">{quotes}</div>
</div></section>

<section class="s alt"><div class="w">
  {sh('07 — RESULTS', '숫자로 보는 HY FLIP')}
  <div class="stats">{stats}</div>
  <p class="note">※ 예시 수치입니다. 실제 사업 실적으로 교체됩니다.</p>
</div></section>

<section class="s" id="faq"><div class="w">
  {sh('08 — FAQ', '자주 묻는 질문')}
  <div class="faq-wrap">{faq_items()}</div>
</div></section>

<section class="dk-cta" id="apply">{img('campus-dusk', label='campus-dusk (캠퍼스 야경)')}{logo('seal', 620, 'seal-wm')}<div class="w">
  <div class="eyebrow">APPLY</div>
  <h2>{C['cta_h']}</h2><p>{C['cta_p']}</p>
  <div class="btns"><a class="btn gold" href="#">{C['cta1']} {icon('arrow', 18)}</a><a class="btn wline" href="#">{icon('down', 18)} {C['cta2']}</a></div>
  <small>{C['contact']} (예시)</small>
</div></section>

<footer><div class="w">
  <span class="brand">{logo('seal', 40)}<b style="font:900 18px var(--serif);letter-spacing:.06em">HY FLIP</b></span>{emblem_ph()}
  <p>{C['notice']}</p>
</div></footer>
{IMG_JS}
</body></html>
"""


PAGES = {"A": page_a, "B": page_b, "C": page_c, "final": page_final}


def main():
    OUT.mkdir(exist_ok=True)
    for k, fn in PAGES.items():
        (OUT / f"detail-{k}.html").write_text(fn(), encoding="utf-8")
        print(f"detail/detail-{k}.html")


if __name__ == "__main__":
    main()
