"""온담찬 확정 로고 SVG 생성기.

글자는 서체 윤곽선(path)으로 바꿔 넣는다. 서체가 없는 컴퓨터·인쇄소에서도 모양이 같다.
실행: python3 brand/logo/src/build.py  (필요: pip install fonttools)
서체: Noto Serif KR Black / Noto Sans KR Bold, '온담찬 ONDAMCH' 글자만 담은 부분 파일 (SIL OFL 1.1)
"""
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

SRC = Path(__file__).resolve().parent
OUT = SRC.parent

BROWN = "#7A4E2D"   # 된장 갈색
ACCENT = "#C8462B"  # 고추 주홍
CREAM = "#FBF6EC"   # 크림
INK = "#2B211A"     # 먹

SERIF = TTFont(SRC / "NotoSerifKR-Black-subset.ttf")
SANS = TTFont(SRC / "NotoSansKR-Bold-subset.ttf")


def _layout(font, text, size, tracking):
    """글자별 (글리프 이름, x 위치)와 전체 폭을 돌려준다."""
    cmap, hmtx = font.getBestCmap(), font["hmtx"]
    scale = size / font["head"].unitsPerEm
    x, items = 0.0, []
    for i, ch in enumerate(text):
        name = cmap[ord(ch)]
        items.append((name, x))
        x += hmtx[name][0] * scale + (tracking if i < len(text) - 1 else 0)
    return items, x, scale


def text_bounds(font, text, size, tracking=0.0):
    """기준선 (0,0)에서 그렸을 때 위아래 범위 (윗쪽은 음수)."""
    items, width, scale = _layout(font, text, size, tracking)
    gs = font.getGlyphSet()
    top, bottom = 0.0, 0.0
    for name, _ in items:
        bp = BoundsPen(gs)
        gs[name].draw(bp)
        if bp.bounds:
            top = min(top, -bp.bounds[3] * scale)
            bottom = max(bottom, -bp.bounds[1] * scale)
    return width, top, bottom


def text_path(font, text, size, x, baseline, anchor="start", tracking=0.0):
    items, width, scale = _layout(font, text, size, tracking)
    if anchor == "middle":
        x -= width / 2
    gs = font.getGlyphSet()
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    for name, gx in items:
        gs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x + gx, baseline)))
    return pen.getCommands()


# ── 심볼 (64×64 격자) ─────────────────────────────────────────────
def sym_a(main, accent, uid):
    """A: 김 오르는 밥그릇. 그릇의 띠는 마스크로 뚫어 어떤 바탕에서도 바탕색이 비친다."""
    return f"""<mask id="band-{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="64" height="64">
    <rect width="64" height="64" fill="#fff"/>
    <path d="M13.5 39.5H50.5" stroke="#000" stroke-width="2.2" stroke-linecap="round"/>
  </mask>
  <g mask="url(#band-{uid})">
    <path d="M8 33H56C56 45.5 45.3 54 32 54S8 45.5 8 33Z" fill="{main}"/>
  </g>
  <rect x="23" y="55.5" width="18" height="4.5" rx="2.25" fill="{main}"/>
  <path d="M21 27c-3.6-3.6 3.6-6.8 0-11.5M43 27c-3.6-3.6 3.6-6.8 0-11.5" fill="none" stroke="{main}" stroke-width="3.8" stroke-linecap="round"/>
  <path d="M32 26c-4.2-4.2 4.2-7.8 0-13.5" fill="none" stroke="{accent}" stroke-width="3.8" stroke-linecap="round"/>"""


def sym_c(main, accent):
    """C: 두 손이 받친 김 오르는 그릇."""
    return f"""<path d="M16 33H48C48 41.8 40.8 48 32 48S16 41.8 16 33Z" fill="{main}"/>
  <path d="M6 37C6.6 49.6 16.6 58.4 29.6 59V54.4C20 53.8 12.6 47.8 11.2 37.6C10.7 35.2 6 34.8 6 37Z" fill="{main}"/>
  <path d="M58 37C57.4 49.6 47.4 58.4 34.4 59V54.4C44 53.8 51.4 47.8 52.8 37.6C53.3 35.2 58 34.8 58 37Z" fill="{main}"/>
  <path d="M23 26.5c-3.2-3.2 3.2-6 0-10M41 26.5c-3.2-3.2 3.2-6 0-10" fill="none" stroke="{main}" stroke-width="3.6" stroke-linecap="round"/>
  <path d="M32 25.5c-3.8-3.8 3.8-7 0-12" fill="none" stroke="{accent}" stroke-width="3.6" stroke-linecap="round"/>"""


def svg(view_w, view_h, body, width=None, height=None, title="온담찬"):
    w = width or view_w
    h = height or view_h
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_w} {view_h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{title}">\n  <title>{title}</title>\n  {body}\n</svg>\n')


# ── 기본 로고: C 원형 엠블럼 (120×120) ─────────────────────────────
def emblem(main, accent, disc):
    fill = f'fill="{disc}"' if disc else 'fill="none"'
    return f"""<circle cx="60" cy="60" r="56" {fill} stroke="{main}" stroke-width="5"/>
  <circle cx="60" cy="60" r="48.5" fill="none" stroke="{main}" stroke-width="1.2"/>
  <g transform="translate(37 17) scale(0.71875)">
  {sym_c(main, accent)}
  </g>
  <path d="{text_path(SERIF, "온담찬", 19, 60, 84, "middle", 0.5)}" fill="{main}"/>
  <path d="{text_path(SANS, "ONDAMCHAN", 5.8, 60, 96, "middle", 1.6)}" fill="{main}"/>
  <circle cx="30" cy="94" r="1.5" fill="{accent}"/>
  <circle cx="90" cy="94" r="1.5" fill="{accent}"/>"""


# ── 가로형: A 심볼 + 글자 ─────────────────────────────────────────
H_SIZE = 60
_h_w, _h_top, _h_bot = text_bounds(SERIF, "온담찬", H_SIZE)
H_BASE = 46 - (_h_top + _h_bot) / 2           # 글자 가운데를 그릇+김 가운데(약 46)에 맞춤
H_TEXT_X = 86
H_W = round(H_TEXT_X + _h_w + 4)


def horizontal(main, accent, uid):
    return f"""<g transform="scale(1.25)">
  {sym_a(main, accent, uid)}
  </g>
  <path d="{text_path(SERIF, "온담찬", H_SIZE, H_TEXT_X, H_BASE)}" fill="{main}"/>"""


# ── 작은 심볼: 원 + C 심볼 (64×64) ─────────────────────────────────
def symbol(main, accent, disc):
    fill = f'fill="{disc}"' if disc else 'fill="none"'
    return f"""<circle cx="32" cy="32" r="29.5" {fill} stroke="{main}" stroke-width="4"/>
  <g transform="translate(12 10) scale(0.625)">
  {sym_c(main, accent)}
  </g>"""


def favicon():
    """16·32px용: 꽉 찬 갈색 원 + 크림 심볼(작을수록 면이 굵어야 읽힌다)."""
    return f"""<circle cx="32" cy="32" r="32" fill="{BROWN}"/>
  <g transform="translate(9 7) scale(0.71875)">
  {sym_c(CREAM, CREAM)}
  </g>"""


FILES = {
    "logo.svg": svg(120, 120, emblem(BROWN, ACCENT, CREAM), 480, 480),
    "logo-reverse.svg": svg(120, 120, emblem(CREAM, CREAM, None), 480, 480),
    "logo-mono.svg": svg(120, 120, emblem(INK, INK, None), 480, 480),
    "logo-horizontal.svg": svg(H_W, 80, horizontal(BROWN, ACCENT, "h"), H_W * 2, 160),
    "logo-horizontal-reverse.svg": svg(H_W, 80, horizontal(CREAM, CREAM, "hr"), H_W * 2, 160),
    "logo-horizontal-mono.svg": svg(H_W, 80, horizontal(INK, INK, "hm"), H_W * 2, 160),
    "symbol.svg": svg(64, 64, symbol(BROWN, ACCENT, CREAM), 256, 256),
    "favicon.svg": svg(64, 64, favicon(), 64, 64),
}

def build_guide():
    """src/guide.tpl.html의 {{파일.svg}}, {{파일.svg:inner}} 자리에 확정 SVG를 넣어 guide.html을 만든다."""
    import re
    html = (SRC / "guide.tpl.html").read_text(encoding="utf-8")

    def fill(m):
        content = FILES[m.group(1)]
        if m.group(2):
            return re.sub(r"^<svg[^>]*>|</svg>\s*$", "", content.strip())
        return content
    return re.sub(r"\{\{([\w.-]+\.svg)(:inner)?\}\}", fill, html)


if __name__ == "__main__":
    for name, content in FILES.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"{name:32s} {len(content):6d} bytes")
    (OUT / "guide.html").write_text(build_guide(), encoding="utf-8")
    print("guide.html")
