import "server-only";
// 서버 컴포넌트에서 지금 화면 언어 읽기(app/[lang] 루트 레이아웃의 lang 값). props로 내려보내지 않아도 된다.
import { lang } from "next/root-params";
import { getDict, hasLocale, type Dict, type Locale } from "./index";

export async function getLang(): Promise<Locale> {
  const l = await lang();
  return l && hasLocale(l) ? l : "ko";
}

export async function getT(): Promise<Dict> {
  return getDict(await getLang());
}
