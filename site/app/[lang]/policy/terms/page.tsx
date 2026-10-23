import type { Metadata } from "next";
import { Fragment } from "react";
import { alternates, getDict, hasLocale } from "@/lib/i18n";
import { getT } from "@/lib/i18n/server";

export async function generateMetadata({ params }: PageProps<"/[lang]/policy/terms">): Promise<Metadata> {
  const { lang } = await params;
  if (!hasLocale(lang)) return {};
  return { title: getDict(lang).terms.title, alternates: alternates(lang, "/policy/terms") };
}

export default async function TermsPage() {
  const t = (await getT()).terms;
  return (
    <section className="gut sec">
      <article className="narrow grid gap-4 [&_h2]:mt-4 [&_h2]:text-[1.1rem] [&_h2]:font-bold">
        <h1 className="title text-[1.8rem]">{t.title}</h1>
        <p className="todo w-fit">{t.draft}</p>
        {t.prevails && <p className="text-[.85rem] text-muted">{t.prevails}</p>}
        {t.sections.map((x) => (
          <Fragment key={x.h}>
            <h2>{x.h}</h2>
            <p>{x.p}</p>
          </Fragment>
        ))}
      </article>
    </section>
  );
}
