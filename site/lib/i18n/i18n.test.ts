import { describe, expect, it } from "vitest";
import { en } from "./en";
import { alternates, getDict, localePath, routeLocale, splitLocale, switchLocalePath } from "./index";
import { ko } from "./ko";

/** 사전의 모든 문구 경로(함수는 이름만) */
function leaves(v: unknown, path = ""): string[] {
  if (typeof v === "function" || typeof v === "string") return [path];
  if (Array.isArray(v)) return v.flatMap((x, i) => leaves(x, `${path}[${i}]`));
  if (v && typeof v === "object") return Object.entries(v).flatMap(([k, x]) => leaves(x, path ? `${path}.${k}` : k));
  return [path];
}
const strings = (v: unknown): string[] =>
  typeof v === "string" ? [v] : Array.isArray(v) ? v.flatMap(strings) : v && typeof v === "object" ? Object.values(v).flatMap(strings) : [];

describe("사전", () => {
  it("영어 사전은 한국어 사전과 같은 문구를 모두 갖는다(배열 길이 포함)", () => {
    expect(leaves(en).sort()).toEqual(leaves(ko).sort());
  });
  it("영어 문구에 한글이 섞여 있지 않다(언어 바꾸기 버튼 '한국어'만 예외)", () => {
    const allowed = new Set([en.nav.switchTo, en.nav.switchLabel]);
    const hangul = strings({ ...en, softness: Object.values(en.softness) }).filter((s) => /[가-힣]/.test(s) && !allowed.has(s));
    expect(hangul).toEqual([]);
  });
  it("비어 있으면 안 되는 문구가 비어 있지 않다", () => {
    const empty = leaves(en).filter((p) => !/prevails|payNotice/.test(p)).filter((p) => {
      const v = p.split(/\.|\[|\]/).filter(Boolean).reduce<unknown>((o, k) => (o as Record<string, unknown>)[k], en);
      return typeof v === "string" && !v.trim();
    });
    expect(empty).toEqual([]);
  });
  it("가격 표시", () => {
    expect(getDict("ko").money(13900)).toBe("13,900원");
    expect(getDict("en").money(13900)).toBe("₩13,900");
  });
  it("부드러움 단계: 한국어 값 → 영어 이름", () => {
    expect(en.softness["잇몸으로"]).toBe("Gum-soft");
    expect(Object.keys(en.softness)).toEqual(Object.keys(ko.softness));
  });
});

describe("주소", () => {
  it("localePath: 한국어는 그대로, 영어는 /en", () => {
    expect(localePath("ko", "/menu")).toBe("/menu");
    expect(localePath("en", "/menu")).toBe("/en/menu");
    expect(localePath("en", "/")).toBe("/en");
  });
  it("splitLocale·switchLocalePath", () => {
    expect(splitLocale("/en/menu/japchae")).toEqual({ lang: "en", path: "/menu/japchae" });
    expect(splitLocale("/en")).toEqual({ lang: "en", path: "/" });
    expect(splitLocale("/menu")).toEqual({ lang: "ko", path: "/menu" });
    expect(splitLocale("/english")).toEqual({ lang: "ko", path: "/english" });
    expect(switchLocalePath("/menu/japchae", "en")).toBe("/en/menu/japchae");
    expect(switchLocalePath("/en/silver", "ko")).toBe("/silver");
    expect(switchLocalePath("/en", "ko")).toBe("/");
  });
  it("proxy 판정: 한국어 rewrite, 영어 통과, /ko 이동, 관리자·API·파일 제외", () => {
    expect(routeLocale("/")).toEqual({ action: "rewrite", path: "/ko" });
    expect(routeLocale("/menu/japchae")).toEqual({ action: "rewrite", path: "/ko/menu/japchae" });
    expect(routeLocale("/en")).toEqual({ action: "pass" });
    expect(routeLocale("/en/menu")).toEqual({ action: "pass" });
    expect(routeLocale("/ko/menu")).toEqual({ action: "redirect", path: "/menu" });
    expect(routeLocale("/ko")).toEqual({ action: "redirect", path: "/" });
    for (const p of ["/admin", "/admin/x", "/api/orders", "/_next/static/a.js", "/photos/a.jpg", "/sitemap.xml", "/robots.txt"]) expect(routeLocale(p), p).toEqual({ action: "pass" });
    expect(routeLocale("/english")).toEqual({ action: "rewrite", path: "/ko/english" });
  });
  it("hreflang: 한국어가 기본(x-default)", () => {
    expect(alternates("en", "/menu")).toEqual({ canonical: "/en/menu", languages: { ko: "/menu", en: "/en/menu", "x-default": "/menu" } });
    expect(alternates("ko", "/").canonical).toBe("/");
  });
});
