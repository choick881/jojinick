// 사이트 주소와 검색 노출 관련 공통 값

/** 대표 도메인(가비아 구입, Vercel에서 ondamchan.kr → www로 이동) */
export const PRIMARY_DOMAIN = "https://www.ondamchan.kr";

const VERCEL_ENV = process.env.VERCEL_ENV ?? "development";

/** 운영 주소. NEXT_PUBLIC_SITE_URL > 운영 배포면 대표 도메인 > 미리보기 주소 > 로컬 */
export const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL ??
  (VERCEL_ENV === "production" ? PRIMARY_DOMAIN : process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : "http://localhost:3000");

/**
 * 주문 받기. 운영 배포는 Vercel 환경변수 NEXT_PUBLIC_ORDERING_OPEN=true를 넣기 전까지 '오픈 준비 중'(메뉴만 보기).
 * 미리보기·로컬은 테스트를 위해 항상 열려 있다. 서버에서만 읽는다(VERCEL_ENV는 서버 값).
 */
export const ORDERING_OPEN = process.env.NEXT_PUBLIC_ORDERING_OPEN === "true" || VERCEL_ENV !== "production";

/** Vercel 미리보기 배포는 검색에 노출하지 않는다 */
export const IS_INDEXABLE = VERCEL_ENV === "production";

export const absoluteUrl = (path: string) => new URL(path, SITE_URL).toString();

/** JSON-LD를 <script>에 넣을 때 '<'를 이스케이프해 스크립트 주입을 막는다 */
export const jsonLd = (data: object) => JSON.stringify(data).replace(/</g, "\\u003c");
