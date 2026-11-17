"""문서 모델 — 한 번 만든 내용(블록)을 HTML(인쇄)·DOCX(Word)·TXT 로 모두 내보낸다."""

from __future__ import annotations

import html
from pathlib import Path

from .util import FONTS, hhmmss

CSS = """
@font-face{font-family:'Pretendard';font-weight:500;src:url('file://%(f)s/Pretendard-Medium.otf')}
@font-face{font-family:'Pretendard';font-weight:700;src:url('file://%(f)s/Pretendard-Bold.otf')}
@font-face{font-family:'Pretendard';font-weight:800;src:url('file://%(f)s/Pretendard-ExtraBold.otf')}
@page{size:A4;margin:20mm 18mm 20mm 18mm;
  @bottom-center{content:counter(page) ' / ' counter(pages);font:500 8.5pt Pretendard;color:#777}
  @top-left{content:string(doc-title);font:500 8.5pt Pretendard;color:#777}}
*{box-sizing:border-box}
html{font-family:'Pretendard',sans-serif;font-weight:500;color:#1b2430;font-size:10.5pt;line-height:1.62}
h1{string-set:doc-title content();font-size:20pt;font-weight:800;margin:0 0 4pt;color:#0f2a4a;line-height:1.3}
.meta{color:#4a5668;font-size:9.5pt;margin:0 0 3pt}
.rule{border:0;border-top:2px solid #0f2a4a;margin:10pt 0 12pt}
h2{font-size:13pt;font-weight:800;color:#0f2a4a;margin:16pt 0 6pt;border-left:4px solid #2b6cb0;padding-left:8pt;break-after:avoid}
h3{font-size:11pt;font-weight:700;margin:12pt 0 3pt;break-after:avoid}
p{margin:0 0 6pt;orphans:3;widows:3}
p.muted{color:#5b6677;font-size:9.5pt}
p.ans{background:#eef5ff;border-radius:4pt;padding:4pt 8pt}
.ts{display:inline-block;min-width:34pt;color:#2b6cb0;font-weight:700;font-size:9pt;font-variant-numeric:tabular-nums}
.tsp{display:flex;gap:6pt;margin:0 0 5pt;break-inside:avoid}.tsp .t{flex:1}
ul{margin:0 0 6pt;padding-left:16pt}li{margin:0 0 2pt}
table{border-collapse:collapse;width:100%%;margin:4pt 0 8pt;font-size:9.5pt}
th{background:#0f2a4a;color:#fff;font-weight:700;text-align:left}
th,td{border:1px solid #cbd5e1;padding:3pt 6pt;vertical-align:top}
tr{break-inside:avoid}tr:nth-child(even) td{background:#f6f9fc}
.pb{break-after:page}
""" % {"f": str(FONTS).replace("\\", "/")}


class Doc:
    def __init__(self, title: str, meta: list[str] | None = None, lang: str = "ko"):
        self.title, self.meta, self.lang, self.blocks = title, meta or [], lang, []

    # 블록: (종류, 내용...)
    def h2(self, t): self.blocks.append(("h2", t)); return self
    def h3(self, t): self.blocks.append(("h3", t)); return self
    def p(self, t, cls=""): self.blocks.append(("p", t, cls)); return self
    def tsp(self, sec, t): self.blocks.append(("tsp", sec, t)); return self
    def ul(self, items): self.blocks.append(("ul", list(items))); return self
    def table(self, head, rows, widths=None): self.blocks.append(("table", head, rows, widths)); return self
    def pb(self): self.blocks.append(("pb",)); return self

    # ---- HTML ----
    def body_html(self) -> str:
        e = html.escape
        out = [f"<h1>{e(self.title)}</h1>"] + [f'<div class="meta">{e(m)}</div>' for m in self.meta] + ['<hr class="rule">']
        for b in self.blocks:
            k = b[0]
            if k in ("h2", "h3"):
                out.append(f"<{k}>{e(b[1])}</{k}>")
            elif k == "p":
                out.append(f'<p class="{b[2]}">{e(b[1]).replace(chr(10), "<br>")}</p>')
            elif k == "tsp":
                out.append(f'<div class="tsp"><span class="ts">{hhmmss(b[1])[3:]}</span><span class="t">{e(b[2])}</span></div>')
            elif k == "ul":
                out.append("<ul>" + "".join(f"<li>{e(i)}</li>" for i in b[1]) + "</ul>")
            elif k == "table":
                cg = "".join(f'<col style="width:{w}">' for w in b[3]) if b[3] else ""
                out.append(f"<table><colgroup>{cg}</colgroup><thead><tr>" + "".join(f"<th>{e(h)}</th>" for h in b[1]) + "</tr></thead><tbody>"
                           + "".join("<tr>" + "".join(f"<td>{e(c).replace(chr(10), '<br>')}</td>" for c in r) + "</tr>" for r in b[2])
                           + "</tbody></table>")
            elif k == "pb":
                out.append('<div class="pb"></div>')
        return "\n".join(out)

    def to_html(self) -> str:
        return (f'<!doctype html><html lang="{self.lang}"><head><meta charset="utf-8"><title>{html.escape(self.title)}</title>'
                f"<style>{CSS}</style></head><body>{self.body_html()}</body></html>")

    # ---- TXT ----
    def to_txt(self) -> str:
        L = [self.title, *self.meta, "=" * 60, ""]
        for b in self.blocks:
            k = b[0]
            if k in ("h2", "h3"):
                L += ["", ("■ " if k == "h2" else "▷ ") + b[1]]
            elif k == "p":
                L.append(b[1])
            elif k == "tsp":
                L.append(f"[{hhmmss(b[1])[3:]}] {b[2]}")
            elif k == "ul":
                L += [f"  · {i}" for i in b[1]]
            elif k == "table":
                L.append(" | ".join(b[1]))
                L += [" | ".join(c.replace("\n", " / ") for c in r) for r in b[2]]
            elif k == "pb":
                L += ["", "-" * 60, ""]
        return "\n".join(L) + "\n"

    # ---- DOCX ----
    def to_docx(self, path: Path) -> None:
        from docx import Document
        from docx.enum.text import WD_BREAK
        from docx.oxml.ns import qn
        from docx.shared import Mm, Pt, RGBColor

        d = Document()
        sec = d.sections[0]
        sec.page_width, sec.page_height = Mm(210), Mm(297)
        sec.left_margin = sec.right_margin = Mm(18)
        sec.top_margin = sec.bottom_margin = Mm(20)
        st = d.styles["Normal"]
        st.font.name, st.font.size = "맑은 고딕", Pt(10.5)
        st.element.rPr.rFonts.set(qn("w:eastAsia"), "맑은 고딕")
        navy = RGBColor(0x0F, 0x2A, 0x4A)

        def para(text, size=None, bold=False, color=None, after=4):
            p = d.add_paragraph()
            r = p.add_run(text)
            r.bold = bold
            if size:
                r.font.size = Pt(size)
            if color:
                r.font.color.rgb = color
            p.paragraph_format.space_after = Pt(after)
            return p

        para(self.title, 20, True, navy, 2)
        for m in self.meta:
            para(m, 9.5, color=RGBColor(0x4A, 0x56, 0x68), after=1)
        para("")
        for b in self.blocks:
            k = b[0]
            if k == "h2":
                para(b[1], 13, True, navy, 4).paragraph_format.space_before = Pt(12)
            elif k == "h3":
                para(b[1], 11, True, after=2).paragraph_format.space_before = Pt(8)
            elif k == "p":
                para(b[1], 9.5 if b[2] == "muted" else None, color=RGBColor(0x5B, 0x66, 0x77) if b[2] == "muted" else None)
            elif k == "tsp":
                p = d.add_paragraph()
                r = p.add_run(f"{hhmmss(b[1])[3:]}  ")
                r.bold, r.font.size, r.font.color.rgb = True, Pt(9), RGBColor(0x2B, 0x6C, 0xB0)
                p.add_run(b[2])
                p.paragraph_format.space_after = Pt(3)
            elif k == "ul":
                for i in b[1]:
                    d.add_paragraph(i, style="List Bullet").paragraph_format.space_after = Pt(1)
            elif k == "table":
                t = d.add_table(rows=1, cols=len(b[1]))
                t.style = "Table Grid"
                for c, h in zip(t.rows[0].cells, b[1]):
                    c.text = ""
                    r = c.paragraphs[0].add_run(h)
                    r.bold = True
                for row in b[2]:
                    cells = t.add_row().cells
                    for c, v in zip(cells, row):
                        c.text = v
                for row in t.rows:
                    for c in row.cells:
                        for pp in c.paragraphs:
                            for rr in pp.runs:
                                rr.font.size = Pt(9)
                if b[3]:
                    for row in t.rows:
                        for c, w in zip(row.cells, b[3]):
                            c.width = Mm(float(w.rstrip("%")) / 100 * 174)
                d.add_paragraph()
            elif k == "pb":
                d.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        d.save(path)
