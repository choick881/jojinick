"""영문 홈페이지 → home/home-en.html  (외국인 교수자·유학생용)

홈 확정안(home-final)과 같은 톤 — 다크 영상 히어로 + 바로가기 + 라이트 본문 — 으로,
영어·다국어 콘텐츠 개발 서비스와 유학생 학습 안내를 더했습니다.
스타일은 build_home.css() 를 그대로 씁니다.

  python3 scripts/build_home_en.py
"""

from pathlib import Path

from build_detail import thumb
from build_home import PLAY_BTN, css
from site_kit import IMG_JS, emblem_ph, head, icon, img, logo

OUT = Path(__file__).resolve().parent.parent / "home"
DETAIL = "../detail/detail-final.html"
BOOKING = "../booking/booking.html"
KO_NOTE = "Korean form · English guide available"

MENU = [("About", "#about"), ("Services", "#services"), ("For Students", "#students"),
        ("Studios", "#studios"), ("FAQ", "#faq")]
QUICK = [("arrow", "Request Production", f"{DETAIL}#apply", KO_NOTE),
         ("calendar", "Book a Studio", BOOKING, "AI pre-check · instant confirmation"),
         ("cc", "Multilingual Captions", "#services", "Korean · English · Chinese"),
         ("help", "FAQ", "#faq", "Language, cost, copyright")]
SERVICES = [("camera", "English Lecture Video Production", "Plan, film and edit your course videos in English with a producer, camera crew and editor."),
            ("cc", "Bilingual AI Captions (KO/EN)", "AI drafts captions on filming day; our editors proofread every line before release."),
            ("mic", "AI Multilingual Dubbing", "Create English, Korean or Chinese versions of a lecture in a voice close to your own."),
            ("book", "Instructional Design in English", "Design pre-class videos and in-class activities together with an English-speaking consultant."),
            ("doc", "AI Summaries & Quizzes", "Each episode comes with an English summary and check-up quiz for self-study."),
            ("calendar", "Studio Booking with English Guide", "Pick an open slot online; rules are checked automatically and you get confirmation and reminders.")]
FLIP_ROWS = [("Before class", "No preview · read the textbook", "Learn key concepts from short videos"),
             ("In class", "Listen to a one-way lecture", "Discuss, practice and solve problems"),
             ("After class", "Do assignments alone", "Go deeper with feedback")]
STUDENT = [("Watch before class", "Short videos (10–15 min) with chapters, so you can pause, replay and study at your own pace."),
           ("Choose your caption language", "Turn on Korean, English or Chinese captions, and use the AI summary to check key terms."),
           ("Join the discussion in class", "Come prepared with questions — class time is for discussion, teamwork and practice.")]
STEPS = [("01", "Apply", "Submit the online request form", "1 day", "Syllabus"),
         ("02", "Plan", "Instructional design consulting · episode outline · script", "1–2 weeks", "Lecture notes · slides"),
         ("03", "Film", "Professional studio with teleprompter support", "2 hrs per session", "Just your schedule"),
         ("04", "Edit & Review", "AI captions · graphics · final review, then upload to the LMS", "2–3 weeks", "One review round")]
STUDIOS = [("studio-hero", "Lecture Studio", "Sound-treated · teleprompter · 3-point lighting"),
           ("chroma", "Chroma-key Studio", "Virtual classroom backgrounds"),
           ("lightboard", "Lightboard", "Write while facing the camera"),
           ("editing", "Editing Suite", "Professional editors on site")]
COURSES = [("thumb-3", "Global Communication English", "International Studies · 10 episodes"),
           ("thumb-1", "Principles of Management with Data", "Business · 12 episodes · EN captions"),
           ("thumb-2", "Engineering Mathematics I — Lightboard", "Engineering · 15 episodes · EN captions"),
           ("thumb-4", "Media Literacy in the Age of AI", "General Education · 8 episodes · KO/EN")]
FAQ = [("Can I produce my course entirely in English?", "Yes. Planning meetings, scripts, filming guidance and captions can all be in English."),
       ("Which caption and dubbing languages are supported?", "Korean, English and Chinese to start. Other languages can be added on request. (Example)"),
       ("Is there a cost?", "Selected faculty receive full support for planning, filming and editing. (Example)"),
       ("Who owns the finished videos?", "Copyright is shared by the instructor and the university under the agreement, for use in the LMS and open courses."),
       ("I am an international student. How do I use these videos?", "Open the course in the LMS, turn on captions in your language, and use the chapters and summary to review.")]
CONTACT = "HY FLIP Office · +82-2-0000-0000 · hyflip@example.ac.kr"
NOTICE = ("※ This page is a design proposal. Figures, testimonials and contacts are examples. "
          "It is not the official emblem or logo of Hanyang University.")


def sh(no, title, lead=""):
    return (f'<div class="sh"><div class="no">{no}</div><div><h2>{title}</h2>'
            f'{f"<p>{lead}</p>" if lead else ""}</div></div>')


def nav():
    links = "".join(f'<a href="{h}">{t}</a>' for t, h in MENU)
    return (f'<header class="nav-dk"><div class="w">'
            f'<a class="brand" href="#">{logo("mark", 40)}<span><b>HY FLIP</b><small>Hanyang Flipped Learning Content Lab</small></span></a>'
            f'<nav>{links}</nav>{emblem_ph()}<a class="btn gold sm" href="#apply">Request<span class="xs-hide"> Production</span></a>'
            f'<a class="lang" href="home-final.html" lang="ko" title="한국어">한국어</a></div></header>')


def page():
    quick = "".join(f'<a href="{h}">{icon(i, 30)}<b>{t}</b><span>{d}</span><span class="go">{icon("arrow", 18)}</span></a>'
                    for i, t, h, d in QUICK)
    services = "".join(f'<li>{icon(i, 40)}<div><h3>{t}</h3><p>{d}</p></div></li>' for i, t, d in SERVICES)
    rows = "".join(f'<tr><td>{a}</td><td>{b}</td><td class="on">{c}</td></tr>' for a, b, c in FLIP_ROWS)
    student = "".join(f'<li><div class="num">0{i}</div><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(STUDENT, 1))
    frames = "".join(f'<div class="dk-frame"><div class="take">TAKE {n}</div><div class="n">{n}</div><h3>{t}</h3><p>{d}</p>'
                     f'<div class="meta"><b>Time</b> {dur}<br><b>You bring</b> {prep}</div></div>' for n, t, d, dur, prep in STEPS)
    studios = "".join(f'<figure>{img(k)}<figcaption><b>{t}</b><span>{d}</span></figcaption></figure>' for k, t, d in STUDIOS)
    courses = "".join(f'<article class="case">{thumb(k)}<h3>{t}</h3><span>{m} (Sample)</span></article>' for k, t, m in COURSES)
    faq = "".join(f'<details class="faq"><summary>{q}{icon("plus", 20, "pm")}</summary><p>{a}</p></details>' for q, a in FAQ)
    play = PLAY_BTN.replace("사업 소개 영상 보기", "Watch the intro video")
    return head("HY FLIP — English", css() + EN_CSS, lang="en") + f"""<body>
{nav()}
<section class="dk-hero tall">{img('studio-hero', label='studio-hero (lecture filming)')}<div class="w">
  <div class="rec"><i></i>NOW RECRUITING · 2026 HY FLIP · ENGLISH SERVICES</div>
  <h1>Flip the Class,<br><span>Deepen the Learning</span></h1>
  <p class="sub">HY FLIP helps international faculty turn their lectures into flipped-learning video courses — in English and other languages — and helps international students learn with them.</p>
  <div class="btns"><a class="btn gold" href="#apply">Request Production {icon('arrow', 18)}</a>{play}</div>
</div></section>
<div class="w"><nav class="quick" aria-label="Quick links">{quick}</nav></div>

<section class="s" id="services" style="padding-top:88px"><div class="w">
  {sh('SERVICES', 'Content Development Services for International Faculty', 'From planning to multilingual release — you focus on teaching, we handle production in your language.')}
  <ul class="ai">{services}</ul>
</div></section>

<section class="s alt" id="about"><div class="w">
  {sh('ABOUT', 'What is flipped learning?', 'Concepts first on video, then discussion and practice in class. Flipping the order changes the depth of learning.')}
  <div class="flip">{img('flipped-class', label='flipped-class (discussion class)')}
    <table class="cmp"><thead><tr><th></th><th>Traditional class</th><th class="on">Flipped learning</th></tr></thead><tbody>{rows}</tbody></table>
  </div>
</div></section>

<section class="s" id="students"><div class="w">
  {sh('STUDENTS', 'For International Students', 'Three steps to study well with HY FLIP courses.')}
  <ul class="who">{student}</ul>
</div></section>

<section class="dk-band" id="process"><div class="w">
  {sh('HOW IT WORKS', 'Four takes from request to release', 'About six weeks on average. Just bring your materials — we take care of the rest.')}
  <div class="dk-strip"><div class="dk-frames">{frames}</div></div>
</div></section>

<section class="s" id="studios"><div class="w">
  {sh('STUDIOS', 'Studios & Equipment', 'Broadcast-quality filming spaces you can book around your schedule.')}
  <div class="bento four">{studios}</div>
  <div class="more"><a href="{BOOKING}">Book a studio {icon('arrow', 18)}</a></div>
</div></section>

<section class="s alt" id="courses"><div class="w">
  {sh('COURSES', 'Featured Courses with English Support')}
  <div class="cases four">{courses}</div>
</div></section>

<section class="s" id="faq"><div class="w">
  {sh('FAQ', 'Frequently Asked Questions')}
  <div class="faq-wrap">{faq}</div>
</div></section>

<section class="dk-cta" id="apply">{img('campus-dusk', label='campus-dusk (campus at dusk)')}{logo('seal', 620, 'seal-wm')}<div class="w">
  <div class="eyebrow">APPLY</div>
  <h2>Flip your class next semester</h2><p>The request form takes about five minutes. A producer will contact you within a week — in English if you prefer.</p>
  <div class="btns"><a class="btn gold" href="{DETAIL}#apply">Request Production {icon('arrow', 18)}</a>
    <a class="btn wline" href="{BOOKING}">Book a Studio</a></div>
  <small>{KO_NOTE} · {CONTACT} (Example)</small>
</div></section>
<footer><div class="w"><span class="brand">{logo("seal", 44)}
  <span><b style="font:900 18px var(--serif);letter-spacing:.06em;display:block">HY FLIP Office</b>
  <small style="color:#9fb3cc">{CONTACT} (Example)</small></span></span>{emblem_ph()}
  <p>{NOTICE}</p></div></footer>
{IMG_JS}
</body></html>
"""


EN_CSS = """
.bento.four{grid-template-columns:repeat(4,1fr);grid-auto-rows:300px}
.bento.four figure{grid-column:auto!important;grid-row:auto!important}
@media (max-width:960px){.bento.four{grid-template-columns:1fr 1fr}}
@media (max-width:520px){.bento.four{grid-template-columns:1fr;grid-auto-rows:220px} .xs-hide{display:none}}
"""


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "home-en.html").write_text(page(), encoding="utf-8")
    print("home/home-en.html")


if __name__ == "__main__":
    main()
