"""로고 목업 합성: AI 로 만든 '빈' 배경 사진 위에 확정 로고를 정확한 모양 그대로 얹습니다.

  python scripts/composite_mockups.py           # assets/mockup_layout.json 대로 → assets/mock-*.png
  python scripts/composite_mockups.py --guide   # 로고 위치 확인용 빨간 가이드 테두리까지 그려 shots/ 에 저장

효과
  engrave — 황동 명판 음각 (그림자·하이라이트 + 에나멜 색)
  glow    — 백릿 입체 사인 (은은한 빛 번짐)
  print   — 종이 인쇄 (종이 결이 비치도록 곱하기 합성)
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from build_logos_r2 import NEW, a_mark

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
LAYOUT = ASSETS / "mockup_layout.json"

SVG = {"seal": NEW["D"]["svg"], "tile": NEW["E"]["svg"], "mark": lambda uid: a_mark()}

RENDER_JS = r"""
const { chromium } = require(process.env.PLAYWRIGHT_PATH || '/opt/node-tools/node_modules/playwright');
const jobs = JSON.parse(require('fs').readFileSync(process.argv[2], 'utf8'));
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const j of jobs) {
    await page.setViewportSize({ width: j.size, height: j.size });
    await page.setContent(`<html><head><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700&display=swap" rel="stylesheet">
      <style>html,body{margin:0;background:transparent}svg{display:block}</style></head><body>${j.svg}</body></html>`,
      { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: j.out, omitBackground: true });
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
"""


def render_logos(layers, tmp):
    """레이어마다 로고를 투명 PNG 로 렌더해 경로 목록 반환."""
    jobs = []
    for i, ly in enumerate(layers):
        px = ly["_px"]
        style = f'--mark:{ly["mark"]};--accent:{ly["accent"]};--knock:{ly.get("knock", "#FFFFFF")}'
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="{px}" height="{px}" '
               f'style="{style}">{SVG[ly["logo"]](f"m{i}")}</svg>')
        jobs.append({"svg": svg, "out": str(tmp / f"logo{i}.png"), "size": px})
    jf = tmp / "jobs.json"
    jf.write_text(json.dumps(jobs), encoding="utf-8")
    js = tmp / "render.cjs"
    js.write_text(RENDER_JS, encoding="utf-8")
    subprocess.run(["node", str(js), str(jf)], check=True)
    return [Image.open(j["out"]).convert("RGBA") for j in jobs]


def alpha_of(im, k=1.0):
    return im.getchannel("A").point(lambda a: int(a * k))


def engrave(bg, logo, x, y):
    a = alpha_of(logo)
    s = max(1, logo.width // 220)
    shadow = Image.new("RGBA", logo.size, (0, 0, 0, 0))
    shadow.putalpha(a.point(lambda v: int(v * 0.45)))
    light = Image.new("RGBA", logo.size, (255, 244, 214, 0))
    light.putalpha(a.point(lambda v: int(v * 0.35)))
    bg.alpha_composite(light, (x + s, y + s))           # 아래·오른쪽 가장자리 반사광
    bg.alpha_composite(shadow, (x - s, y - s))          # 위·왼쪽 파인 그림자
    enamel = logo.copy()
    enamel.putalpha(a.point(lambda v: int(v * 0.92)))
    bg.alpha_composite(enamel, (x, y))


def glow(bg, logo, x, y):
    pad = logo.width // 4
    halo = Image.new("RGBA", (logo.width + pad * 2, logo.height + pad * 2), (0, 0, 0, 0))
    white = Image.new("RGBA", logo.size, (235, 242, 255, 0))
    white.putalpha(alpha_of(logo))
    halo.alpha_composite(white, (pad, pad))
    halo = halo.filter(ImageFilter.GaussianBlur(logo.width / 28))
    halo.putalpha(halo.getchannel("A").point(lambda v: int(v * 0.7)))
    bg.alpha_composite(halo, (x - pad, y - pad))
    drop = Image.new("RGBA", logo.size, (0, 0, 0, 0))
    drop.putalpha(alpha_of(logo, 0.35))
    bg.alpha_composite(drop.filter(ImageFilter.GaussianBlur(3)), (x + 4, y + 6))
    bg.alpha_composite(logo, (x, y))


def print_ink(bg, logo, x, y):
    region = bg.crop((x, y, x + logo.width, y + logo.height)).convert("RGB")
    ink = Image.new("RGB", logo.size, (255, 255, 255))
    ink.paste(logo.convert("RGB"), mask=logo.getchannel("A"))
    printed = ImageChops.multiply(region, ink).convert("RGBA")
    printed.putalpha(alpha_of(logo, 0.95))
    bg.alpha_composite(printed, (x, y))


EFFECTS = {"engrave": engrave, "glow": glow, "print": print_ink}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--guide", action="store_true")
    args = ap.parse_args()
    layout = json.loads(LAYOUT.read_text(encoding="utf-8"))
    missing = [v["background"] for k, v in layout.items() if k != "note" and not (ASSETS / v["background"]).exists()]
    if missing:
        print("배경 사진이 없습니다 (먼저 scripts/fetch_figma.py): " + ", ".join(missing))
        return 1
    for name, spec in layout.items():
        if name == "note":
            continue
        bg = Image.open(ASSETS / spec["background"]).convert("RGBA")
        W, H = bg.size
        for ly in spec["layers"]:
            ly["_px"] = max(16, round(ly["size"] * H))
        with tempfile.TemporaryDirectory() as td:
            logos = render_logos(spec["layers"], Path(td))
        guides = []
        for ly, lg in zip(spec["layers"], logos):
            x, y = round(ly["cx"] * W - lg.width / 2), round(ly["cy"] * H - lg.height / 2)
            EFFECTS[ly["effect"]](bg, lg, x, y)
            guides.append((x, y, x + lg.width, y + lg.height))
        out = ASSETS / f"{name}.png"
        bg.convert("RGB").save(out, "PNG", optimize=True)
        print(f"✓ {out.relative_to(ROOT)} ({W}×{H}, 로고 {len(logos)}개)")
        if args.guide:
            g = bg.convert("RGB")
            d = ImageDraw.Draw(g)
            for box in guides:
                d.rectangle(box, outline=(230, 40, 40), width=3)
            (ROOT / "shots").mkdir(exist_ok=True)
            g.save(ROOT / "shots" / f"{name}-guide.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
