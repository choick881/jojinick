import { existsSync } from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import menu from "@/data/menu.json";
import { PHOTOS, PRODUCT_PHOTO_SLUGS, productPhoto, setContentsPhoto } from "./photos";

const inPublic = (src: string) => existsSync(path.join(__dirname, "..", "public", src));

describe("photos", () => {
  it("모든 사진 경로가 public에 실제로 있다", () => {
    const srcs = [...Object.values(PHOTOS), ...menu.products.map((p) => productPhoto(p.slug)), setContentsPhoto("dinner-set-1")];
    for (const src of srcs) expect(src && inPublic(src), src).toBe(true);
  });

  it("사진 목록의 상품은 모두 메뉴에 있다", () => {
    const slugs = new Set(menu.products.map((p) => p.slug));
    for (const s of PRODUCT_PHOTO_SLUGS) expect(slugs.has(s), s).toBe(true);
  });

  it("사진이 없는 상품은 undefined (선 그림으로 대신)", () => {
    expect(productPhoto("new-banchan")).toBeUndefined();
    expect(setContentsPhoto("banchan-3-set")).toBeUndefined();
  });
});
