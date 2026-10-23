"""셀프 스튜디오 예약·승인 자동화 프로토타입 → booking/booking.html (교수용), booking/admin.html (담당자용)

흐름: 교수 예약 신청 → AI 사전 검토(규칙 + 교안 점검) → 규칙 충족 시 자동 승인 / 예외만 담당자
      → 구글 캘린더 자동 등록 → 확인 메일 · D-3 · D-1 리마인드 → 촬영 후 편집요청·CMS·LMS 연계
스튜디오 목록·규칙은 2025-2 스마트 교육 OT 자료(셀프 스튜디오 12실, '촬영 3일 전부터 변경 불가')를 따름.
화면의 예약·통계 데이터는 모두 예시이며, 실제 연동(Apps Script·Calendar API)은 개선방안 문서 참고.
  python scripts/build_booking.py
"""

import json
from pathlib import Path

from build_detail import CSS_A, CSS_DK
from build_home import CSS_HOME, footer, nav
from site_kit import IMG_JS, head, icon, img

OUT = Path(__file__).resolve().parent.parent / "booking"

STUDIOS = [
    ("s01", "경영대학 307호", "경영"), ("s02", "경제금융관 508호", "경제금융"), ("s03", "공과대학 본관 314호", "공과"),
    ("s04", "공업센터별관 716-2호", "공과"), ("s05", "사범대학 본관 314호", "사범"), ("s06", "사회과학대학 107호", "사회과학"),
    ("s07", "예술체육대학 232-1호", "예술체육"), ("s08", "융합교육관 205호", "정책과학"), ("s09", "의과대학 본관 616호", "의과"),
    ("s10", "인문과학대학 101호", "인문과학"), ("s11", "자연과학대학 721호", "자연과학"), ("s12", "백남학술정보관 511호 (학생전용)", "학생"),
]
SLOTS = ["09:00–11:00", "11:00–13:00", "13:00–15:00", "15:00–17:00", "17:00–19:00"]
COURSES = ["데이터로 읽는 경영학 원론", "공학수학 I", "글로벌 커뮤니케이션 영어", "AI 시대의 미디어 리터러시"]
TYPES = ["유형1 PPT 강의형", "유형2 타블릿 판서형", "유형3 유리칠판 판서형", "유형4 전자칠판 판서형"]

CSS_BOOK = """
:root{--hy:#0E4A84}
.band{background:#071A31;color:#fff;padding:120px 0 40px;position:relative;overflow:hidden}
.band > .ph{position:absolute;inset:0;opacity:.35}
.band .w{position:relative;z-index:1}
.band h1{font:900 40px/1.25 var(--serif);margin:12px 0 8px} .band p{color:#c9d5e5;max-width:640px}
.steps3{display:flex;gap:10px;margin-top:22px;flex-wrap:wrap}
.steps3 span{border:1px solid rgba(255,255,255,.3);padding:8px 14px;font-size:14px;color:#dfe7f1}
.steps3 span b{color:#E2C77F;margin-right:6px}
.demo{display:inline-block;margin-top:14px;font-size:12px;color:#E2C77F;border:1px dashed rgba(226,199,127,.6);padding:4px 10px}
.app{display:grid;grid-template-columns:1fr 360px;gap:28px;padding:40px 0 80px;align-items:start}
.card{background:#fff;border:1px solid var(--line);padding:24px;margin-bottom:20px}
.card h2{font:900 20px/1.3 var(--serif);color:var(--deep);display:flex;align-items:center;gap:10px;margin-bottom:14px}
.card h2 .n{font:700 12px/1 var(--sans);background:var(--navy);color:#fff;padding:5px 8px}
.row{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-bottom:14px}
select,input,textarea{font:inherit;font-size:15px;border:1px solid #cfd6e1;padding:10px 12px;background:#fff;color:var(--ink);border-radius:2px}
select:focus,input:focus,textarea:focus{outline:2px solid var(--hy);outline-offset:1px}
label.f{display:flex;flex-direction:column;gap:6px;font-size:13px;color:var(--muted);font-weight:500}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.wk{display:flex;align-items:center;gap:10px}
.wk button{border:1px solid #cfd6e1;background:#fff;width:34px;height:34px;cursor:pointer;font-size:16px}
.wk b{font-size:15px;color:var(--deep);min-width:190px;text-align:center}
.cal{width:100%;border-collapse:collapse;font-size:13px;table-layout:fixed}
.cal th{background:var(--ivory);color:var(--deep);font-weight:700;padding:10px 4px;border:1px solid var(--line)}
.cal th small{display:block;font-weight:400;color:var(--muted)}
.cal td{border:1px solid var(--line);height:46px;padding:3px;text-align:center}
.cal td.t{background:var(--ivory);font-size:12px;color:var(--muted);width:92px}
.slot{width:100%;height:100%;border:0;cursor:pointer;font:inherit;font-size:12px;transition:.15s}
.slot.free{background:#EEF5EE;color:#1E6B3A} .slot.free:hover{background:#d9ecd9}
.slot.busy{background:#E8ECF2;color:#7a8496;cursor:not-allowed}
.slot.lock{background:repeating-linear-gradient(135deg,#f6efe0 0 6px,#fbf7ee 6px 12px);color:#8a6d1e;cursor:not-allowed}
.slot.sel{background:var(--hy);color:#fff;font-weight:700}
.scroll{overflow-x:auto;max-width:100%}
.app > *,.adm > *,.card{min-width:0}
.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin-top:10px}
.legend i{display:inline-block;width:12px;height:12px;vertical-align:-1px;margin-right:5px}
.drop{border:1.5px dashed #b9c3d3;padding:16px;text-align:center;color:var(--muted);font-size:14px;cursor:pointer;background:#fafbfd}
.drop.ok{border-color:#1E7A43;color:#1E7A43;background:#f1f8f3}
.side{position:sticky;top:20px}
.aibox{background:var(--deep);color:#fff;border:0}
.aibox h2{color:#fff} .aibox h2 .n{background:var(--gold);color:#0A1B30}
.chk{list-style:none;margin:6px 0 16px}
.chk li{display:grid;grid-template-columns:22px 1fr;gap:8px;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.12);font-size:14px}
.chk li small{display:block;color:#9fb0c8;font-size:12px;margin-top:2px}
.chk .s{width:20px;height:20px;border-radius:50%;display:grid;place-items:center;font-size:12px;font-weight:900}
.s.ok{background:#2E9E5B;color:#fff} .s.warn{background:var(--gold);color:#0A1B30} .s.no{background:#D9534F;color:#fff} .s.wait{background:rgba(255,255,255,.18);color:#fff}
.verdict{padding:14px;font-weight:700;font-size:15px;margin-bottom:14px}
.verdict.ok{background:#E6F4EC;color:#16603A} .verdict.warn{background:#FFF4D8;color:#7A5A0E} .verdict.no{background:#FBE5E4;color:#9B2C2A} .verdict.wait{background:rgba(255,255,255,.1);color:#dfe7f1}
.aibox .btn{width:100%;justify-content:center}
.aibox .btn[disabled]{opacity:.4;cursor:not-allowed}
.summary{font-size:13px;color:#c9d5e5;margin-bottom:14px;line-height:1.7}
.summary b{color:#fff}
.faq{font-size:14px} .faq .q{background:var(--ivory);padding:10px 12px;margin-bottom:6px} .faq .a{border-left:3px solid var(--gold);padding:8px 12px;margin-bottom:12px;color:#3a4356}
.faq .a b{color:var(--navy)}
.modal{position:fixed;inset:0;background:rgba(5,18,36,.6);display:none;align-items:center;justify-content:center;z-index:50;padding:20px}
.modal.on{display:flex}
.modal .box2{background:#fff;max-width:520px;width:100%;padding:28px}
.modal h3{font:900 22px/1.3 var(--serif);color:var(--deep);margin-bottom:6px}
.tl{list-style:none;margin:16px 0;border-left:2px solid var(--line)}
.tl li{position:relative;padding:0 0 14px 18px;font-size:14px}
.tl li::before{content:"";position:absolute;left:-7px;top:4px;width:12px;height:12px;border-radius:50%;background:var(--hy)}
.tl li small{display:block;color:var(--muted);font-size:12px}
/* 관리자 */
.kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin:36px 0 20px}
.kpi{background:#fff;border:1px solid var(--line);padding:18px}
.kpi b{display:block;font:900 30px/1.1 var(--serif);color:var(--hy)} .kpi span{font-size:13px;color:var(--muted)}
.kpi em{font-style:normal;font-size:12px;color:#1E7A43;font-weight:700}
.adm{display:grid;grid-template-columns:1.25fr 1fr;gap:20px;padding-bottom:80px;align-items:start}
.qc{border:1px solid var(--line);border-left:4px solid var(--gold);padding:16px;margin-bottom:12px;background:#fff}
.qc.no{border-left-color:#D9534F}
.qc .h{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap} .qc .h b{color:var(--deep)}
.qc .why{font-size:13px;color:#7A5A0E;background:#FFF8E6;padding:8px 10px;margin:10px 0}
.qc.no .why{color:#9B2C2A;background:#FDF0EF}
.qc .recm{font-size:13px;color:var(--hy);margin-bottom:10px}
.qc .draft{font-size:13px;color:#3a4356;background:var(--ivory);padding:10px;margin-bottom:12px;border:1px dashed #cfd6e1}
.qc .acts{display:flex;gap:8px;flex-wrap:wrap}
.qc .acts button{font:700 13px var(--sans);padding:8px 14px;border:1px solid var(--navy);background:#fff;color:var(--navy);cursor:pointer}
.qc .acts button.p{background:var(--navy);color:#fff}
.qc.done{opacity:.55} .qc.done .acts{display:none}
.tbl{width:100%;border-collapse:collapse;font-size:13.5px}
.tbl th,.tbl td{border-bottom:1px solid var(--line);padding:9px 6px;text-align:left}
.tbl th{color:var(--muted);font-weight:500;font-size:12px}
.pill{font-size:11px;font-weight:700;padding:3px 7px;border-radius:2px;white-space:nowrap}
.pill.a{background:#E6F4EC;color:#16603A} .pill.m{background:#E3ECF8;color:var(--hy)} .pill.c{background:#F1F2F4;color:#6b7280}
.bars div{display:grid;grid-template-columns:150px 1fr 44px;gap:10px;align-items:center;font-size:13px;margin:7px 0}
.bars i{display:block;height:10px;background:var(--hy)} .bars i.lo{background:#8FB0D6}
.bars span{color:var(--muted);text-align:right}
.log{list-style:none;font-size:13px} .log li{display:grid;grid-template-columns:52px 1fr;gap:10px;padding:7px 0;border-bottom:1px dashed var(--line)}
.log time{color:var(--muted)} .log b{color:var(--deep)}
.note2{font-size:12px;color:var(--muted);margin-top:8px}
@media (max-width:1000px){
  .app,.adm{grid-template-columns:1fr} .side{position:static} .grid2{grid-template-columns:1fr}
  .kpis{grid-template-columns:1fr 1fr} .band{padding:96px 0 32px} .band h1{font-size:30px}
  .cal td.t{width:64px;font-size:11px} .slot{font-size:11px} .cal th{font-size:12px;padding:8px 2px}
  .bars div{grid-template-columns:110px 1fr 40px}
  .cal{min-width:520px} .tbl{min-width:480px} .row .wk{width:100%;justify-content:space-between}
  .card{padding:18px} .kpi b{font-size:24px}
}
"""

DATA = {
    "studios": [{"id": i, "name": n, "college": c} for i, n, c in STUDIOS],
    "slots": SLOTS,
    "courses": COURSES,
    "today": "2026-10-19",
}

BOOK_JS = """<script>
const D = __DATA__;
const DAY = 864e5, TODAY = new Date(D.today + 'T00:00:00');
const fmt = d => `${d.getMonth()+1}/${d.getDate()}`;
const wd = ['일','월','화','수','목','금','토'];
let week = 0, sel = null;
// 예시 예약 현황: 스튜디오·날짜·시간마다 결정적인 의사난수
function busy(sid, d, s){ const k = (sid.charCodeAt(1)*7 + sid.charCodeAt(2)*13 + d.getDate()*5 + s*11) % 10; return k < 3; }
function monday(off){ const d = new Date(TODAY); d.setDate(d.getDate() - ((d.getDay()+6)%7) + off*7); return d; }
function draw(){
  const sid = document.getElementById('studio').value, m = monday(week);
  const days = [...Array(5)].map((_,i)=> new Date(m.getTime()+i*DAY));
  document.getElementById('wk').textContent = `${m.getFullYear()}. ${fmt(days[0])} – ${fmt(days[4])}`;
  let h = '<thead><tr><th></th>' + days.map(d=>`<th>${wd[d.getDay()]}<small>${fmt(d)}</small></th>`).join('') + '</tr></thead><tbody>';
  D.slots.forEach((t,s)=>{
    h += `<tr><td class="t">${t}</td>`;
    days.forEach(d=>{
      const key = `${sid}|${d.toISOString().slice(0,10)}|${s}`;
      const lock = (d - TODAY) / DAY < 3, b = busy(sid,d,s);
      const cls = sel===key ? 'sel' : lock ? 'lock' : b ? 'busy' : 'free';
      const txt = sel===key ? '선택' : lock ? '마감' : b ? '예약됨' : '가능';
      h += `<td><button type="button" class="slot ${cls}" data-k="${key}" ${cls==='busy'||cls==='lock'?'disabled':''}>${txt}</button></td>`;
    });
    h += '</tr>';
  });
  document.getElementById('cal').innerHTML = h + '</tbody>';
  document.querySelectorAll('.slot.free,.slot.sel').forEach(b=> b.onclick = ()=>{ sel = b.dataset.k; draw(); check(); });
}
function set(id, st, msg){ const li = document.getElementById(id); li.querySelector('.s').className = 's ' + st;
  li.querySelector('.s').textContent = {ok:'✓',warn:'!',no:'✕',wait:'·'}[st]; li.querySelector('small').textContent = msg; }
function check(){
  const course = document.getElementById('course').value, sid = document.getElementById('studio').value;
  const wkno = +document.getElementById('wkno').value, file = document.getElementById('drop').classList.contains('ok');
  const name = document.getElementById('prof').value.trim();
  let worst = 'ok';
  const up = st => { const r = {ok:0,warn:1,no:2}; if (r[st] > r[worst]) worst = st; };
  if (!sel){ set('c1','wait','캘린더에서 시간을 선택하세요'); worst = 'wait'; }
  else { const [,d,s] = sel.split('|'); set('c1','ok',`${d} ${D.slots[+s]} · 구글 캘린더 빈 시간 확인`); }
  if (course === '__other'){ set('c2','warn','승인 과목 목록에 없음 → 담당자 확인'); up('warn'); }
  else set('c2','ok','2026-1 특수수업(SMART-F) 승인 과목');
  if (sid === 's12'){ set('c3','no','학생전용 스튜디오 — 교수 예약 불가, 다른 스튜디오 추천'); up('no'); }
  else set('c3','ok','교수자용 셀프 스튜디오');
  if (wkno === 3){ set('c4','warn','3주차 촬영이 이미 예약됨 → 재촬영이면 담당자 확인'); up('warn'); }
  else set('c4','ok',`${wkno}주차 첫 촬영 · 촬영 3일 전 이후 변경 불가 규칙 안내`);
  if (!file){ set('c5','wait','교안을 올리면 AI 가 규격을 점검합니다'); if (worst==='ok') worst='wait'; }
  else set('c5','ok','16:9 · 최소 글자 20pt · 과목표지(과목명·이름·메일) 확인');
  const v = document.getElementById('verdict'), btn = document.getElementById('go');
  const ready = worst !== 'wait' && name;
  const M = {ok:['ok','✓ 자동 승인 대상 — 신청 즉시 확정됩니다'],warn:['warn','! 담당자 확인 후 확정 (평균 반나절, 예시)'],
             no:['no','✕ 이 조건으로는 신청할 수 없어요'],wait:['wait','입력을 마치면 AI 가 바로 검토합니다']};
  const hasNo = [...document.querySelectorAll('.chk .s')].some(e=>e.classList.contains('no'));
  const state = hasNo ? 'no' : (!name ? 'wait' : worst);
  const [c,t] = M[state]; v.className = 'verdict ' + c; v.textContent = t; worst = state;
  btn.disabled = !ready || worst === 'no';
  btn.textContent = worst === 'warn' ? '담당자 확인 요청 보내기' : '예약 신청 · 자동 확정';
  const st = D.studios.find(x=>x.id===sid).name;
  document.getElementById('sum').innerHTML = sel ? `<b>${name||'교수명 미입력'}</b> · ${course==='__other'?'(직접 입력 과목)':course} ${wkno}주차<br>${st} · ${sel.split('|')[1]} ${D.slots[+sel.split('|')[2]]}` : '선택 전';
  window.__verdict = worst;
}
function submit(){
  const auto = window.__verdict === 'ok';
  document.getElementById('mt').textContent = auto ? '예약이 확정되었습니다' : '담당자 확인을 요청했습니다';
  document.getElementById('ms').textContent = auto ? 'AI 사전 검토를 모두 통과해 자동 승인됐어요. 아래 일정은 자동으로 진행됩니다.' :
    'AI 가 검토 사유와 추천 대안을 담당자에게 보냈어요. 확인되면 메일로 알려 드립니다.';
  document.getElementById('modal').classList.add('on');
}
document.addEventListener('DOMContentLoaded', ()=>{
  const st = document.getElementById('studio');
  st.innerHTML = D.studios.map(s=>`<option value="${s.id}">${s.name}</option>`).join('');
  document.getElementById('course').innerHTML = D.courses.map(c=>`<option>${c}</option>`).join('') + '<option value="__other">목록에 없는 과목 (직접 입력)</option>';
  ['studio','course','wkno','prof'].forEach(id=> document.getElementById(id).addEventListener('input', ()=>{ if(id==='studio') sel=null; draw(); check(); }));
  document.getElementById('prev').onclick = ()=>{ week = Math.max(0, week-1); draw(); };
  document.getElementById('next').onclick = ()=>{ week = Math.min(3, week+1); draw(); };
  document.getElementById('drop').onclick = e=>{ e.currentTarget.classList.add('ok'); e.currentTarget.innerHTML = '✓ 3주차_데이터로읽는경영학.pptx 업로드됨 (예시)'; check(); };
  document.getElementById('go').onclick = submit;
  document.getElementById('close').onclick = ()=> document.getElementById('modal').classList.remove('on');
  // 예시 입력 상태로 시작 (화면 시연용)
  week = 1; const m = monday(1); m.setDate(m.getDate()+1);
  sel = `s01|${m.toISOString().slice(0,10)}|1`;
  draw(); document.getElementById('drop').click();
});
</script>"""


def booking_page():
    types = "".join(f"<option>{t}</option>" for t in TYPES)
    weeks = "".join(f'<option value="{i}"{" selected" if i == 4 else ""}>{i}주차</option>' for i in range(1, 16))
    js = BOOK_JS.replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
    return head("HY FLIP 스튜디오 예약", CSS_A + CSS_DK + CSS_HOME + CSS_BOOK) + f"""<body>
{nav(True)}
<section class="band">{img('chroma', label='chroma')}<div class="w">
  <div class="rec"><i></i>SELF STUDIO · 12 ROOMS</div>
  <h1>셀프 스튜디오 예약</h1>
  <p>빈 시간을 고르고 교안을 올리면 AI 가 바로 검토합니다. 규칙에 맞으면 <b style="color:#E2C77F">즉시 자동 확정</b>되고, 구글 캘린더 등록과 안내 메일까지 자동으로 처리돼요.</p>
  <div class="steps3"><span><b>①</b>스튜디오·시간 선택</span><span><b>②</b>강의 정보·교안</span><span><b>③</b>AI 사전 검토 → 확정</span></div>
  <div class="demo">프로토타입 · 예시 데이터 · 실제 예약되지 않습니다</div>
</div></section>

<main class="w app">
  <div>
    <div class="card"><h2><span class="n">1</span>스튜디오와 시간</h2>
      <div class="row" style="justify-content:space-between">
        <label class="f">스튜디오 (교내 12실)<select id="studio"></select></label>
        <div class="wk"><button id="prev" aria-label="이전 주">‹</button><b id="wk"></b><button id="next" aria-label="다음 주">›</button></div>
      </div>
      <div class="scroll"><table class="cal" id="cal"></table></div>
      <div class="legend"><span><i style="background:#EEF5EE;border:1px solid #cfe5cf"></i>예약 가능</span><span><i style="background:#E8ECF2"></i>예약됨</span>
        <span><i style="background:#f3e9d2"></i>마감 (촬영 3일 전 이내)</span><span><i style="background:var(--hy)"></i>선택</span></div>
    </div>
    <div class="card"><h2><span class="n">2</span>강의 정보와 교안</h2>
      <div class="grid2">
        <label class="f">교수명<input id="prof" value="김한양" autocomplete="off"></label>
        <label class="f">소속<input value="경영대학 경영학부"></label>
        <label class="f">과목 (특수수업 승인 과목)<select id="course"></select></label>
        <label class="f">촬영 주차<select id="wkno">{weeks}</select></label>
        <label class="f">콘텐츠 유형<select>{types}</select></label>
        <label class="f">분량<select><option>1학점 · 25분 이상</option><option>1.5학점 · 40분 이상</option></select></label>
      </div>
      <label class="f" style="margin-top:14px">강의 교안 (PPT · 16:9 권장)<div class="drop" id="drop">{icon('down', 18)} 파일을 끌어다 놓거나 눌러서 선택</div></label>
      <label class="f" style="margin-top:14px">요청 사항<textarea rows="2" placeholder="예) 2~3개로 나눠 촬영하고 싶어요"></textarea></label>
    </div>
    <div class="card faq"><h2><span class="n">?</span>AI 도우미 — 자주 묻는 질문</h2>
      <div class="q">촬영 이틀 전인데 시간을 바꿀 수 있나요?</div>
      <div class="a"><b>AI</b> 촬영 3일 전부터는 변경할 수 없어요. 꼭 바꿔야 하면 아래 '담당자 연결'로 사유를 남겨 주세요. 비어 있는 가장 가까운 시간은 <b>목 13:00 경영대학 307호</b>입니다.</div>
      <div class="q">25분 분량을 한 번에 찍어야 하나요?</div>
      <div class="a"><b>AI</b> 아니요. 2~3개로 나눠 촬영·편집할 수 있어요. 요청 사항에 적어 주시면 편집 담당자에게 전달됩니다.</div>
    </div>
  </div>

  <aside class="side">
    <div class="card aibox"><h2><span class="n">3</span>AI 사전 검토</h2>
      <div class="summary" id="sum"></div>
      <ul class="chk">
        <li id="c1"><span class="s wait">·</span><div>시간 충돌<small></small></div></li>
        <li id="c2"><span class="s wait">·</span><div>승인 과목 여부<small></small></div></li>
        <li id="c3"><span class="s wait">·</span><div>스튜디오 이용 대상<small></small></div></li>
        <li id="c4"><span class="s wait">·</span><div>주차 중복 · 변경 마감 규칙<small></small></div></li>
        <li id="c5"><span class="s wait">·</span><div>교안 규격 (AI 점검)<small></small></div></li>
      </ul>
      <div class="verdict wait" id="verdict"></div>
      <button class="btn gold" id="go" disabled>예약 신청 · 자동 확정</button>
      <p class="note2" style="color:#9fb0c8">확정되면 구글 캘린더(스튜디오별)에 자동 등록되고, 확인 메일 · D-3 변경 마감 · D-1 준비물 안내가 자동 발송됩니다.</p>
    </div>
  </aside>
</main>

<div class="modal" id="modal"><div class="box2">
  <h3 id="mt"></h3><p id="ms" style="color:var(--muted)"></p>
  <ul class="tl">
    <li>구글 캘린더 등록<small>스튜디오 캘린더에 일정 생성 · 교수님 캘린더로 초대</small></li>
    <li>확인 메일 발송<small>위치 · 준비물(교안·복장) · 변경 규칙 안내</small></li>
    <li>D-3 변경 마감 알림<small>이후 변경은 담당자 협의</small></li>
    <li>D-1 리마인드<small>교안 최종본 확인 · 주차 정보 재안내</small></li>
    <li>촬영 후 편집 요청 연결<small>CMS 편집요청서 → 검수 → LMS 탑재 단계로 자동 이어짐</small></li>
  </ul>
  <button class="btn primary" id="close">확인</button>
</div></div>
{footer()}
{IMG_JS}
{js}
</body></html>
"""


QUEUE = [
    ("warn", "이OO 교수 · 공과대학", "공학수학 I · 6주차", "공과대학 본관 314호 · 10/27(화) 17:00–19:00",
     "같은 날 같은 교수 예약 3건(하루 최대 2건 규칙 초과)",
     "AI 추천: 10/28(수) 13:00 공업센터별관 716-2호 비어 있음",
     "교수님, 10/27 촬영이 이미 2건 예약되어 있어 3번째 일정은 10/28(수) 13:00 공업센터별관 716-2호로 안내드립니다. 괜찮으시면 '확정'을 눌러 주세요."),
    ("warn", "박OO 교수 · 국제학부", "현대사회와 윤리 (승인 목록에 없음)", "인문과학대학 101호 · 10/29(목) 11:00–13:00",
     "특수수업 승인 과목 목록에 없음 — 학사운영팀 승인 여부 확인 필요",
     "AI 확인: 2026-1 승인 목록 개정 이전 신청일 가능성",
     "교수님, 해당 과목의 스마트 과목 승인 여부를 확인 중입니다. 승인이 확인되는 대로 예약을 확정해 드리겠습니다."),
    ("no", "최OO 교수 · 자연과학대학", "일반화학 · 4주차 (변경 요청)", "자연과학대학 721호 · 10/21(수) → 10/22(목)",
     "촬영 2일 전 변경 요청 — '촬영 3일 전부터 변경 불가' 규칙",
     "AI 추천: 기존 일정 유지 또는 11/2(월) 이후 재예약",
     "교수님, 촬영 3일 전부터는 일정 변경이 어렵습니다. 불가피한 사유가 있으시면 회신 주세요. 담당자가 직접 조율하겠습니다."),
]
TODAY = [("09:00", "경영대학 307호", "김OO", "데이터로 읽는 경영학 원론 4주차", "a"),
         ("11:00", "경제금융관 508호", "정OO", "금융데이터분석 2주차", "a"),
         ("13:00", "공과대학 본관 314호", "이OO", "공학수학 I 5주차", "m"),
         ("15:00", "사회과학대학 107호", "한OO", "미디어와 사회 7주차", "a"),
         ("17:00", "인문과학대학 101호", "윤OO", "글쓰기의 기초 3주차", "c")]
UTIL = [("경영대학 307호", 82), ("경제금융관 508호", 76), ("공과대학 본관 314호", 71), ("사회과학대학 107호", 64),
        ("인문과학대학 101호", 58), ("자연과학대학 721호", 47), ("의과대학 본관 616호", 33), ("예술체육대학 232-1호", 21)]
LOG = [("09:02", "김OO 교수 예약 <b>자동 승인</b> → 캘린더 등록 → 확인 메일 발송"),
       ("09:15", "이OO 교수 예약 <b>검토 필요</b> (하루 3건) → 담당자 알림 · 대안 추천"),
       ("10:40", "D-1 리마인드 12건 발송 (교안·복장·위치)"),
       ("11:05", "윤OO 교수 예약 <b>취소</b> (D-4) → 대기자 정OO 교수에게 빈자리 알림"),
       ("13:30", "촬영 완료 3건 → CMS 편집요청서 자동 생성 링크 발송")]


def admin_page():
    q = "".join(
        f'<div class="qc {"no" if k == "no" else ""}"><div class="h"><b>{who}</b><span class="pill {"m" if k == "warn" else "c"}">'
        f'{"검토 필요" if k == "warn" else "규칙 위반"}</span></div>'
        f'<div style="font-size:14px;margin-top:4px">{course}<br><span style="color:var(--muted)">{when}</span></div>'
        f'<div class="why">AI 판단 사유 — {why}</div><div class="recm">{rec}</div>'
        f'<div class="draft"><b style="color:var(--navy)">AI 안내문 초안</b><br>{draft}</div>'
        f'<div class="acts"><button class="p">{"대안으로 확정" if k == "warn" else "안내문 발송"}</button><button>원래대로 승인</button><button>직접 연락</button></div></div>'
        for k, who, course, when, why, rec, draft in QUEUE)
    rows = "".join(f'<tr><td>{t}</td><td>{s}</td><td>{p} 교수</td><td>{c}</td>'
                   f'<td><span class="pill {k}">{ {"a": "자동 승인", "m": "담당자 승인", "c": "취소"}[k]}</span></td></tr>'
                   for t, s, p, c, k in TODAY)
    bars = "".join(f'<div>{n}<i class="{"lo" if v < 40 else ""}" style="width:{v}%"></i><span>{v}%</span></div>' for n, v in UTIL)
    log = "".join(f"<li><time>{t}</time><span>{m}</span></li>" for t, m in LOG)
    acts_js = """<script>document.querySelectorAll('.qc .acts button').forEach(b=>b.onclick=()=>{const q=b.closest('.qc');
q.classList.add('done');q.querySelector('.pill').textContent='처리 완료';});</script>"""
    return head("HY FLIP 예약 관리", CSS_A + CSS_DK + CSS_HOME + CSS_BOOK) + f"""<body>
{nav(True)}
<section class="band" style="padding-bottom:32px">{img('editing', label='editing')}<div class="w">
  <div class="rec"><i></i>ADMIN · 담당자 화면</div>
  <h1>스튜디오 예약 관리</h1>
  <p>규칙에 맞는 예약은 AI 가 자동으로 확정합니다. 담당자는 <b style="color:#E2C77F">예외만</b> 확인하면 돼요 — AI 가 사유·대안·안내문 초안까지 준비합니다.</p>
  <div class="demo">프로토타입 · 2026. 10. 19(월) 기준 예시 데이터</div>
</div></section>
<main class="w">
  <div class="kpis">
    <div class="kpi"><b>38</b><span>이번 주 예약</span></div>
    <div class="kpi"><b>87%</b><span>자동 승인 비율</span></div>
    <div class="kpi"><b>3</b><span>검토 대기</span></div>
    <div class="kpi"><b>6%</b><span>취소율 <em>리마인드 효과 측정 중</em></span></div>
    <div class="kpi"><b>0</b><span>이중 예약</span></div>
  </div>
  <div class="adm">
    <div><div class="card"><h2><span class="n">!</span>담당자 확인이 필요한 예약</h2>{q}
      <p class="note2">※ 위 3건 외 33건은 규칙을 모두 충족해 자동 확정됨 (예시)</p></div></div>
    <div>
      <div class="card"><h2><span class="n">{icon('calendar', 14)}</span>오늘 촬영 일정</h2>
        <div class="scroll"><table class="tbl"><thead><tr><th>시간</th><th>스튜디오</th><th>교수</th><th>강의</th><th>처리</th></tr></thead><tbody>{rows}</tbody></table></div>
        <p class="note2">구글 캘린더(스튜디오별)와 자동 동기화</p></div>
      <div class="card"><h2><span class="n">%</span>스튜디오 가동률 (이번 학기)</h2><div class="bars">{bars}</div>
        <p class="note2">가동률이 낮은 스튜디오는 홈페이지에서 우선 추천</p></div>
      <div class="card"><h2><span class="n">⟳</span>자동화 기록</h2><ul class="log">{log}</ul></div>
    </div>
  </div>
</main>
{footer()}
{IMG_JS}
{acts_js}
</body></html>
"""


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "booking.html").write_text(booking_page(), encoding="utf-8")
    (OUT / "admin.html").write_text(admin_page(), encoding="utf-8")
    print("booking/booking.html, booking/admin.html")


if __name__ == "__main__":
    main()
