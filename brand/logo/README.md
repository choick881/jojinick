# 온담찬 로고 (확정 2026-10-21)

- **기본**: C안 원형 엠블럼 — 두 손이 받친 김 오르는 그릇 (`logo.svg`)
- **가로형**: A안 김 오르는 밥그릇 + 글자 (`logo-horizontal.svg`)
- 사용 안내 페이지: `guide.html` (바탕별 버전, 최소 크기, 색, 규칙, 파일 목록)

| 파일 | 내용 |
|---|---|
| `logo.svg` / `logo-reverse.svg` / `logo-mono.svg` | 엠블럼 컬러 / 반전(어두운 바탕) / 단색(먹) |
| `logo-horizontal.svg` / `-reverse.svg` / `-mono.svg` | 가로형 컬러 / 반전 / 단색 |
| `symbol.svg` | 글자 없는 원형 심볼 (96px·20mm보다 작을 때) |
| `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`, `png/icon-512.png` | 탭·홈 화면 아이콘 |
| `og-image.png` | 링크 공유 이미지 1200×630 |
| `png/*.png` | SVG를 못 쓰는 곳(캔바, 카카오 채널 등)용 투명 PNG |

색: 된장 갈색 #7A4E2D · 고추 주홍 #C8462B(김 한 줄·점 두 개만) · 크림 #FBF6EC · 먹 #2B211A

## 다시 만들기
글자는 서체 윤곽선(path)으로 들어가 있다. 모양을 고칠 때는 `src/build.py`를 수정하고 아래를 실행한다.

```bash
pip install fonttools
python3 brand/logo/src/build.py       # SVG 8종 + guide.html
node brand/logo/src/render-png.cjs    # PNG (playwright 필요)
```

`src/*-subset.ttf`는 Noto Serif KR Black / Noto Sans KR Bold에서 로고 글자만 뽑은 부분 서체(SIL OFL 1.1).
시안 기록: `compare.html`, `drafts/`
