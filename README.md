# jojinick — 양주 무인 반찬가게 브랜드 · 홈페이지 프로젝트

조피디의 창업 프로젝트 작업 레포입니다. 로고 → 상품 상세페이지 → 홈페이지(사업소개·상품·상세·결제)를 `homepage-builder-kr` 스킬로 만듭니다.

## 스킬 (전역 설정)

| 위치 | 용도 |
|---|---|
| `.claude/skills/homepage-builder-kr/` | 홈페이지 빌더 스킬 v0.4.0 ([wonhp1/claude-skills](https://github.com/wonhp1/claude-skills) 기반 + 보강) |
| `.claude/skills/feature-planner/` | 홈페이지 빌더가 Phase 2.5에서 호출하는 계획 스킬 |
| `scripts/install-global-skills.sh` | 내 PC의 `~/.claude/skills/`로 복사 → 모든 프로젝트에서 `/homepage-builder-kr` 사용 |
| `dist/*.zip` | claude.ai → 설정 → Capabilities → Skills에 올리는 업로드용 파일 (웹·앱·클라우드 세션 공통 전역) |

원본 대비 보강 내용 (v0.3.0 → v0.4.0)
- 토스페이먼츠 **v2 결제위젯**(`@tosspayments/tosspayments-sdk`)으로 교체. 서버 금액 재검증, `orders` 개인정보 비공개 RLS
- **Phase 1.5** 메타프롬프트·레퍼런스·로고 3안 → SVG 확정 (`references/brand-assets-gpt-image.md`)
- **Phase 5.5** 한국형 세로 상세페이지 (`references/detail-page.md`)
- `scripts/gen-image.mjs` — OpenAI `gpt-image-2` 이미지 생성 CLI (의존성 없음, 프록시 자동 대응)
- 인터뷰 Round 7(브랜드·로고), Round 8(대표 상품 상세) 추가

### GPT 이미지 생성 준비

```bash
export OPENAI_API_KEY=...   # 클라우드 세션이면 환경 설정 → 환경변수
node .claude/skills/homepage-builder-kr/scripts/gen-image.mjs --help
```

Claude Code 클라우드 환경에서는 Network access의 Allowed domains에 `api.openai.com`(결제 테스트 시 `js.tosspayments.com`, `api.tosspayments.com`, `log.tosspayments.com`)을 추가해야 합니다.
