"use client";
import Link from "next/link";
import { useHref, useT } from "@/components/lang";

export default function NotFound() {
  const t = useT().notFound;
  const href = useHref();
  return (
    <section className="gut sec">
      <div className="narrow grid justify-items-center gap-4 text-center">
        <span className="hand">{t.hand}</span>
        <h1 className="title text-[1.8rem]">{t.title}</h1>
        <p className="lead">{t.lead}</p>
        <Link href={href("/menu")} className="btn btn-primary">{t.cta}</Link>
      </div>
    </section>
  );
}
