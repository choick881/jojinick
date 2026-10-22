// brand/ 폴더(원본)의 메뉴 데이터와 확정 로고를 site/로 복사한다.
// 메뉴·로고를 바꿀 때는 brand/를 고치고 `npm run sync:brand`를 실행한다.
import fs from "node:fs";
import path from "node:path";

const site = path.resolve(import.meta.dirname, "..");
const brand = path.resolve(site, "..", "brand");

const copies = [
  ["menu.json", "data/menu.json"],
  ["logo/logo.svg", "public/brand/logo.svg"],
  ["logo/logo-horizontal.svg", "public/brand/logo-horizontal.svg"],
  ["logo/logo-horizontal-reverse.svg", "public/brand/logo-horizontal-reverse.svg"],
  ["logo/symbol.svg", "public/brand/symbol.svg"],
  ["logo/favicon.svg", "app/icon.svg"],
  ["logo/apple-touch-icon.png", "app/apple-icon.png"],
  ["logo/og-image.png", "app/opengraph-image.png"],
];

if (!fs.existsSync(brand)) {
  console.log("brand/ 폴더가 없어 복사를 건너뜁니다 (이미 복사된 파일 사용).");
  process.exit(0);
}
for (const [from, to] of copies) {
  fs.mkdirSync(path.dirname(path.join(site, to)), { recursive: true });
  fs.copyFileSync(path.join(brand, from), path.join(site, to));
  console.log(`${from} → ${to}`);
}
