"""내려받기 묶음 → dist/

  python3 scripts/build_bundle.py [출력폴더]      (기본: dist/)

만드는 것
  HY_FLIP_한눈에보기.html   페이지·이미지·PDF를 모두 넣은 단일 파일 뷰어.
                            압축을 풀지 않고 ZIP 안에서 바로 열어도 깨지지 않습니다.
  HY_FLIP_전체결과물.zip    허브에서 연결된 모든 파일(사진은 JPEG로 축소) + 뷰어 + 시작하기.txt
  HY_FLIP_핵심문서.zip      제안서·개선방안 PDF + 과제 계획서 폼 답안지

ZIP 속 index.html 은 사진을 못 불러오면(압축을 안 풀고 연 경우) 맨 위에 안내 띠를 띄웁니다.
"""

import base64
import io
import json
import os
import re
import sys
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "dist"
VIEWER = "HY_FLIP_한눈에보기.html"
WEB = "https://claude.ai/artifact/NjWkiYUqe5XssoTKVE3Yj7"
EXTRA = ["proposal/form-answers.md"]
CORE = ["proposal/proposal.pdf", "proposal/studio-booking.pdf", "proposal/form-answers.md"]

REF = re.compile(r"""((?:src|href|data-img)=)(["'])([^"']+)\2|url\((['"]?)([^'")]+)\4\)""")
IMG_EXT = (".png", ".jpg", ".jpeg", ".svg", ".webp")

START = f"""HY FLIP 결과물 — 시작하기
=========================

★ 가장 쉬운 방법: {VIEWER} 를 더블클릭하세요.
  파일 하나에 모든 화면·사진·PDF가 들어 있어서, 압축을 풀지 않아도 그대로 열립니다.

■ 1. 압축 풀기 (폴더째 보고 싶을 때)
  - Windows : ZIP 파일에 마우스 오른쪽 버튼 → [모두 압축 풀기] → [압축 풀기]
  - Mac     : ZIP 파일을 더블클릭하면 같은 자리에 폴더가 생깁니다.
  ※ ZIP 안에서 index.html 을 바로 열면 사진이 안 보입니다(Windows가 그 파일 하나만 꺼내기 때문).
    꼭 압축을 푼 뒤 index.html 을 여세요.

■ 2. 폴더 안내
  proposal/  과제 제안서 PDF · 스튜디오 예약 개선방안 PDF · 과제 계획서 폼 답안지(form-answers.md)
  booking/   스튜디오 예약 화면 (booking.html = 교수용, admin.html = 담당자용)
  home/      홈페이지 시안 (home-final.html = 확정본)
  detail/    사업 상세페이지 시안 (detail-final.html = 확정본)
  logo/      로고 시안 (logo-board-r2.html = 확정본, .svg = 로고 원본 파일)
  assets/    AI로 만든 실사 사진 (gallery.html = 사진 모아 보기)
  shots/     화면 캡처 그림
  prompts/   디자인에 쓴 메타 프롬프트

■ 3. 답안지(form-answers.md) 여는 법
  마우스 오른쪽 버튼 → [연결 프로그램] → [메모장]

■ 4. 웹에서 보기
  {WEB}
  (처음엔 본인만 열림 — 팀원에게 보여주려면 페이지 오른쪽 위 [공유] 메뉴에서 열어 주세요)

※ 제안용 디자인 시안입니다. 수치·후기·연락처는 예시이며, 한양대학교 공식 교표·로고가 아닙니다.
"""

GUARD = """<script>(function(){var i=new Image();i.onerror=function(){var d=document.createElement('div');
d.style.cssText='position:sticky;top:0;z-index:999;background:#B8902F;color:#fff;padding:14px 20px;font:600 15px/1.6 "Noto Sans KR",sans-serif';
d.innerHTML='사진이 보이지 않나요? ZIP 안에서 바로 열면 사진이 따로 떨어집니다. <u>ZIP 파일 오른쪽 클릭 › 모두 압축 풀기</u> 후 다시 열거나, 같은 폴더의 <b>%s</b> 를 여세요.';
document.body.insertBefore(d,document.body.firstChild)};i.src='%s';})();</script>"""


def split(ref):
    """'a/b.html#x' → ('a/b.html', '#x')"""
    m = re.match(r"([^#?]*)(.*)", ref)
    return m.group(1), m.group(2)


def is_local(ref):
    return ref and not ref.startswith(("http:", "https:", "data:", "mailto:", "tel:", "//", "#", "javascript:"))


def resolve(page, ref):
    return os.path.normpath(os.path.join(os.path.dirname(page), ref)).replace("\\", "/")


def collect():
    """허브에서 링크를 따라가며 실제 존재하는 파일을 모읍니다."""
    todo, seen, files = ["index.html"], set(), {"index.html"}
    while todo:
        page = todo.pop()
        if page in seen:
            continue
        seen.add(page)
        for m in REF.finditer((ROOT / page).read_text(encoding="utf-8")):
            ref = split(m.group(3) or m.group(5))[0]
            if not is_local(ref):
                continue
            full = resolve(page, ref)
            if full.startswith("..") or not (ROOT / full).is_file():
                continue
            files.add(full)
            if full.endswith(".html"):
                todo.append(full)
    files |= {f for f in EXTRA if (ROOT / f).is_file()}
    files |= {p.relative_to(ROOT).as_posix() for p in (ROOT / "logo").glob("*.svg")}
    return sorted(files)


def jpeg(path, width=None, crop=None, quality=82):
    im = Image.open(ROOT / path).convert("RGB")
    if width and im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    if crop and im.height > crop:
        im = im.crop((0, 0, im.width, crop))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    return buf.getvalue()


def converts(path):
    return path.endswith(".png") and path.split("/")[0] in ("assets", "shots")


def rewrite_png(text, names):
    return re.sub(r"([\w\-]+)\.png", lambda m: m.group(1) + ".jpg" if m.group(0) in names else m.group(0), text)


# ── 단일 파일 뷰어 ─────────────────────────────────────────────

def build_viewer(files):
    assets, pages, docs = {}, {}, {}
    for f in files:
        if f.endswith(".html"):
            text = (ROOT / f).read_text(encoding="utf-8")

            def tok(m, page=f):
                ref = m.group(3) or m.group(5)
                path, _ = split(ref)
                if not is_local(path) or not path.lower().endswith(IMG_EXT):
                    return m.group(0)
                full = resolve(page, path)
                if full not in assets and (ROOT / full).is_file():
                    if converts(full):
                        data = jpeg(full, width=960, crop=600) if full.startswith("shots/") else jpeg(full, width=1600, quality=80)
                        assets[full] = "data:image/jpeg;base64," + base64.b64encode(data).decode()
                    else:
                        mime = "image/svg+xml" if full.endswith(".svg") else "image/" + full.rsplit(".", 1)[1].replace("jpg", "jpeg")
                        assets[full] = f"data:{mime};base64," + base64.b64encode((ROOT / full).read_bytes()).decode()
                t = f"__A:{full}:A__"
                return f"{m.group(1)}{m.group(2)}{t}{m.group(2)}" if m.group(1) else f"url({m.group(4)}{t}{m.group(4)})"

            pages[f] = REF.sub(tok, text)
        elif f.endswith(".pdf"):
            docs[f] = {"t": "pdf", "d": base64.b64encode((ROOT / f).read_bytes()).decode()}
        elif f.endswith(".md"):
            docs[f] = {"t": "md", "d": (ROOT / f).read_text(encoding="utf-8")}

    def blob(obj):
        return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")

    html = VIEWER_TPL.replace("/*PAGES*/", blob(pages)).replace("/*ASSETS*/", blob(assets)).replace("/*DOCS*/", blob(docs))
    return html.encode("utf-8"), len(pages), len(assets)


VIEWER_TPL = """<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>HY FLIP 한눈에 보기</title>
<style>
:root{--deep:#0A2E55;--gold:#C8A24A;--ivory:#F7F5F0;--ink:#1A2233}
*{box-sizing:border-box}html,body{height:100%;margin:0}
body{display:flex;flex-direction:column;background:var(--ivory);color:var(--ink);font:500 14px/1.4 'Noto Sans KR','Malgun Gothic',system-ui,sans-serif}
.bar{display:flex;align-items:center;gap:10px;padding:8px 16px;background:var(--deep);color:#fff;flex:none}
.bar button{font:inherit;color:#fff;background:transparent;border:1px solid rgba(255,255,255,.35);padding:6px 12px;border-radius:3px;cursor:pointer}
.bar button:hover,.bar button:focus-visible{border-color:var(--gold);color:var(--gold);outline:none}
.bar button:disabled{opacity:.35;cursor:default}
.bar b{color:var(--gold);letter-spacing:.08em;font-size:12px}
.bar span{opacity:.85;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
iframe{flex:1;width:100%;border:0;background:#fff}
</style></head><body>
<div class="bar"><b>HY FLIP</b><button id="home" type="button">← 허브로</button><button id="back" type="button" disabled>뒤로</button><span id="now"></span></div>
<iframe id="f" title="HY FLIP 화면"></iframe>
<script type="application/json" id="P">/*PAGES*/</script>
<script type="application/json" id="A">/*ASSETS*/</script>
<script type="application/json" id="D">/*DOCS*/</script>
<script>
var P=JSON.parse(document.getElementById('P').textContent),A=JSON.parse(document.getElementById('A').textContent),
    D=JSON.parse(document.getElementById('D').textContent),f=document.getElementById('f'),hist=[],cur=null;
function fill(s){return s.replace(/__A:(.+?):A__/g,function(m,p){return A[p]||''})}
function norm(base,ref){var parts=base.split('/');parts.pop();ref.split('/').forEach(function(x){if(x==='..')parts.pop();else if(x&&x!=='.')parts.push(x)});return parts.join('/')}
function esc(s){return s.replace(/[&<>]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;'}[c]})}
function openDoc(p){var d=D[p];if(!d)return;
  if(d.t==='pdf'){var b=atob(d.d),u=new Uint8Array(b.length);for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);
    var url=URL.createObjectURL(new Blob([u],{type:'application/pdf'})),name=p.split('/').pop();
    show(p,'<!doctype html><meta charset="utf-8"><title>'+name+'</title><body style="margin:0;display:flex;flex-direction:column;height:100vh;font:15px/1.5 \\'Noto Sans KR\\',\\'Malgun Gothic\\',sans-serif">'
      +'<div style="padding:10px 16px;background:#F7F5F0;border-bottom:1px solid #E3E6EC;display:flex;gap:12px;align-items:center">'
      +'<b style="color:#0A2E55">'+name+'</b><a id="dl" href="'+url+'" download="'+name+'" style="margin-left:auto;background:#0E4A84;color:#fff;padding:7px 14px;border-radius:3px;text-decoration:none">PDF 내려받기</a></div>'
      +'<iframe src="'+url+'" style="flex:1;border:0;width:100%" title="'+name+'"></iframe></body>',null);}
  else show(p,'<!doctype html><meta charset="utf-8"><title>'+p+'</title><pre style="white-space:pre-wrap;font:15px/1.7 \\'Noto Sans KR\\',\\'Malgun Gothic\\',sans-serif;max-width:900px;margin:32px auto;padding:0 20px">'+esc(d.d)+'</pre>',null,true)}
function show(p,html,hash,push){if(push!==false&&cur)hist.push(cur);cur=p;document.getElementById('back').disabled=!hist.length;
  f.onload=function(){wire(hash)};f.srcdoc=html}
function go(p,hash,push){if(P[p])show(p,fill(P[p]),hash,push);else if(D[p])openDoc(p)}
function wire(hash){var doc=f.contentDocument;if(!doc)return;document.getElementById('now').textContent=doc.title||cur;
  if(hash){var t=doc.getElementById(hash.slice(1));if(t)t.scrollIntoView()}
  doc.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href]');if(!a)return;
    var h=a.getAttribute('href');if(/^(blob:|data:)/.test(h))return;if(/^(https?:|mailto:|tel:)/.test(h)){e.preventDefault();window.open(h,'_blank');return}
    e.preventDefault();if(h.charAt(0)==='#'){var t=doc.getElementById(h.slice(1));if(t)t.scrollIntoView({behavior:'smooth'});return}
    var m=h.match(/^([^#?]*)(#.*)?/),p=norm(cur,m[1]);if(p===cur&&m[2]){var t2=doc.getElementById(m[2].slice(1));if(t2)t2.scrollIntoView({behavior:'smooth'});return}
    go(p,m[2])},true)}
document.getElementById('home').onclick=function(){go('index.html')};
document.getElementById('back').onclick=function(){if(hist.length)go(hist.pop(),null,false);document.getElementById('back').disabled=!hist.length};
go('index.html');
</script></body></html>"""


# ── ZIP ───────────────────────────────────────────────────────

def build_zip(files, viewer):
    names = {Path(f).name for f in files if converts(f)}
    first = next(f for f in files if f.startswith("shots/") and converts(f))
    out = OUT / "HY_FLIP_전체결과물.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("HY_FLIP/시작하기.txt", START)
        z.writestr(f"HY_FLIP/{VIEWER}", viewer)
        for f in files:
            if converts(f):
                z.writestr(f"HY_FLIP/{f[:-4]}.jpg", jpeg(f, width=1440 if f.startswith("shots/") else None))
            elif f.endswith((".html", ".md")):
                text = rewrite_png((ROOT / f).read_text(encoding="utf-8"), names)
                if f == "index.html":
                    text = text.replace("</body>", GUARD % (VIEWER, first[:-4] + ".jpg") + "</body>")
                z.writestr(f"HY_FLIP/{f}", text)
            else:
                z.write(ROOT / f, f"HY_FLIP/{f}")
    core = OUT / "HY_FLIP_핵심문서.zip"
    with zipfile.ZipFile(core, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("HY_FLIP/시작하기.txt", START)
        for f in CORE:
            z.write(ROOT / f, f"HY_FLIP/{f}")
    return out, core


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = collect()
    viewer, n_pages, n_assets = build_viewer(files)
    (OUT / VIEWER).write_bytes(viewer)
    full, core = build_zip(files, viewer)
    mb = lambda p: f"{p.stat().st_size / 2**20:.1f}MB"
    print(f"{VIEWER}  {mb(OUT / VIEWER)}  (페이지 {n_pages} · 이미지 {n_assets})")
    print(f"{full.name}  {mb(full)}  (파일 {len(files) + 2})")
    print(f"{core.name}  {mb(core)}")


if __name__ == "__main__":
    main()
