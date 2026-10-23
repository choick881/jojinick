"""GPT 실사 이미지 갤러리 → assets/gallery.html

manifest 의 16장을 한 페이지에서 확인합니다. 아직 없는 사진은 자리표시로 보여요.
  python scripts/build_gallery.py
"""

import html
import json
from pathlib import Path

from site_kit import head, logo

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

CSS = """
:root{--navy:#0E4A84;--deep:#0A2E55;--gold:#C8A24A;--ink:#1A2233;--muted:#5B6475;--line:#E3E6EC;--ivory:#F7F5F0}
*{box-sizing:border-box;margin:0}
body{background:var(--ivory);color:var(--ink);font:400 15px/1.7 'Noto Sans KR',system-ui,sans-serif;word-break:keep-all}
.w{max-width:1280px;margin:0 auto;padding:0 40px}
header{background:var(--deep);color:#fff;padding:40px 0;--mark:#fff;--accent:var(--gold)}
header .w{display:flex;align-items:center;gap:18px;flex-wrap:wrap}
h1{font:900 30px/1.3 'Noto Serif KR',serif} header p{color:#b9c8dc;font-size:14px}
.count{margin-left:auto;font:700 14px/1 'Noto Sans KR';background:rgba(255,255,255,.1);padding:10px 14px;border-radius:2px}
.count b{color:#E2C77F}
main{padding:40px 0 80px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
figure{background:#fff;border:1px solid var(--line);margin:0}
figure .ph{aspect-ratio:3/2}
figcaption{padding:14px 16px 16px}
figcaption b{display:block;font-size:15px} figcaption .meta{font-size:12px;color:var(--muted)}
.st{display:inline-block;font:700 11px/1 'Noto Sans KR';padding:4px 7px;border-radius:2px;margin-right:6px;vertical-align:1px}
.st.ok{background:#E6F2EA;color:#1E6B3A} .st.no{background:#F3F0E6;color:#8A6D1E}
details{margin-top:8px;font-size:12px;color:var(--muted)} summary{cursor:pointer;color:var(--navy)}
@media (max-width:900px){.w{padding:0 20px}.grid{grid-template-columns:1fr 1fr;gap:12px}}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
"""


def main():
    items = json.loads((ASSETS / "manifest.json").read_text(encoding="utf-8"))
    made = sum((ASSETS / it["file"]).exists() for it in items)
    cards = []
    for it in items:
        ok = (ASSETS / it["file"]).exists()
        w, h = (int(x) for x in it.get("size", "1536x1024").split("x"))
        bg = f' style="background-image:url({it["file"]})"' if ok else ""
        st = '<span class="st ok">완료</span>' if ok else '<span class="st no">대기</span>'
        ref = f" · 참고: {it['ref']}" if it.get("ref") else ""
        cards.append(
            f'<figure>'
            f'<div class="ph{" has-img" if ok else ""}" data-label="대기 · {it["name"]}"{bg}></div>'
            f'<figcaption>{st}<b style="display:inline">{it["name"]}</b>'
            f'<div class="meta">{html.escape(it["use"])} · {w}×{h}{ref}<br>{html.escape(it.get("generator", ""))}</div>'
            f'<details><summary>프롬프트 보기</summary>{html.escape(it["prompt"])}</details></figcaption></figure>')
    page = head("HY FLIP 이미지 갤러리", CSS) + f"""<body>
<header><div class="w">{logo('seal', 52)}<div><h1>GPT 실사 이미지 갤러리</h1>
<p>GPT 이미지 모델(gpt-image-2.5, Figma 경유) · 로고 목업은 빈 배경 + 확정 로고 합성 · 페이지의 자리표시에 자동으로 들어가는 사진들</p></div>
<span class="count">완료 <b>{made}</b> / {len(items)}</span></div></header>
<main><div class="w grid">{''.join(cards)}</div></main>
</body></html>
"""
    (ASSETS / "gallery.html").write_text(page, encoding="utf-8")
    print(f"assets/gallery.html (완료 {made}/{len(items)})")


if __name__ == "__main__":
    main()
