# HY FLIP — 한양 플립러닝 콘텐츠 개발 사업 디자인 시안

> ※ 제안·포트폴리오용 시안입니다. 한양대학교 공식 교표·로고가 아니며, 교표 자리는 "UNIVERSITY EMBLEM" 자리표시로 둡니다.

## 진행 순서
| 단계 | 상태 | 결과물 |
|---|---|---|
| 0. 디자인 규칙 · 메타 프롬프트 | ✅ | `prompts/00~03_*.md`, `prompts/references.md` |
| 1. 로고 (1차 3시안 → 2차 변형·D/E/F) | ✅ 확정: D 인장 · A 모노그램 · E 타일 | `logo/logo-board.html`, `logo/logo-board-r2.html`, `logo/logo-{A..F}.svg` |
| 2. 사업 상세페이지 | ✅ 확정: A+C 리믹스 | `detail/detail-final.html` (비교용 시안 `detail-{A,B,C}.html`) |
| 3. 홈페이지 | ✅ 확정: 1+2 (영상 히어로 + 공지·일정 카드) | `home/home-final.html` (비교용 시안 `home-{1,2,3}.html`) |
| 4. GPT 실사 이미지 | ✅ 16장 완료 · 페이지 반영 (Figma 경유 gpt-image-2.5, 로고 목업 3장은 확정 로고 합성) | `assets/*.png` (`assets/gallery.html`) · 예비 `assets/extra/` · 목업 배경 `assets/blank/` |
| 5. 프로젝트 허브 | ✅ | `index.html` — 확정본·시안·문서 한눈에 |
| 6. Edu-Tech AI Lab 과제 제안서 | ✅ A4 3쪽 (제출 기한 2026-10-15) | `proposal/proposal.pdf` (원본 `proposal/proposal.html`, 다시 만들기 `node scripts/build_proposal.mjs`) |
| 7. 셀프 스튜디오 예약·승인 AI 자동화 | ✅ 개선방안 A4 3쪽 + 화면 프로토타입 (구글 캘린더 직접 입력 → 웹 예약·AI 사전 검토·규칙 충족 시 자동 승인, 예외만 담당자) · 제안서 M3에 반영 | `proposal/studio-booking.pdf` · `booking/booking.html`(교수용) · `booking/admin.html`(담당자용) — 다시 만들기 `python3 scripts/build_booking.py` |
| 8. 내려받기 묶음 | ✅ 단일 파일 뷰어(압축 안 풀고 열어도 사진·화면·PDF 정상) + 전체/핵심 ZIP | `python3 scripts/build_bundle.py` → `dist/HY_FLIP_한눈에보기.html`, `dist/HY_FLIP_전체결과물.zip`, `dist/HY_FLIP_핵심문서.zip` (dist 는 커밋 안 함) |
| 9. 영문 홈페이지 (외국인 교수자·유학생) | ✅ 영어·다국어 콘텐츠 개발 서비스 6종 · 유학생 학습 안내 · KO/EN 전환 링크 | `home/home-en.html` — 다시 만들기 `python3 scripts/build_home_en.py` |

## 파일 안내
- `prompts/` — Claude Design(claude.ai/design)에 그대로 붙여넣는 메타 프롬프트 + GPT 이미지 프롬프트
- `scripts/build_logos.py` — 로고 도형 정의(한 곳) → SVG·비교판 생성
- `scripts/site_kit.py` — 공통 문구·로고·아이콘·이미지 자리표시 / `build_detail.py`·`build_home.py` — 페이지 생성
- `scripts/gen_image.py` — gpt-image-2 로 실사 이미지 생성 (`assets/manifest.json` 목록, `--check` 진단, 자동 재시도·3장 동시)
- `scripts/images_pipeline.sh` — 진단 → 생성 → 갤러리 → 스크린샷 (→ `--commit` 저장) 원클릭
- `scripts/build_gallery.py` — `assets/gallery.html` (16장 한눈에 보기)
- `scripts/fetch_figma.py` — Figma 로 만든 원본 내려받기 (`assets/figma_urls.json`, 7일 유효)
- `scripts/composite_mockups.py` — 빈 명판·사인·명함 사진 + 확정 로고 합성 (`assets/mockup_layout.json`)
- `scripts/build_index.py` — 프로젝트 허브 `index.html`
- `scripts/shoot.mjs` — 데스크톱/모바일 스크린샷 + 로고 PNG 내보내기 → `shots/`

## 다시 만들기
```bash
python3 scripts/build_logos.py                 # 로고 SVG + 비교판
node scripts/shoot.mjs --logos logo/logo-board.html   # PNG + 스크린샷
python3 scripts/build_detail.py && python3 scripts/build_home.py   # 상세·홈 HTML
python3 scripts/gen_image.py --list            # GPT 이미지 목록
python3 scripts/gen_image.py --all             # 생성 (OPENAI_API_KEY 필요)
```

## GPT 이미지 — 완료 (2026-10-08)
- 페이지 사진 13장 + 로고 목업 3장 = **16장**, 모두 상세페이지·홈페이지·갤러리에 반영됨
- 생성: Figma `generate_image` 의 GPT 이미지 모델 `gpt-image-2.5-sunburst` (OpenAI 키 없이)
- 로고 목업: AI 로 *빈* 명판·사인·명함 사진을 만들고 확정 로고를 정확히 합성 (`scripts/composite_mockups.py`, 위치는 `assets/mockup_layout.json`)
- 라이트보드·토론수업 사진은 한국인 교수·학생으로 재생성, 처음 버전은 `assets/extra/` 에 예비 보관
- 사진 1장 교체: Figma 로 다시 만든 주소를 `assets/figma_urls.json` 에 넣고 해당 png 삭제 → `bash scripts/images_pipeline.sh --figma`

## (참고) OpenAI 키로 직접 생성하는 방법
1. **한 번만 설정** (세션 상단 클라우드 환경 메뉴 → Edit)
   - 네트워크 → Custom → 허용 도메인에 `api.openai.com` 추가 (기본 패키지 목록 유지)
   - 환경변수 `OPENAI_API_KEY` 등록
2. **새 세션**을 열면 "HY FLIP: GPT 사진 16장 대기 중" 안내가 나옵니다.
3. **"GPT 이미지 생성해줘"** 라고 말하면 `.claude/skills/hyflip-images` 스킬이
   생성(high) → 페이지 자동 반영 → 사진 검토(문제 있는 것만 재생성) → 스크린샷 전달 → 커밋까지 진행합니다.

직접 실행할 때: `bash scripts/images_pipeline.sh` (저장까지: `--commit`) · 진단만: `python3 scripts/gen_image.py --check`
