---
name: hyflip-images
description: HY FLIP(한양 플립러닝 콘텐츠 개발 사업) 디자인 시안의 GPT 실사 이미지를 받아오거나(Figma 로 이미 생성된 원본) gpt-image-2 로 생성해 상세페이지·홈페이지 자리표시를 채우고, 검토·전달·저장까지 자동으로 진행한다. 사용자가 "GPT 이미지 생성해줘", "실사 이미지 만들어줘", "사진 채워줘", "자리표시 교체", "HY FLIP 이미지", "gpt-image", "사진 받아서 마무리해줘", "프로젝트 완료" 라고 하거나 design/hanyang-flip 의 사진 작업을 요청하면 사용한다. 특정 사진만 다시 만들어 달라는 요청("스튜디오 사진 다시")도 포함.
---

# HY FLIP 이미지 자동화

작업 폴더: `design/hanyang-flip/` (모든 명령은 이 폴더에서 실행)

## 0. 먼저: Figma 로 이미 만든 원본이 있는가? (2026-10-08 생성, 2026-10-15 만료)
`assets/figma_urls.json` 에 17개 주소(페이지 사진 13 + 목업 빈 배경 3 + 예비 1)가 있으면 **새로 생성하지 말고 받는다**:
```bash
bash scripts/images_pipeline.sh --figma     # 받기 → 로고 목업 합성 → 갤러리 → 스크린샷
```
- 종료코드 2 = `www.figma.com` 차단 → 허용 도메인 추가 안내(read_documentation environment.network) 후 멈춘다.
- 만료(2026-10-15 이후)면 Figma `generate_image`(model `gpt-image-2.5-sunburst`, planKey 는 `mcp__Figma__whoami` 로 확인)로
  manifest prompt 를 다시 생성해 `figma_urls.json` 을 갱신한 뒤 같은 명령을 실행한다.
- 목업 3장은 `shots/mock-*-guide.png` 를 보려면 `python3 scripts/composite_mockups.py --guide`. 위치가 어긋나면
  `assets/mockup_layout.json` 의 cx·cy·size 만 고쳐 다시 합성한다.
- 이어서 3·4단계(검토·전달)를 하고, `python3 scripts/build_index.py` 로 허브를 갱신한 뒤
  `bash scripts/images_pipeline.sh --figma --commit` 으로 저장한다. README 4단계를 ✅ 로 바꾼다.

아래 1·2단계는 OpenAI 키(`OPENAI_API_KEY`)로 직접 생성할 때만 쓴다.

## 1. 진단 (비용 없음)
```bash
python3 scripts/gen_image.py --check
```
- 종료코드 2 = 키 없음 또는 `api.openai.com` 차단 → 출력된 설정 안내를 쉬운 말로 전하고 멈춘다.
  `read_documentation` 도구(environment.network / environment.secrets)로 설정 화면 카드를 함께 띄운다.
  키를 채팅에 붙여넣으라고 하지 않는다.

## 2. 전체 실행
```bash
bash scripts/images_pipeline.sh
```
진단 → 로고 참고 PNG 확인 → 없는 사진만 생성(high, 3장 동시, 자동 재시도) → `assets/gallery.html` → 스크린샷 재촬영.
이미 있는 사진은 건너뛰므로 재실행해도 비용이 중복되지 않는다. 16장이라 몇 분 걸릴 수 있으니 진행 상황을 한 줄씩 알린다.

## 3. 검토 (반드시 직접 본다)
- 각 `assets/*.png` 를 Read 로 열어 확인한다:
  - 사진에 깨진 글자·가짜 한글·워터마크가 보이는지
  - 목업(`mock-*`)의 로고 모양이 `logo/png/logo-A.png`·`logo-D.png` 와 같은지
  - 인물 손·얼굴이 어색하지 않은지, 남색·회색 톤이 페이지와 어울리는지
- 문제가 있는 것만 다시 만든다 (그 한 장만 비용 발생):
  ```bash
  python3 scripts/gen_image.py <이름> --force   # OpenAI 직결일 때
  # Figma 경로: generate_image 로 그 1장만 다시 만들어 figma_urls.json 주소 교체 → assets/<이름>.png 삭제 → python3 scripts/fetch_figma.py
  ```
  같은 문제가 반복되면 `assets/manifest.json` 의 해당 prompt 에 제약을 한 줄 더 넣고 다시 만든다.
- `shots/home-final-desktop.png`, `shots/detail-final-desktop.png` 를 열어 사진이 자리에 들어갔는지 확인한다.

## 4. 전달·저장
- SendUserFile 로 `shots/gallery-desktop.png`, `shots/home-final-desktop.png`, `shots/detail-final-desktop.png`,
  `assets/gallery.html` 을 보낸다 (render).
- 다시 만든 사진이 있으면 스크린샷을 갱신한 뒤 저장한다:
  ```bash
  bash scripts/images_pipeline.sh --commit
  ```
- README 의 4단계 상태를 ✅ 로 바꾸고 함께 커밋한다.

## 답변 형식
조피디님께 한국어로 쉽게 설명하고, 끝에 🔑 핵심 키워드를 요약한다. 실패한 사진이 있으면 이름과 이유를 그대로 알린다.
