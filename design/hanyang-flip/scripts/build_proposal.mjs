// 과제 제안서 HTML → A4 PDF + 쪽별 미리보기 PNG
//   node scripts/build_proposal.mjs                 → proposal.html, studio-booking.html 모두
//   node scripts/build_proposal.mjs proposal        → 하나만
// 결과: proposal/<이름>.pdf, shots/<이름>-p{n}.png
import { createRequire } from 'node:module';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || '/opt/node-tools/node_modules/playwright');
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');

const names = process.argv.slice(2).length ? process.argv.slice(2) : ['proposal', 'studio-booking'];
const browser = await chromium.launch();
try {
 for (const name of names) {
  console.log(`── ${name}`);
  const page = await browser.newPage({ viewport: { width: 900, height: 1200 }, deviceScaleFactor: 2 });
  await page.goto(pathToFileURL(resolve(ROOT, `proposal/${name}.html`)).href, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);

  // 넘침 검사: 각 쪽 내용이 297mm 안에 들어가는지
  const over = await page.evaluate(() => [...document.querySelectorAll('.page')].map((p, i) => {
    const foot = p.querySelector('.foot');
    const last = [...p.children].filter(c => c !== foot).pop();
    return { page: i + 1, gap: Math.round(foot.getBoundingClientRect().top - last.getBoundingClientRect().bottom) };
  }));
  for (const o of over) console.log(`${o.page}쪽 여백 ${o.gap}px ${o.gap < 0 ? '⚠ 넘침' : '✓'}`);

  const pages = await page.$$('.page');
  for (let i = 0; i < pages.length; i++) {
    await pages[i].screenshot({ path: resolve(ROOT, `shots/${name}-p${i + 1}.png`) });
  }
  await page.emulateMedia({ media: 'print' });
  await page.pdf({ path: resolve(ROOT, `proposal/${name}.pdf`), format: 'A4', printBackground: true, preferCSSPageSize: true });
  console.log(`✓ proposal/${name}.pdf`);
  await page.close();
 }
} finally {
  await browser.close();
}
