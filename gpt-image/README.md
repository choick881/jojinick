# GPT 이미지 생성기

OpenAI 이미지 API(`gpt-image-1` 계열)로 SNS 카드뉴스·포스터·유튜브 썸네일·로고 시안을 만드는 도구입니다.
실버 헬스케어·노인스포츠·자선 캠페인용 한국어 프리셋이 들어 있습니다.

## 준비물

- OpenAI API 키: https://platform.openai.com/api-keys
- gpt-image 모델은 OpenAI 조직 인증(Verify Organization)이 필요할 수 있습니다.

## 1. 웹 버전 (코딩 없이 사용)

1. `index.html` 파일을 크롬/엣지로 엽니다.
2. API 키 입력 → 프리셋 선택 또는 프롬프트 작성 → **이미지 생성**.
3. 결과 이미지의 **다운로드**를 눌러 저장합니다.

| 기능 | 설명 |
|---|---|
| 프리셋 6종 | 카드뉴스 표지, 노인스포츠 포스터, 유튜브 썸네일, 요양시설 안내, 자선 캠페인, 로고 시안 |
| 크기 | 정사각형(피드) / 세로(포스터·스토리) / 가로(썸네일) |
| 참고 이미지 | 사진을 올리면 편집 모드로 수정·합성 |
| 투명 배경 | 로고·스티커용 (PNG/WEBP) |

> API 키는 브라우저에서 OpenAI로 직접 전송됩니다. 개인 PC에서만 사용하고, 공용 PC에서는 '기억하기'를 끄세요.

## 2. 파이썬 버전 (대량 생성)

```bash
pip install openai
export OPENAI_API_KEY=sk-...

# 한 장
python generate.py "공원에서 스트레칭하는 시니어 부부, 수채화 스타일"

# prompts.txt 의 프롬프트를 한 번에 생성 (세로, 고품질)
python generate.py -f prompts.txt --size 1024x1536 --quality high

# 참고 이미지 편집
python generate.py "이 사진 오른쪽 아래에 로고를 자연스럽게 넣어줘" --image photo.png --image logo.png
```

결과는 `output/` 폴더에 저장됩니다.

## 프롬프트 작성 팁

- **주제 + 인물 + 배경 + 스타일 + 색감 + 문구** 순서로 쓰면 결과가 안정적입니다.
- 이미지 속 글자는 큰따옴표로 감싸고 짧게 (10자 내외 권장).
- 시니어 대상 콘텐츠는 "큰 요소, 단순한 구도, 높은 대비"를 넣으면 가독성이 좋아집니다.
- 실존 인물·상표는 넣지 마세요.

## 비용 참고

품질 `low` < `medium` < `high` 순으로 비용과 시간이 늘어납니다. 시안은 `low`로 여러 장 뽑고, 확정안만 `high`로 다시 만드는 방식을 권장합니다.
최신 요금은 https://openai.com/api/pricing 에서 확인하세요.
