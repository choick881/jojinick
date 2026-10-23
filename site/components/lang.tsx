"use client";
// 브라우저 쪽 화면 언어. [lang] 레이아웃이 감싸 주고, 클라이언트 컴포넌트는 useT()로 사전을 받는다.
import { createContext, useContext } from "react";
import { getDict, localePath, type Dict, type Locale } from "@/lib/i18n";

const LangContext = createContext<Locale>("ko");

export function LangProvider({ lang, children }: { lang: Locale; children: React.ReactNode }) {
  return <LangContext.Provider value={lang}>{children}</LangContext.Provider>;
}

export const useLang = () => useContext(LangContext);
export const useT = (): Dict => getDict(useLang());
/** 현재 언어의 링크 주소 */
export function useHref() {
  const lang = useLang();
  return (path: string) => localePath(lang, path);
}
