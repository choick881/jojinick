// 화면 언어 사전. 서버·브라우저 양쪽에서 쓴다(문구 안에 함수가 있어 props로 넘기지 않고 각자 불러온다).
import { en } from "./en";
import { ko, type Dict } from "./ko";
import { localePath, type Locale } from "./routing";

export type { Dict } from "./ko";
export * from "./routing";

const DICTS: Record<Locale, Dict> = { ko: ko as Dict, en };

export const getDict = (lang: Locale): Dict => DICTS[lang];

/** 페이지 메타데이터의 대표 주소와 언어별 주소(hreflang) */
export function alternates(lang: Locale, path: string) {
  return { canonical: localePath(lang, path), languages: { ko: path, en: localePath("en", path), "x-default": path } };
}
