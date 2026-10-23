"""HY FLIP 모노그램 3시안 → logo/*.svg + logo/logo-board.html 생성.

도형 정의는 여기 한 곳에만 있습니다. 모양을 고치면 이 파일을 다시 실행하세요.
  python scripts/build_logos.py
색은 두 변수로만 칠합니다: --mark(본체, 기본 남색) / --accent(포인트, 기본 골드).
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "logo"

NAVY, DEEP, GOLD, IVORY = "#0E4A84", "#0A2E55", "#C8A24A", "#F7F5F0"

# 120x120 격자. (본체 도형, 포인트 도형)
CONCEPTS = {
    "A": {
        "title": "Page Flip",
        "ko": "책장 넘기기",
        "story": "H의 오른쪽 기둥이 그대로 F의 기둥이 됩니다. F의 윗변 끝이 책장처럼 접혀 있어 "
                 "'교재를 넘기듯 수업을 뒤집는다'는 뜻을 담았어요. 가로획이 기둥을 사이에 두고 한 줄로 이어져 안정감이 있습니다.",
        "good": "가장 단순해서 작은 크기(파비콘)에서도 또렷함 · 웹·영상 자막 바에 잘 어울림",
        "watch": "접힌 모서리가 작아서 16px 에서는 거의 안 보임 (그래도 HF 는 읽힘)",
        # 한 덩어리 패스 (도형 사이 이음새 방지)
        "mark": '<path d="M22 20H38V52H62V20H94L104 30V36H78V52H98V66H78V100H62V66H38V100H22Z"/>',
        "accent": '<path d="M94 20V30H104Z"/>',
    },
    "B": {
        "title": "Academic Seal",
        "ko": "아카데믹 인장",
        "story": "대학 문서에 찍는 인장(씰) 형식입니다. 바깥 고리에 영문 사업명이 둥글게 돌고, 가운데에는 "
                 "끝에 받침(세리프)이 달린 고전적인 HF 가 들어가요. 두 글자를 잇는 가로획만 골드로 칠해 '연결'을 강조했습니다.",
        "good": "공문·수료증·명판처럼 격식 있는 곳에 강함 · 대학 사업이라는 신뢰감이 가장 큼",
        "watch": "원형 문구는 32px 이하에서 안 읽힘 → 작은 곳에는 가운데 HF 만 따로 사용",
        "mark": '<circle cx="60" cy="60" r="56" fill="none" stroke="var(--mark)" stroke-width="3"/>'
                '<circle cx="60" cy="60" r="43" fill="none" stroke="var(--mark)" stroke-width="1.2"/>'
                '<path id="ring-{id}" d="M60 60m-49.5 0a49.5 49.5 0 1 1 99 0a49.5 49.5 0 1 1-99 0" fill="none"/>'
                '<text font-family="\'Noto Sans KR\',Arial,sans-serif" font-weight="700" font-size="7.4" '
                'letter-spacing="1.6"><textPath href="#ring-{id}" startOffset="0" textLength="300" '
                'lengthAdjust="spacing">HY FLIP · FLIPPED LEARNING CONTENT LAB · EST. 2026 ·</textPath></text>'
                # H (세리프 포함)
                '<rect x="38" y="38" width="8" height="44"/><rect x="34" y="38" width="16" height="3.5"/>'
                '<rect x="34" y="78.5" width="16" height="3.5"/>'
                '<rect x="64" y="38" width="8" height="44"/><rect x="60" y="38" width="16" height="3.5"/>'
                '<rect x="60" y="78.5" width="16" height="3.5"/>'
                # F 팔
                '<rect x="70" y="38" width="18" height="6"/><rect x="85" y="38" width="3.5" height="11"/>'
                '<rect x="70" y="57" width="13" height="5"/><rect x="81" y="54" width="2.5" height="11"/>',
        "accent": '<rect x="46" y="57" width="18" height="5"/>'
                  '<path d="M60 22.5l1.6 3.2 3.5.5-2.55 2.5.6 3.5L60 30.5l-3.15 1.7.6-3.5-2.55-2.5 3.5-.5Z"/>',
    },
    "C": {
        "title": "Play Flip",
        "ko": "재생 버튼",
        "story": "H 의 가로획 자리에 영상의 '재생(▶)' 삼각형을 넣었어요. 왼쪽 기둥에서 출발한 삼각형이 오른쪽 기둥(=F 의 기둥)에 닿아 "
                 "'강의실 수업 → 영상 콘텐츠'로 넘어가는 흐름을 보여줍니다.",
        "good": "'영상 콘텐츠 사업'이라는 정체성이 한눈에 보임 · 유튜브 썸네일·영상 워터마크에 최적",
        "watch": "재생 버튼 모양은 흔해서, 반드시 HF 기둥과 함께 써야 고유성이 생김",
        "mark": '<rect x="20" y="20" width="16" height="80"/>'
                '<path d="M70 20H106V36H86V52H100V68H86V100H70Z"/>',
        "accent": '<path d="M36 40V80L70 60Z"/>',
    },
}


def symbol_body(c, uid):
    d = CONCEPTS[c]
    return (f'<g fill="var(--mark)">{d["mark"].replace("{id}", uid)}</g>'
            f'<g fill="var(--accent)">{d["accent"]}</g>')


def standalone_svg(c, mark=NAVY, accent=GOLD):
    body = symbol_body(c, f"{c}-solo")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="512" height="512" '
            f'style="--mark:{mark};--accent:{accent}">'
            f'<title>HY FLIP 모노그램 시안 {c} — {CONCEPTS[c]["title"]}</title>{body}</svg>\n')


def lockup_svg(c):
    serif = c == "B"
    family = "'Noto Serif KR',Georgia,serif" if serif else "'Noto Sans KR',Arial,sans-serif"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 120" width="920" height="240" '
            f'style="--mark:{NAVY};--accent:{GOLD}"><title>HY FLIP 가로 조합형 시안 {c}</title>'
            f'{symbol_body(c, c + "-lock")}'
            f'<text x="140" y="66" font-family="{family}" font-weight="800" font-size="46" letter-spacing="3" '
            f'fill="{NAVY}">HY FLIP</text>'
            f'<text x="142" y="88" font-family="\'Noto Sans KR\',Arial,sans-serif" font-weight="700" font-size="10.5" '
            f'letter-spacing="3.2" fill="{GOLD}">FLIPPED LEARNING CONTENT LAB</text>'
            f'<text x="142" y="106" font-family="\'Noto Sans KR\',Arial,sans-serif" font-weight="500" font-size="11" '
            f'letter-spacing="1" fill="#5B6475">한양 플립러닝 콘텐츠 개발 사업</text></svg>\n')


def board_html():
    def use(c, cls="", size=None):
        st = f' style="width:{size}px;height:{size}px"' if size else ""
        return f'<svg class="sym {cls}" viewBox="0 0 120 120"{st} aria-hidden="true">{symbol_body(c, c + uid())}</svg>'

    counter = [0]

    def uid():
        counter[0] += 1
        return f"-{counter[0]}"

    sections = []
    for c, d in CONCEPTS.items():
        family = "var(--serif)" if c == "B" else "var(--sans)"
        sizes = "".join(
            f'<figure class="tiny"><div class="tiny-box">{use(c, size=s)}</div><figcaption>{s}px</figcaption></figure>'
            for s in (16, 32, 64))
        sections.append(f"""
<section class="concept" id="concept-{c}">
  <header class="c-head">
    <span class="c-tag">시안 {c}</span>
    <h2>{d['title']} <small>{d['ko']}</small></h2>
  </header>
  <div class="grid">
    <div class="tile hero-tile">{use(c, 'big')}</div>
    <div class="tile navy">{use(c, 'mid')}</div>
    <div class="tile ivory mono">{use(c, 'mid')}</div>
    <div class="tile lockup">
      {use(c, 'lock')}
      <div class="wm"><b style="font-family:{family}">HY FLIP</b>
        <span class="en">FLIPPED LEARNING CONTENT LAB</span>
        <span class="ko">한양 플립러닝 콘텐츠 개발 사업</span></div>
    </div>
    <div class="tile appicon-wrap"><div class="appicon">{use(c, 'app')}</div><span>앱·SNS 프로필</span></div>
    <div class="tile tinies">{sizes}</div>
    <div class="tile lockup navy">
      {use(c, 'lock')}
      <div class="wm"><b style="font-family:{family};color:#fff">HY FLIP</b>
        <span class="en">FLIPPED LEARNING CONTENT LAB</span>
        <span class="ko" style="color:#C9D6E8">한양 플립러닝 콘텐츠 개발 사업</span></div>
    </div>
  </div>
  <div class="explain">
    <div><h3>이 로고의 이야기</h3><p>{d['story']}</p></div>
    <div><h3>👍 잘 맞는 곳</h3><p>{d['good']}</p><h3>⚠️ 주의할 점</h3><p>{d['watch']}</p></div>
    <figure class="mock">
      <img src="../assets/mock-plaque-{c}.png" alt="시안 {c} 황동 명판 실사 목업"
           onerror="this.replaceWith(Object.assign(document.createElement('div'),{{className:'mock-ph',innerHTML:'GPT 실사 목업 자리<br><small>황동 명판 · gpt-image-2</small>'}}))">
      <figcaption>실사 목업 (GPT 이미지)</figcaption>
    </figure>
  </div>
</section>""")

    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>HY FLIP 로고 시안</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&family=Noto+Serif+KR:wght@700;900&display=swap" rel="stylesheet">
<style>
:root{{--navy:{NAVY};--deep:{DEEP};--gold:{GOLD};--ivory:{IVORY};--ink:#1A2233;--muted:#5B6475;--line:#E3E6EC;
  --sans:'Noto Sans KR',system-ui,sans-serif;--serif:'Noto Serif KR',Georgia,serif;--mark:var(--navy);--accent:var(--gold)}}
*{{box-sizing:border-box;margin:0}}
body{{background:#fff;color:var(--ink);font-family:var(--sans);line-height:1.7;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1200px;margin:0 auto;padding:0 48px}}
.top{{border-bottom:1px solid var(--line);padding:56px 0 40px}}
.eyebrow{{font-size:12px;font-weight:700;letter-spacing:.18em;color:var(--gold)}}
h1{{font-family:var(--serif);font-size:44px;line-height:1.25;color:var(--deep);margin:10px 0 14px}}
.lead{{color:var(--muted);max-width:720px}}
.how{{display:flex;gap:12px;flex-wrap:wrap;margin-top:22px}}
.how span{{border:1px solid var(--line);padding:6px 12px;font-size:14px;border-radius:2px}}
.how b{{color:var(--navy)}}
.concept{{padding:88px 0;border-bottom:1px solid var(--line)}}
.c-head{{display:flex;align-items:baseline;gap:16px;margin-bottom:28px}}
.c-tag{{background:var(--navy);color:#fff;font-size:13px;font-weight:700;padding:4px 10px;border-radius:2px;letter-spacing:.06em}}
h2{{font-family:var(--serif);font-size:34px;color:var(--deep)}} h2 small{{font-family:var(--sans);font-size:16px;color:var(--muted);font-weight:500;margin-left:6px}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:200px;gap:16px}}
.tile{{border:1px solid var(--line);border-radius:4px;display:flex;align-items:center;justify-content:center;background:#fff}}
.hero-tile{{grid-row:span 2;grid-column:span 2}}
.navy{{background:var(--navy);border-color:var(--navy);--mark:#fff;--accent:var(--gold)}}
.ivory{{background:var(--ivory)}} .mono{{--mark:#111;--accent:#111}}
.sym.big{{width:62%;height:62%}} .sym.mid{{width:58%;height:58%}}
.lockup{{grid-column:span 2;gap:20px;padding:0 28px;justify-content:flex-start}}
.sym.lock{{width:104px;height:104px;flex:none}}
.wm{{display:flex;flex-direction:column;line-height:1.2}}
.wm b{{font-size:44px;font-weight:800;letter-spacing:.06em;color:var(--navy)}}
.wm .en{{font-size:11px;font-weight:700;letter-spacing:.24em;color:var(--gold);margin-top:8px}}
.wm .ko{{font-size:13px;color:var(--muted);margin-top:6px}}
.appicon-wrap{{flex-direction:column;gap:10px;font-size:13px;color:var(--muted)}}
.appicon{{width:96px;height:96px;border-radius:22px;background:var(--navy);display:flex;align-items:center;justify-content:center;--mark:#fff;--accent:var(--gold)}}
.sym.app{{width:64px;height:64px}}
.tinies{{gap:22px}} .navy.lockup{{justify-content:flex-start}} .tiny{{text-align:center;font-size:12px;color:var(--muted)}}
.tiny-box{{height:72px;display:flex;align-items:center;justify-content:center}}
.explain{{display:grid;grid-template-columns:1.2fr 1fr 1.1fr;gap:32px;margin-top:36px}}
h3{{font-size:15px;color:var(--navy);margin:0 0 6px}} .explain p{{font-size:15px;color:#3a4356;margin-bottom:14px}}
.mock{{margin:0}} .mock img,.mock-ph{{width:100%;aspect-ratio:3/2;object-fit:cover;border-radius:4px;display:block}}
.mock-ph{{background:repeating-linear-gradient(135deg,#eef1f6 0 12px,#f6f8fb 12px 24px);border:1px dashed #b9c3d3;display:flex;
  flex-direction:column;align-items:center;justify-content:center;color:var(--muted);font-size:14px;text-align:center}}
.mock figcaption{{font-size:12px;color:var(--muted);margin-top:6px}}
.compare{{padding:88px 0 120px}}
table{{width:100%;border-collapse:collapse;font-size:15px}} th,td{{border-bottom:1px solid var(--line);padding:14px 10px;text-align:left}}
th{{color:var(--muted);font-weight:500;font-size:13px}} td b{{color:var(--navy)}}
.stars{{color:var(--gold);letter-spacing:2px}}
.note{{margin-top:24px;font-size:13px;color:var(--muted)}}
@media (max-width:860px){{
  .wrap{{padding:0 20px}} h1{{font-size:32px}} .concept{{padding:64px 0}}
  .grid{{grid-template-columns:repeat(2,1fr);grid-auto-rows:150px}}
  .lockup{{grid-column:span 2;padding:0 16px;gap:12px}} .sym.lock{{width:64px;height:64px}} .wm b{{font-size:30px}}
  .wm .en{{font-size:9px;letter-spacing:.16em}}
  .explain{{grid-template-columns:1fr;gap:12px}}
  .table-scroll{{overflow-x:auto}} table{{min-width:560px}}
}}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <div class="eyebrow">HY FLIP · LOGO ROUND 1</div>
  <h1>HY FLIP 모노그램 로고 — 시안 3종</h1>
  <p class="lead">H 와 F 를 하나로 엮은 이니셜 로고예요. 세 시안 모두 <b>H 의 오른쪽 기둥 = F 의 기둥</b> 구조를 공유하고,
  골드는 딱 한 곳에만 씁니다. 각 시안은 흰 바탕 · 남색 반전 · 흑백 · 가로 조합 · 앱 아이콘 · 작은 크기로 시험했어요.</p>
  <div class="how"><span>고르는 법 ① <b>16px 에서도 HF 가 보이나요?</b></span><span>② <b>남색 바탕에서도 고급스러운가요?</b></span>
  <span>③ <b>교수님이 3초 안에 '대학·영상·뒤집기'를 떠올리나요?</b></span></div>
</div></header>
<main class="wrap">
{''.join(sections)}
<section class="compare">
  <h2>한눈에 비교</h2>
  <div class="table-scroll"><table>
    <tr><th>기준</th><th>A Page Flip</th><th>B Academic Seal</th><th>C Play Flip</th></tr>
    <tr><td>대학다운 신뢰감</td><td class="stars">★★★★☆</td><td class="stars">★★★★★</td><td class="stars">★★★☆☆</td></tr>
    <tr><td>영상 콘텐츠 느낌</td><td class="stars">★★★☆☆</td><td class="stars">★★☆☆☆</td><td class="stars">★★★★★</td></tr>
    <tr><td>작은 크기 가독성</td><td class="stars">★★★★★</td><td class="stars">★★★☆☆</td><td class="stars">★★★★☆</td></tr>
    <tr><td>추천 용도</td><td>웹 · 자막바 · 범용</td><td>공문 · 수료증 · 명판</td><td>유튜브 · 썸네일 · SNS</td></tr>
  </table></div>
  <p class="note">💡 조합도 가능해요: 예) <b>B 인장(공식 문서용) + A 또는 C 모노그램(웹·영상용)</b> 2단 체계.
  ※ 제안용 시안이며 한양대학교 공식 교표·로고가 아닙니다.</p>
</section>
</main>
</body>
</html>
"""


def main():
    OUT.mkdir(exist_ok=True)
    for c in CONCEPTS:
        (OUT / f"logo-{c}.svg").write_text(standalone_svg(c), encoding="utf-8")
        (OUT / f"logo-{c}-reverse.svg").write_text(standalone_svg(c, "#FFFFFF", GOLD), encoding="utf-8")
        (OUT / f"logo-{c}-lockup.svg").write_text(lockup_svg(c), encoding="utf-8")
    (OUT / "logo-board.html").write_text(board_html(), encoding="utf-8")
    print("logo/ 생성 완료:", ", ".join(sorted(p.name for p in OUT.glob("*.*"))))


if __name__ == "__main__":
    main()
