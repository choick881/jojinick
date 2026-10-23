"""로고 2차 보드: 굵기·비율 변형 + 새 방향 3시안(D/E/F) + 2단 체계(인장+모노그램) 미리보기.

  python scripts/build_logos_r2.py   → logo/logo-board-r2.html, logo/logo-{D,E,F}.svg

A 모노그램과 B 인장 가운데 HF 를 굵기(w)·간격 파라미터로 다시 그립니다.
기본값(w=16 / wb=8)은 1차 시안(build_logos.py)과 같은 모양입니다.
"""

from build_logos import DEEP, GOLD, IVORY, NAVY, OUT

SANS = "'Noto Sans KR',Arial,sans-serif"
RING_TEXT = "HY FLIP · FLIPPED LEARNING CONTENT LAB · EST. 2026 ·"


def n(v):
    return f"{v:g}"


# ── A 모노그램 (파라미터) ─────────────────────────────────────────────
def a_mark(w=16, t=14, c1=30, c2=70, R=104, f=10, fold=True):
    """w: 기둥 굵기, t: 가로획 굵기, c1/c2: 두 기둥 중심, R: F 윗팔 끝, f: 접힘 크기."""
    L0, L1, S0, S1 = c1 - w / 2, c1 + w / 2, c2 - w / 2, c2 + w / 2
    y0, y1, mid = 59 - t / 2, 59 + t / 2, R - 6
    d = (f"M{n(L0)} 20H{n(L1)}V{n(y0)}H{n(S0)}V20H{n(R - f)}L{n(R)} {n(20 + f)}V{n(20 + w)}H{n(S1)}"
         f"V{n(y0)}H{n(mid)}V{n(y1)}H{n(S1)}V100H{n(S0)}V{n(y1)}H{n(L1)}V100H{n(L0)}Z")
    body = f'<path fill="var(--mark)" d="{d}"/>'
    if fold:
        body += f'<path fill="var(--accent)" d="M{n(R - f)} 20V{n(20 + f)}H{n(R)}Z"/>'
    return body


def placed(inner, cx, cy, s, ox=63, oy=60):
    return f'<g transform="translate({n(cx)} {n(cy)}) scale({n(s)}) translate(-{ox} -{oy})">{inner}</g>'


# ── B 인장 (파라미터) ────────────────────────────────────────────────
def seal_ring(uid):
    return (f'<circle cx="60" cy="60" r="56" fill="none" stroke="var(--mark)" stroke-width="3"/>'
            f'<circle cx="60" cy="60" r="43" fill="none" stroke="var(--mark)" stroke-width="1.2"/>'
            f'<path id="ring-{uid}" d="M60 60m-49.5 0a49.5 49.5 0 1 1 99 0a49.5 49.5 0 1 1-99 0" fill="none"/>'
            f'<text fill="var(--mark)" font-family="{SANS}" font-weight="700" font-size="7.4" letter-spacing="1.6">'
            f'<textPath href="#ring-{uid}" textLength="300" lengthAdjust="spacing">{RING_TEXT}</textPath></text>')


def b_center(wb=8):
    h1, h2 = 42, 68
    th, mh = wb * 0.75, wb * 0.6
    r = []
    for c in (h1, h2):
        r += [(c - wb / 2, 38, wb, 44), (c - wb / 2 - 4, 38, wb + 8, 3.5), (c - wb / 2 - 4, 78.5, wb + 8, 3.5)]
    arm0 = h2 + wb / 2 - 0.5
    r += [(arm0, 38, 88 - arm0, th), (85, 38, 3.5, th + 5), (arm0, 57, 83 - arm0, mh), (81, 54, 2.5, mh + 6)]
    rects = "".join(f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}"/>' for x, y, w, h in r)
    star = '<path d="M60 22.5l1.6 3.2 3.5.5-2.55 2.5.6 3.5L60 30.5l-3.15 1.7.6-3.5-2.55-2.5 3.5-.5Z"/>'
    gold = f'<rect x="{n(h1 + wb / 2)}" y="57" width="{n(h2 - h1 - wb)}" height="{n(mh)}"/>'
    return f'<g fill="var(--mark)">{rects}</g><g fill="var(--accent)">{gold}{star}</g>'


def b_seal(uid, wb=8):
    return seal_ring(uid) + b_center(wb)


# ── 새 방향 D / E / F ────────────────────────────────────────────────
NEW = {
    "D": {
        "title": "Seal × Flip", "ko": "인장 속 모노그램 (리믹스)",
        "story": "B 인장의 고리 안에 A 모노그램을 그대로 넣었어요. 고르신 'B 인장 + A 모노그램' 두 로고가 "
                 "한 가족처럼 보이도록 이어주는 리믹스입니다. 공문에서는 인장 전체, 웹에서는 가운데 A 만 떼어 쓰면 돼요.",
        "good": "2단 체계가 완벽히 통일됨 · 인장과 모노그램을 따로 관리할 필요 없음",
        "watch": "B 의 고전적인 세리프 HF 가 주던 '전통미'는 조금 줄어듦",
        "svg": lambda uid: seal_ring(uid) + placed(a_mark(), 60, 61, 0.56),
    },
    "E": {
        "title": "Page Tile", "ko": "넘어가는 페이지 타일",
        "story": "로고 전체가 '한 장의 페이지'예요. 남색 타일의 오른쪽 위 모서리가 골드로 접혀 넘어가고, "
                 "그 위에 흰색 HF 가 새겨져 있습니다. 그 자체로 앱 아이콘·유튜브 프로필이 되는 형태예요.",
        "good": "SNS 프로필·앱 아이콘·영상 워터마크에 바로 사용 · 작은 크기에서도 덩어리감이 큼",
        "watch": "격식 있는 문서에는 B·D 인장보다 캐주얼해 보일 수 있음",
        "svg": lambda uid: ('<path fill="var(--mark)" d="M18 8H86L112 34V102A10 10 0 0 1 102 112H18A10 10 0 0 1 8 102V18A10 10 0 0 1 18 8Z"/>'
                            '<path fill="var(--accent)" d="M86 8V34H112Z"/>'
                            + placed(a_mark(fold=False).replace("var(--mark)", "var(--knock)"), 57, 63, 0.62)),
    },
    "F": {
        "title": "Arch Gate", "ko": "캠퍼스 아치",
        "story": "대학 건물의 아치형 문 안에 HF 가 서 있어요. '배움의 문을 연다'는 뜻이고, 아치는 요즘 대학·교육 브랜드에서 "
                 "많이 쓰는 전통+현대의 상징이에요. 접힌 골드 모서리는 A 와 같은 언어로 유지했습니다.",
        "good": "캠퍼스·공간(스튜디오) 이미지와 잘 맞음 · 세로형이라 배너·사이니지에 강함",
        "watch": "가로 공간이 좁은 곳(헤더)에서는 작아 보일 수 있음",
        "svg": lambda uid: ('<path fill="none" stroke="var(--mark)" stroke-width="5" d="M26 106V56A34 34 0 0 1 94 56V106"/>'
                            '<rect fill="var(--mark)" x="14" y="104" width="92" height="5"/>'
                            + placed(a_mark(), 60, 76, 0.5)),
    },
}

_uid = [0]


def svg(inner_fn, cls="", size=None):
    _uid[0] += 1
    st = f' style="width:{size}px;height:{size}px"' if size else ""
    return f'<svg class="sym {cls}" viewBox="0 0 120 120"{st} aria-hidden="true">{inner_fn(f"u{_uid[0]}")}</svg>'


def variant_card(label, sub, fn):
    return (f'<figure class="var"><div class="var-big">{svg(fn, "vbig")}</div>'
            f'<div class="var-small">{svg(fn, size=32)}{svg(fn, size=16)}</div>'
            f'<figcaption><b>{label}</b><span>{sub}</span></figcaption></figure>')


def new_section(c, d):
    fn = d["svg"]
    return f"""
<section class="concept" id="concept-{c}">
  <header class="c-head"><span class="c-tag">시안 {c}</span><h2>{d['title']} <small>{d['ko']}</small></h2></header>
  <div class="grid">
    <div class="tile hero-tile">{svg(fn, 'big')}</div>
    <div class="tile navy">{svg(fn, 'mid')}</div>
    <div class="tile ivory mono">{svg(fn, 'mid')}</div>
    <div class="tile lockup">{svg(fn, 'lock')}
      <div class="wm"><b>HY FLIP</b><span class="en">FLIPPED LEARNING CONTENT LAB</span><span class="ko">한양 플립러닝 콘텐츠 개발 사업</span></div></div>
    <div class="tile appicon-wrap"><div class="appicon">{svg(fn, 'app')}</div><span>앱·SNS 프로필</span></div>
    <div class="tile tinies">{''.join(f'<figure class="tiny"><div class="tiny-box">{svg(fn, size=s)}</div><figcaption>{s}px</figcaption></figure>' for s in (16, 32, 64))}</div>
    <div class="tile lockup navy">{svg(fn, 'lock')}
      <div class="wm"><b style="color:#fff">HY FLIP</b><span class="en">FLIPPED LEARNING CONTENT LAB</span><span class="ko" style="color:#C9D6E8">한양 플립러닝 콘텐츠 개발 사업</span></div></div>
  </div>
  <div class="explain">
    <div><h3>이 로고의 이야기</h3><p>{d['story']}</p></div>
    <div><h3>👍 잘 맞는 곳</h3><p>{d['good']}</p></div>
    <div><h3>⚠️ 주의할 점</h3><p>{d['watch']}</p></div>
  </div>
</section>"""


def system_preview(seal_fn, seal_name):
    a = lambda uid: a_mark()
    return f"""
<div class="sys">
  <div class="sys-label">{seal_name}</div>
  <div class="paper">
    <div class="paper-head">{svg(seal_fn, size=78)}
      <div><div class="p-title">HY FLIP 플립러닝 콘텐츠 개발 사업</div><div class="p-sub">FLIPPED LEARNING CONTENT LAB · 공문 / 수료증 / 명판</div></div></div>
    <div class="lines"><i></i><i></i><i style="width:70%"></i><i></i><i style="width:55%"></i></div>
  </div>
  <div class="webbar">
    <div class="wb-logo">{svg(a, size=34)}<b>HY FLIP</b></div>
    <nav>사업소개 · 제작절차 · 스튜디오 · 공지</nav><span class="wb-cta">제작신청</span>
  </div>
  <div class="thumb">
    <div class="thumb-img"></div>
    <div class="thumb-badge">{svg(a, size=26)}</div>
    <span>영상 워터마크 · 썸네일</span>
  </div>
</div>"""


def board():
    weights = "".join(variant_card(lbl, sub, (lambda w, t, f: lambda uid: a_mark(w=w, t=t, f=f))(w, t, f))
                      for lbl, sub, w, t, f in [("Light", "기둥 11 · 우아함", 11, 9, 9),
                                                ("Regular", "기둥 16 · 1차 시안", 16, 14, 10),
                                                ("Bold", "기둥 21 · 힘 있음", 21, 18, 11)])
    ratios = "".join(variant_card(lbl, sub, (lambda c1, c2, R: lambda uid: a_mark(c1=c1, c2=c2, R=R))(c1, c2, R))
                     for lbl, sub, c1, c2, R in [("Condensed", "좁게 · 세로 강조", 34, 68, 96),
                                                 ("Regular", "1차 시안", 30, 70, 104),
                                                 ("Wide", "넓게 · 가로 안정", 24, 72, 106)])
    seals = "".join(variant_card(lbl, sub, (lambda wb: lambda uid: b_seal(uid, wb))(wb))
                    for lbl, sub, wb in [("Light", "가는 세리프 · 클래식", 6), ("Regular", "1차 시안", 8),
                                         ("Bold", "굵은 세리프 · 또렷함", 10.5)])
    news = "".join(new_section(c, d) for c, d in NEW.items())
    systems = (system_preview(lambda uid: b_seal(uid), "B 인장 + A 모노그램 (선택하신 조합)")
               + system_preview(NEW["D"]["svg"], "D 인장 속 모노그램 + A 모노그램 (리믹스 대안)"))
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>HY FLIP 로고 2차</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&family=Noto+Serif+KR:wght@700;900&display=swap" rel="stylesheet">
<style>
:root{{--navy:{NAVY};--deep:{DEEP};--gold:{GOLD};--ivory:{IVORY};--ink:#1A2233;--muted:#5B6475;--line:#E3E6EC;
  --sans:'Noto Sans KR',system-ui,sans-serif;--serif:'Noto Serif KR',Georgia,serif;--mark:var(--navy);--accent:var(--gold);--knock:#fff}}
*{{box-sizing:border-box;margin:0}}
body{{background:#fff;color:var(--ink);font-family:var(--sans);line-height:1.7;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1200px;margin:0 auto;padding:0 48px}}
.top{{border-bottom:1px solid var(--line);padding:56px 0 40px}}
.eyebrow{{font-size:12px;font-weight:700;letter-spacing:.18em;color:var(--gold)}}
h1{{font-family:var(--serif);font-size:44px;line-height:1.25;color:var(--deep);margin:10px 0 14px}}
.lead{{color:var(--muted);max-width:760px}}
.toc{{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}} .toc a{{border:1px solid var(--line);padding:6px 12px;font-size:14px;border-radius:2px;color:var(--navy);text-decoration:none;font-weight:500}}
.block{{padding:80px 0;border-bottom:1px solid var(--line)}}
h2{{font-family:var(--serif);font-size:34px;color:var(--deep)}} h2 small{{font-family:var(--sans);font-size:16px;color:var(--muted);font-weight:500;margin-left:6px}}
.desc{{color:var(--muted);margin:8px 0 28px;max-width:760px}}
h3.row-t{{font-size:15px;color:var(--navy);margin:28px 0 12px}}
.vars{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
.var{{border:1px solid var(--line);border-radius:4px;margin:0;padding:20px;display:flex;flex-direction:column;gap:14px}}
.var-big{{aspect-ratio:1.4;padding:10px;display:flex;align-items:center;justify-content:center;background:#fff}}
.sym.vbig{{height:100%;width:auto;max-width:100%}}
.var-small{{display:flex;gap:16px;align-items:center;justify-content:center;border-top:1px solid var(--line);padding-top:14px}}
.var figcaption{{display:flex;justify-content:space-between;font-size:14px}} .var figcaption span{{color:var(--muted)}}
.concept{{padding:80px 0;border-bottom:1px solid var(--line)}}
.c-head{{display:flex;align-items:baseline;gap:16px;margin-bottom:28px;flex-wrap:wrap}}
.c-tag{{background:var(--navy);color:#fff;font-size:13px;font-weight:700;padding:4px 10px;border-radius:2px;letter-spacing:.06em}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:200px;gap:16px}}
.tile{{border:1px solid var(--line);border-radius:4px;display:flex;align-items:center;justify-content:center;background:#fff}}
.hero-tile{{grid-row:span 2;grid-column:span 2}}
.navy{{background:var(--navy);border-color:var(--navy);--mark:#fff;--accent:var(--gold);--knock:var(--navy)}}
.ivory{{background:var(--ivory)}} .mono{{--mark:#111;--accent:#111;--knock:var(--ivory)}}
.sym.big{{width:62%;height:62%}} .sym.mid{{width:58%;height:58%}}
.lockup{{grid-column:span 2;gap:20px;padding:0 28px;justify-content:flex-start}}
.sym.lock{{width:104px;height:104px;flex:none}}
.wm{{display:flex;flex-direction:column;line-height:1.2}}
.wm b{{font-size:44px;font-weight:800;letter-spacing:.06em;color:var(--navy)}}
.wm .en{{font-size:11px;font-weight:700;letter-spacing:.24em;color:var(--gold);margin-top:8px}}
.wm .ko{{font-size:13px;color:var(--muted);margin-top:6px}}
.appicon-wrap{{flex-direction:column;gap:10px;font-size:13px;color:var(--muted)}}
.appicon{{width:96px;height:96px;border-radius:22px;background:var(--navy);display:flex;align-items:center;justify-content:center;--mark:#fff;--accent:var(--gold);--knock:var(--navy)}}
.sym.app{{width:64px;height:64px}}
.tinies{{gap:22px}} .tiny{{text-align:center;font-size:12px;color:var(--muted);margin:0}}
.tiny-box{{height:72px;display:flex;align-items:center;justify-content:center}}
.explain{{display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:32px;margin-top:32px}}
.explain h3{{font-size:15px;color:var(--navy);margin:0 0 6px}} .explain p{{font-size:15px;color:#3a4356}}
.sys{{display:grid;grid-template-columns:1.1fr 1fr;grid-template-rows:auto auto;gap:16px;margin-bottom:40px}}
.sys-label{{grid-column:1/-1;font-weight:700;color:var(--navy)}}
.paper{{grid-row:span 2;border:1px solid var(--line);background:var(--ivory);padding:32px;border-radius:4px}}
.paper-head{{display:flex;gap:18px;align-items:center;border-bottom:2px solid var(--navy);padding-bottom:18px}}
.p-title{{font-family:var(--serif);font-size:20px;color:var(--deep)}} .p-sub{{font-size:11px;letter-spacing:.14em;color:var(--gold);font-weight:700}}
.lines{{display:flex;flex-direction:column;gap:12px;margin-top:24px}} .lines i{{display:block;height:8px;background:#e2e5ea;border-radius:2px}}
.webbar{{border:1px solid var(--line);border-radius:4px;display:flex;align-items:center;gap:18px;padding:16px 20px;font-size:13px;flex-wrap:wrap}}
.wb-logo{{display:flex;align-items:center;gap:8px}} .wb-logo b{{font-size:20px;letter-spacing:.06em;color:var(--navy)}}
.webbar nav{{color:var(--muted);flex:1}} .wb-cta{{background:var(--gold);color:#fff;padding:6px 14px;border-radius:2px;font-weight:700}}
.thumb{{position:relative;border-radius:4px;overflow:hidden;min-height:170px;display:flex;align-items:flex-end;padding:12px;color:#fff;font-size:12px}}
.thumb-img{{position:absolute;inset:0;background:linear-gradient(120deg,#0A2E55,#1d5a96 60%,#3b6f9f)}}
.thumb span{{position:relative}} .thumb-badge{{position:absolute;top:12px;right:12px;--mark:#fff;opacity:.9}}
.note{{margin-top:12px;font-size:13px;color:var(--muted)}}
@media (max-width:860px){{
  .wrap{{padding:0 20px}} h1{{font-size:32px}} .block,.concept{{padding:56px 0}}
  .vars{{grid-template-columns:1fr}}
  .grid{{grid-template-columns:repeat(2,1fr);grid-auto-rows:150px}}
  .lockup{{padding:0 16px;gap:12px}} .sym.lock{{width:64px;height:64px}} .wm b{{font-size:30px}} .wm .en{{font-size:9px;letter-spacing:.16em}}
  .explain{{grid-template-columns:1fr;gap:12px}}
  .sys{{grid-template-columns:1fr}} .paper{{grid-row:auto;padding:20px}} .webbar nav{{display:none}}
}}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <div class="eyebrow">HY FLIP · LOGO ROUND 2</div>
  <h1>로고 2차 — 굵기·비율 조정 + 새 방향 3시안</h1>
  <p class="lead">1차에서 고르신 <b>B 인장 + A 모노그램</b> 조합을 기준으로 ① 글자 굵기 ② 가로세로 비율을 바꿔 보고,
  ③ 새로운 방향 3가지(D 리믹스 · E 페이지 타일 · F 캠퍼스 아치)를 더 만들었어요. 마지막에는 실제로 쓰일 때의 모습(공문·웹 헤더·영상)을 미리 보여드립니다.</p>
  <div class="toc"><a href="#weights">① 굵기</a><a href="#ratios">② 비율</a><a href="#concept-D">③ 새 방향 D·E·F</a><a href="#system">④ 2단 체계 미리보기</a></div>
</div></header>
<main class="wrap">
<section class="block" id="weights">
  <h2>① 글자 굵기 <small>Weight</small></h2>
  <p class="desc">굵기는 '목소리 크기'와 같아요. 가늘면 차분하고 우아하며, 굵으면 멀리서도 잘 보이고 힘이 있습니다. 아래 작은 크기(32·16px)에서 얼마나 또렷한지도 함께 보세요.</p>
  <h3 class="row-t">A 모노그램</h3><div class="vars">{weights}</div>
  <h3 class="row-t">B 인장 (가운데 HF)</h3><div class="vars">{seals}</div>
</section>
<section class="block" id="ratios">
  <h2>② 비율 <small>Proportion</small></h2>
  <p class="desc">두 기둥 사이 간격을 바꾼 변형이에요. 좁으면 세로로 곧고 단단해 보이고, 넓으면 안정적이고 여유 있어 보입니다.</p>
  <div class="vars">{ratios}</div>
</section>
{news}
<section class="block" id="system">
  <h2>④ 2단 체계 미리보기 <small>Seal + Monogram</small></h2>
  <p class="desc">격식 있는 곳(공문·수료증·명판)에는 인장을, 웹·영상에는 모노그램을 씁니다. 같은 자리에 두 조합을 놓아 비교해 보세요.</p>
  {systems}
  <p class="note">※ 제안용 시안이며 한양대학교 공식 교표·로고가 아닙니다.</p>
</section>
</main>
</body>
</html>
"""


def main():
    for c, d in NEW.items():
        (OUT / f"logo-{c}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="512" height="512" '
            f'style="--mark:{NAVY};--accent:{GOLD};--knock:#fff"><title>HY FLIP 시안 {c} — {d["title"]}</title>'
            f'{d["svg"](c + "-solo")}</svg>\n', encoding="utf-8")
    (OUT / "logo-board-r2.html").write_text(board(), encoding="utf-8")
    print("logo/logo-board-r2.html, logo-D/E/F.svg 생성 완료")


if __name__ == "__main__":
    main()
