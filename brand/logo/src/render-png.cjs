// 확정 SVG → PNG 내보내기 (투명 배경). 실행: node brand/logo/src/render-png.cjs
// 필요: playwright (클라우드 세션에는 설치되어 있음)
const path = require("path");
const fs = require("fs");
let pw;
try { pw = require("playwright"); } catch { pw = require("/opt/node-tools/node_modules/playwright"); }

const DIR = path.resolve(__dirname, "..");
const PNG = path.join(DIR, "png");
fs.mkdirSync(PNG, { recursive: true });

const svg = (f) => fs.readFileSync(path.join(DIR, f), "utf8");
const jobs = [
  // [원본, 저장 이름, 폭, 높이, 바탕]
  ["logo.svg", "png/logo-1024.png", 1024, 1024],
  ["logo-reverse.svg", "png/logo-reverse-1024.png", 1024, 1024],
  ["logo-mono.svg", "png/logo-mono-1024.png", 1024, 1024],
  ["logo-horizontal.svg", null, 1200, 0],
  ["logo-horizontal-reverse.svg", null, 1200, 0],
  ["logo-horizontal-mono.svg", null, 1200, 0],
  ["symbol.svg", "png/symbol-512.png", 512, 512],
  ["favicon.svg", "favicon-32.png", 32, 32],
  ["favicon.svg", "png/icon-512.png", 512, 512],
];

(async () => {
  const browser = await pw.chromium.launch({ executablePath: fs.existsSync("/opt/pw-browsers/chromium") ? "/opt/pw-browsers/chromium" : undefined });
  const page = await browser.newPage({ deviceScaleFactor: 1 });
  for (let [src, out, w, h] of jobs) {
    const s = svg(src);
    if (!h) {
      const [, vw, vh] = s.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
      h = Math.round((w * vh) / vw);
      out = `png/${src.replace(".svg", "")}-${w}.png`;
    }
    await page.setViewportSize({ width: w, height: h });
    await page.setContent(`<style>html,body{margin:0;background:transparent}svg{display:block;width:${w}px;height:${h}px}</style>${s}`);
    await page.screenshot({ path: path.join(DIR, out), omitBackground: true });
    console.log(out, `${w}x${h}`);
  }

  // 아이폰 홈 화면 아이콘: 크림 바탕 + 원형 엠블럼
  await page.setViewportSize({ width: 180, height: 180 });
  await page.setContent(`<style>html,body{margin:0;background:#FBF6EC}svg{display:block;width:164px;height:164px;margin:8px}</style>${svg("logo.svg")}`);
  await page.screenshot({ path: path.join(DIR, "apple-touch-icon.png") });
  console.log("apple-touch-icon.png 180x180");

  // 공유 이미지 (카카오톡·페이스북 링크 미리보기)
  await page.setViewportSize({ width: 1200, height: 630 });
  await page.setContent(fs.readFileSync(path.join(__dirname, "og.html"), "utf8").replace("{{LOGO}}", svg("logo.svg")), { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(DIR, "og-image.png") });
  console.log("og-image.png 1200x630");
  await browser.close();
})();
