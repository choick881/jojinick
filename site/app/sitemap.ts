import type { MetadataRoute } from "next";
import { getProducts } from "@/lib/catalog";
import { absoluteUrl } from "@/lib/site";

export default function sitemap(): MetadataRoute.Sitemap {
  const pages = [
    { path: "/", priority: 1, changeFrequency: "daily" as const },
    { path: "/menu", priority: 0.9, changeFrequency: "daily" as const },
    { path: "/silver", priority: 0.8, changeFrequency: "weekly" as const },
    { path: "/about", priority: 0.6, changeFrequency: "monthly" as const },
    { path: "/policy/terms", priority: 0.2, changeFrequency: "yearly" as const },
    { path: "/policy/refund", priority: 0.2, changeFrequency: "yearly" as const },
  ];
  return [
    ...pages.map((p) => ({ url: absoluteUrl(p.path), priority: p.priority, changeFrequency: p.changeFrequency })),
    ...getProducts().map((p) => ({ url: absoluteUrl(`/menu/${p.slug}`), priority: p.featured ? 0.8 : 0.6, changeFrequency: "weekly" as const })),
  ];
}
