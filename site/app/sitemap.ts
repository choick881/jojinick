import type { MetadataRoute } from "next";
import { getCatalog } from "@/lib/catalog";
import { localePath } from "@/lib/i18n";
import { absoluteUrl } from "@/lib/site";

/** 한국어·영어 주소를 모두 싣고, 서로의 언어 주소(hreflang)를 함께 알린다 */
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const pages = [
    { path: "/", priority: 1, changeFrequency: "daily" as const },
    { path: "/menu", priority: 0.9, changeFrequency: "daily" as const },
    { path: "/silver", priority: 0.8, changeFrequency: "weekly" as const },
    { path: "/about", priority: 0.6, changeFrequency: "monthly" as const },
    { path: "/policy/terms", priority: 0.2, changeFrequency: "yearly" as const },
    { path: "/policy/refund", priority: 0.2, changeFrequency: "yearly" as const },
    ...(await getCatalog()).products.map((p) => ({ path: `/menu/${p.slug}`, priority: p.featured ? 0.8 : 0.6, changeFrequency: "weekly" as const })),
  ];
  const languages = (path: string) => ({ ko: absoluteUrl(path), en: absoluteUrl(localePath("en", path)) });
  return pages.flatMap((p) =>
    (["ko", "en"] as const).map((lang) => ({
      url: absoluteUrl(localePath(lang, p.path)),
      priority: lang === "ko" ? p.priority : Math.round(p.priority * 8) / 10,
      changeFrequency: p.changeFrequency,
      alternates: { languages: languages(p.path) },
    })),
  );
}
