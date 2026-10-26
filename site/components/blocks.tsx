// 여러 페이지에서 함께 쓰는 섹션 조각
import Link from "next/link";
import type { StoreStatus } from "@/lib/catalog";
import { localePath } from "@/lib/i18n";
import { getLang, getT } from "@/lib/i18n/server";
import { PHOTOS } from "@/lib/photos";
import { Lines } from "./lines";
import { PhotoSlot } from "./photo-slot";

export function SectionHead({ eyebrow, title, lead }: { eyebrow: string; title: React.ReactNode; lead?: React.ReactNode }) {
  return (
    <div className="mb-6 grid gap-2">
      <span className="eyebrow">{eyebrow}</span>
      <h2 className="h2">{title}</h2>
      {lead && <p className="lead">{lead}</p>}
    </div>
  );
}

/** 홈 2안에서 가져온 매장 현황판 */
export async function StoreBoard({ status, total, onSale }: { status: StoreStatus; total: number; onSale: number }) {
  const t = (await getT()).board;
  const pct = total ? Math.round((onSale / total) * 100) : 0;
  return (
    <div className="grid gap-2.5 rounded-[var(--r)] bg-ink px-5 py-4 text-paper" aria-label={t.label}>
      <div className="flex flex-wrap items-baseline justify-between gap-2 text-[.76rem] text-[#CDBEAB]">
        <span>{t.done}</span>
        {status.isExample && <span>{t.example}</span>}
      </div>
      <div className="num text-[1.15rem] font-extrabold leading-tight sm:text-[1.35rem] md:text-[1.5rem]">
        {status.madeAt} · <em className="not-italic text-[#F2A58A]">{t.onSale(total, onSale)}</em>{t.onSaleSuffix}
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-[#4A3C31]" aria-hidden="true"><i className="block h-full bg-[#F2A58A]" style={{ width: `${pct}%` }} /></div>
      <small className="text-[.76rem] text-[#CDBEAB]">{t.pickup}</small>
    </div>
  );
}

export function Steps({ items }: { items: { title: string; body: string }[] }) {
  return (
    <ol className="grid gap-3 md:grid-cols-3">
      {items.map((s, i) => (
        <li key={s.title} className="card grid content-start gap-1.5 p-5">
          <span className="grid size-[34px] place-items-center rounded-full bg-brand text-[.85rem] font-extrabold text-white">{i + 1}</span>
          <b>{s.title}</b>
          <span className="text-[.88rem] text-muted">{s.body}</span>
        </li>
      ))}
    </ol>
  );
}

export async function Promises() {
  const items = (await getT()).promises;
  return (
    <ul className="grid gap-3 md:grid-cols-3">
      {items.map((p) => (
        <li key={p.title} className="card grid gap-1 px-5 py-6 text-center">
          <span className="num font-serif text-[1.9rem] font-black leading-tight text-brand">{p.big}</span>
          <b>{p.title}</b>
          <span className="text-[.88rem] text-muted">{p.body}</span>
        </li>
      ))}
    </ul>
  );
}

export async function StoreInfo() {
  const all = await getT();
  const t = all.store;
  return (
    <>
      <SectionHead eyebrow={t.eyebrow} title={t.title} />
      <div className="grid gap-5 md:grid-cols-[1.2fr_1fr] md:items-center">
        <div className="grid aspect-[16/10] place-items-center rounded-[var(--r)] p-3 text-center text-[.85rem] text-muted"
          style={{ background: "repeating-linear-gradient(45deg,#EDE2CE 0 12px,#E8DBC4 12px 24px)" }}>
          <span><b className="block text-base text-brand">{t.mapTitle}</b>{t.mapBody}</span>
        </div>
        <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-2">
          <dt className="text-[.88rem] text-muted">{t.address}</dt><dd className="font-bold">{t.addressValue}<span className="todo">{t.pending}</span></dd>
          <dt className="text-[.88rem] text-muted">{t.shop}</dt><dd className="num font-bold">{t.shopValue}</dd>
          <dt className="text-[.88rem] text-muted">{all.common.pickup}</dt><dd className="num font-bold">{t.pickupValue}</dd>
          <dt className="text-[.88rem] text-muted">{t.contact}</dt><dd className="font-bold">{t.contactValue}</dd>
        </dl>
      </div>
    </>
  );
}

export async function SilverBand() {
  const lang = await getLang();
  const all = await getT();
  const t = all.silverBand;
  return (
    <div className="card grid gap-4 p-6 md:grid-cols-2 md:items-center md:p-8">
      <div className="grid gap-2.5">
        <span className="eyebrow">{t.eyebrow}</span>
        <h2 className="h2"><Lines text={t.title} /></h2>
        <p className="lead">{t.lead}</p>
        <div className="flex flex-wrap gap-2">
          {Object.values(all.softness).map((l) => <span key={l} className="rounded-full border-[1.5px] border-brand px-3.5 py-1 text-[.9rem] font-bold text-brand">{l}</span>)}
        </div>
        <div><Link href={localePath(lang, "/silver")} className="btn btn-ghost">{t.cta}</Link></div>
      </div>
      <div className="grid gap-1.5">
        <PhotoSlot drawing="tray" caption={t.cap} src={PHOTOS.silverTray} />
        <StagedNote />
      </div>
    </div>
  );
}

export function Faq({ items }: { items: { q: string; a: string }[] }) {
  return (
    <div className="grid gap-2.5">
      {items.map((f, i) => (
        <details key={f.q} open={i === 0} className="group card border border-line">
          <summary className="relative cursor-pointer list-none py-4 pl-[18px] pr-12 font-bold [&::-webkit-details-marker]:hidden">
            {f.q}
            <span aria-hidden="true" className="absolute right-[18px] top-1/2 -translate-y-1/2 text-[1.3rem] text-brand group-open:hidden">+</span>
            <span aria-hidden="true" className="absolute right-[18px] top-1/2 hidden -translate-y-1/2 text-[1.3rem] text-brand group-open:inline">−</span>
          </summary>
          <p className="px-[18px] pb-4 text-[.92rem] text-muted">{f.a}</p>
        </details>
      ))}
    </div>
  );
}

/** 연출 사진 안내(사진 아래) */
export async function StagedNote({ className = "" }: { className?: string }) {
  return <p className={`staged ${className}`}>{(await getT()).common.staged}</p>;
}
