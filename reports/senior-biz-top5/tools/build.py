#!/usr/bin/env python3
"""src/*.md → html/*.html (인쇄용, CSS 내장). 사용법: python3 tools/build.py"""
import pathlib, re, html
import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "src", ROOT / "html"
CSS = (ROOT / "tools" / "style.css").read_text(encoding="utf-8")

PAGE = """<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<style>{css}</style></head>
<body>
<div class="printbar">A4 인쇄용 보고서입니다 <button onclick="window.print()">인쇄 / PDF 저장</button></div>
<div class="doc">
<section class="cover">
  <div class="kicker">{kicker}</div>
  <div class="no">{no}</div>
  <h1 class="title">{title_html}</h1>
  <div class="subtitle">{subtitle}</div>
  <div class="tagrow">{tags}</div>
  <div class="meta">{meta}</div>
</section>
{body}
</div></body></html>"""


def parse(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
        text = text[m.end():]
    return fm, text


def gantt(h):
    def fix(m):
        seg = m.group(0)
        seg = seg.replace("<td>■</td>", '<td class="on"></td>')
        seg = re.sub(r"<td><strong>([^<]+)</strong></td>", r'<td class="ms">\1</td>', seg)
        seg = re.sub(r"<td>([가-힣/0-9]{1,6})</td>", r'<td class="mid">\1</td>', seg)
        return seg
    return re.sub(r'<div class="gantt">.*?</div>', fix, h, flags=re.S)


def main():
    OUT.mkdir(exist_ok=True)
    for md_path in sorted(SRC.glob("*.md")):
        fm, body = parse(md_path.read_text(encoding="utf-8"))
        conv = markdown.Markdown(extensions=["tables", "attr_list", "md_in_html", "sane_lists", "toc"])
        body_html = gantt(conv.convert(body))
        tags = "".join(f"<span>{html.escape(t.strip())}</span>" for t in fm.get("tags", "").split("|") if t.strip())
        meta = "<br>".join(f"<b>{html.escape(k)}</b> {html.escape(v)}" for k, v in
                           (x.split("=", 1) for x in fm.get("meta", "").split("|") if "=" in x))
        page = PAGE.format(
            title=html.escape(fm.get("title", md_path.stem).replace("<br>", " ")),
            title_html=fm.get("title", md_path.stem),
            kicker=html.escape(fm.get("kicker", "")),
            no=html.escape(fm.get("no", "")),
            subtitle=fm.get("subtitle", ""),
            tags=tags, meta=meta, css=CSS, body=body_html,
        )
        (OUT / f"{md_path.stem}.html").write_text(page, encoding="utf-8")
        print("built", md_path.stem)


if __name__ == "__main__":
    main()
