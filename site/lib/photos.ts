// 사진 경로 모음 (public/photos). 모두 GPT 이미지(gpt-image-2)로 만든 연출 사진이라 쓰는 곳마다 STAGED_NOTE를 함께 둔다.
// 사진이 없는 상품은 undefined를 돌려주고, PhotoSlot이 선 그림과 '사진 준비 중'을 보여 준다.

export const PHOTOS = {
  dinnerTable: "/photos/dinner-table.jpg",
  silverTray: "/photos/silver-tray.jpg",
  setContainers: "/photos/dinner-set-containers.jpg",
  pickup: "/photos/pickup-cabinet.jpg",
  shop: "/photos/shop-interior.jpg",
} as const;

/** 세트 상품은 상차림 사진을 대표 사진으로 쓴다 */
const SET_PHOTOS: Record<string, string> = {
  "dinner-set-1": PHOTOS.dinnerTable,
  "silver-dinner-set": PHOTOS.silverTray,
};

/** public/photos/products/<slug>.jpg 가 있는 상품 */
export const PRODUCT_PHOTO_SLUGS = [
  "banchan-3-set", "spinach-namul", "bean-sprout-namul", "stir-fried-anchovy", "cabbage-kimchi",
  "braised-potato", "egg-roll", "beef-jangjorim", "spicy-pork", "braised-mackerel", "japchae",
  "doenjang-jjigae", "kimchi-jjigae", "beef-radish-soup", "silver-soft-3-set",
] as const;

const SLUGS = new Set<string>(PRODUCT_PHOTO_SLUGS);

export function productPhoto(slug: string): string | undefined {
  return SET_PHOTOS[slug] ?? (SLUGS.has(slug) ? `/photos/products/${slug}.jpg` : undefined);
}

/** 세트 '오늘의 구성' 용기 사진. 사진 속 구성과 같은 세트에만 붙인다 */
export function setContentsPhoto(slug: string): string | undefined {
  return slug === "dinner-set-1" ? PHOTOS.setContainers : undefined;
}
