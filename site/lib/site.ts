// 사이트 주소와 검색 노출 관련 공통 값

/** 운영 주소. NEXT_PUBLIC_SITE_URL > Vercel 운영 도메인 > 로컬 */
export const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL ??
  (process.env.VERCEL_PROJECT_PRODUCTION_URL ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}` : "http://localhost:3000");

/** Vercel 미리보기 배포는 검색에 노출하지 않는다 */
export const IS_INDEXABLE = (process.env.VERCEL_ENV ?? "production") === "production";

export const absoluteUrl = (path: string) => new URL(path, SITE_URL).toString();

/** JSON-LD를 <script>에 넣을 때 '<'를 이스케이프해 스크립트 주입을 막는다 */
export const jsonLd = (data: object) => JSON.stringify(data).replace(/</g, "\\u003c");
