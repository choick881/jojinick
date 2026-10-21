"""시안 템플릿의 {{파일.svg}} 자리에 brand/logo 확정 SVG를 넣어 prototypes/*.html을 만든다.
실행: python3 prototypes/src/build.py
"""
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent
LOGO = SRC.parents[1] / "brand" / "logo"

for tpl in SRC.glob("*.tpl.html"):
    html = re.sub(r"\{\{([\w.-]+\.svg)\}\}", lambda m: (LOGO / m.group(1)).read_text(encoding="utf-8").strip(),
                  tpl.read_text(encoding="utf-8"))
    out = SRC.parent / tpl.name.replace(".tpl", "")
    out.write_text(html, encoding="utf-8")
    print(out.relative_to(SRC.parents[1]))
