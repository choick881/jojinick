import Link from "next/link";
import { localePath } from "@/lib/i18n";
import { getLang, getT } from "@/lib/i18n/server";

/** 오픈 준비 중 띠(모든 화면 맨 위). 운영 배포에서 주문을 열기 전까지만 보인다 */
export async function OpeningBanner() {
  const t = (await getT()).opening;
  return (
    <p className="bg-brand px-4 py-2 text-center text-[.88rem] font-bold text-white" role="status">
      {t.bannerBefore}<span className="text-[#FFD9A8]">{t.bannerStrong}</span>{t.bannerAfter}
    </p>
  );
}

/** 주문 화면 대신 보여 줄 안내 */
export async function OpeningNotice() {
  const lang = await getLang();
  const t = (await getT()).opening;
  return (
    <div className="card mx-auto grid max-w-md justify-items-center gap-4 p-7 text-center">
      <span className="hand text-[1.4rem]">{t.hand}</span>
      <h1 className="title text-[1.7rem]">{t.title}</h1>
      <p className="lead">{t.body}</p>
      <Link href={localePath(lang, "/menu")} className="btn btn-primary">{t.cta}</Link>
    </div>
  );
}
