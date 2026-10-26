// 언어별 주소 규칙. 한국어는 지금 주소 그대로(/menu), 영어는 /en을 붙인다(/en/menu).
// 내부적으로 한국어 화면은 app/[lang]의 lang=ko로 그리므로, proxy.ts가 /menu → /ko/menu로 몰래 바꿔(rewrite) 보낸다.

export const LOCALES = ["ko", "en"] as const;
export type Locale = (typeof LOCALES)[number];
export const DEFAULT_LOCALE: Locale = "ko";

export const hasLocale = (v: string): v is Locale => (LOCALES as readonly string[]).includes(v);

/** 화면 안 링크 주소: ko → 그대로, en → /en 붙이기 */
export function localePath(lang: Locale, path: string): string {
  if (lang === DEFAULT_LOCALE) return path;
  return path === "/" ? `/${lang}` : `/${lang}${path}`;
}

/** 주소에서 언어를 떼어 낸다: /en/menu → { lang: "en", path: "/menu" }, /menu → { lang: "ko", path: "/menu" } */
export function splitLocale(pathname: string): { lang: Locale; path: string } {
  const m = pathname.match(/^\/(en)(\/.*)?$/);
  if (m) return { lang: "en", path: m[2] || "/" };
  return { lang: DEFAULT_LOCALE, path: pathname || "/" };
}

/** 같은 화면의 다른 언어 주소(언어 바꾸기 버튼) */
export const switchLocalePath = (pathname: string, to: Locale) => localePath(to, splitLocale(pathname).path);

export type LocaleRoute = { action: "pass" } | { action: "rewrite"; path: string } | { action: "redirect"; path: string };

/** proxy.ts가 쓰는 판정. 관리자·API·파일(확장자 있는 주소)은 손대지 않는다 */
export function routeLocale(pathname: string): LocaleRoute {
  if (/^\/(admin|api|_next)(\/|$)/.test(pathname) || /\/[^/]+\.[a-z0-9]+$/i.test(pathname)) return { action: "pass" };
  if (/^\/en(\/|$)/.test(pathname)) return { action: "pass" };
  const ko = pathname.match(/^\/ko(\/.*)?$/);
  if (ko) return { action: "redirect", path: ko[1] || "/" }; // /ko/menu → /menu (같은 화면 주소를 하나로)
  return { action: "rewrite", path: pathname === "/" ? "/ko" : `/ko${pathname}` };
}
