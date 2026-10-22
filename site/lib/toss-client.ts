// 토스페이먼츠 v2 결제위젯 클라이언트 키. 기본값은 토스 공식 문서의 공개 테스트 키(gck)다.
// 운영 전환 때 Vercel 환경변수 NEXT_PUBLIC_TOSS_CLIENT_KEY를 live 키로 바꾼다(시크릿 키와 짝을 맞춘다).
export const TOSS_CLIENT_KEY = process.env.NEXT_PUBLIC_TOSS_CLIENT_KEY?.trim() || "test_gck_docs_Ovk5rk1EwkEbP0W43n07xlzm";

export const isTestMode = TOSS_CLIENT_KEY.startsWith("test_");
