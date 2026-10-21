"""시안 템플릿의 {{파일.svg}}·{{파일.json}} 자리에 brand/logo SVG와 brand/*.json을 넣어 prototypes/*.html을 만든다.
실행: python3 prototypes/src/build.py
"""
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent
BRAND = SRC.parents[1] / "brand"
LOGO = BRAND / "logo"

PARTS = SRC / "partials"


def expand(html):
    """{{> 이름}} → partials/이름.html, {{PH:이름}} → partials/ph-이름.svg (사진 자리 선 그림)"""
    html = re.sub(r"\{\{> ([\w-]+)\}\}", lambda m: (PARTS / f"{m.group(1)}.html").read_text(encoding="utf-8").strip(), html)
    return re.sub(r"\{\{PH:(\w+)\}\}", lambda m: (PARTS / f"ph-{m.group(1)}.svg").read_text(encoding="utf-8").strip(), html)


for tpl in SRC.glob("*.tpl.html"):
    html = re.sub(r"\{\{([\w.-]+\.(svg|json))\}\}",
                  lambda m: ((LOGO if m.group(2) == "svg" else BRAND) / m.group(1)).read_text(encoding="utf-8").strip(),
                  expand(tpl.read_text(encoding="utf-8")))
    out = SRC.parent / tpl.name.replace(".tpl", "")
    out.write_text(html, encoding="utf-8")
    print(out.relative_to(SRC.parents[1]))
