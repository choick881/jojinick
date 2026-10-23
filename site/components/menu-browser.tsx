"use client";
import { useState } from "react";
import type { Category } from "@/lib/catalog";
import { useT } from "./lang";

/** 분류 탭. 상품 카드는 서버에서 그려 넘겨받고(children 대신 분류별 묶음), 여기서는 보이기만 바꾼다. */
export function MenuBrowser({ categories, panels }: { categories: Category[]; panels: Record<string, React.ReactNode> }) {
  const [cur, setCur] = useState("all");
  const t = useT().menuPage;
  const tabs = [{ slug: "all", name: t.all }, ...categories];
  return (
    <>
      <div className="mb-4 flex gap-1.5 overflow-x-auto pb-1" role="group" aria-label={t.tabs}>
        {tabs.map((c) => (
          <button key={c.slug} type="button" aria-pressed={cur === c.slug} onClick={() => setCur(c.slug)}
            className={`whitespace-nowrap rounded-full border-[1.5px] px-3.5 py-1.5 text-[.85rem] ${cur === c.slug ? "border-brand bg-brand font-bold text-white" : "border-line bg-white"}`}>
            {c.name}
          </button>
        ))}
      </div>
      {tabs.map((c) => <div key={c.slug} hidden={cur !== c.slug}>{panels[c.slug]}</div>)}
    </>
  );
}
