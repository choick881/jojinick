// 시안 HTML 스크린샷 + 로고 PNG(GPT 참고 이미지용) 내보내기.
//   node scripts/shoot.mjs logo/logo-board.html detail/detail-A.html ...
//   node scripts/shoot.mjs --logos          # logo/png/logo-{A..F}.png 1024px
// 결과: shots/<이름>-desktop.png, shots/<이름>-mobile.png (+ 가로 스크롤 검사 결과 출력)
import { createRequire } from 'node:module';
import { existsSync, mkdirSync, readFileSync } from 'node:fs';
import { dirname, resolve, basename } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || '/opt/node-tools/node_modules/playwright');
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);

const browser = await chromium.launch();
try {
  if (args.includes('--logos')) {
    mkdirSync(resolve(ROOT, 'logo/png'), { recursive: true });
    const page = await browser.newPage({ viewport: { width: 1024, height: 1024 } });
    for (const c of ['A', 'B', 'C', 'D', 'E', 'F']) {
      const svg = readFileSync(resolve(ROOT, `logo/logo-${c}.svg`), 'utf8');
      await page.setContent(`<html><head><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700&display=swap" rel="stylesheet">
        <style>body{margin:0;background:#fff;display:grid;place-items:center;height:100vh}svg{width:820px;height:820px}</style></head>
        <body>${svg}</body></html>`, { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);
      await page.screenshot({ path: resolve(ROOT, `logo/png/logo-${c}.png`) });
      console.log(`✓ logo/png/logo-${c}.png`);
    }
  }
  mkdirSync(resolve(ROOT, 'shots'), { recursive: true });
  for (const rel of args.filter(a => !a.startsWith('--'))) {
    const file = resolve(ROOT, rel);
    if (!existsSync(file)) { console.error(`없음: ${rel}`); continue; }
    const name = basename(rel, '.html');
    for (const [label, width] of [['desktop', 1440], ['mobile', 390]]) {
      const page = await browser.newPage({ viewport: { width, height: 900 }, deviceScaleFactor: label === 'mobile' ? 2 : 1 });
      await page.goto(pathToFileURL(file).href, { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      await page.screenshot({ path: resolve(ROOT, `shots/${name}-${label}.png`), fullPage: true });
      console.log(`${overflow > 0 ? '⚠ 가로스크롤 ' + overflow + 'px' : '✓'} shots/${name}-${label}.png`);
      await page.close();
    }
  }
} finally {
  await browser.close();
}
