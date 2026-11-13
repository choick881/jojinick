// html/*.html → pdf/*.pdf (A4, 쪽번호 머리말/꼬리말). 사용법: node tools/pdf.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const HTML = path.join(ROOT, 'html');
const PDF = path.join(ROOT, 'pdf');

(async () => {
  fs.mkdirSync(PDF, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const f of fs.readdirSync(HTML).filter((x) => x.endsWith('.html')).sort()) {
    await page.goto('file://' + path.join(HTML, f), { waitUntil: 'load' });
    await page.emulateMedia({ media: 'print' });
    const title = await page.title();
    const out = path.join(PDF, f.replace(/\.html$/, '.pdf'));
    const tmpCover = out + '.cover.tmp';
    const tmpBody = out + '.body.tmp';
    await page.pdf({ path: tmpCover, format: 'A4', printBackground: true, preferCSSPageSize: true, pageRanges: '1' });
    await page.pdf({
      path: tmpBody,
      pageRanges: '2-',
      format: 'A4',
      printBackground: true,
      preferCSSPageSize: true,
      displayHeaderFooter: true,
      headerTemplate: `<div style="font-family:Pretendard;font-size:7.5px;color:#8a8175;width:100%;padding:0 17mm;display:flex;justify-content:space-between"><span>온벗(가칭) 시니어 비즈니스 사업추진 보고서</span><span>${title}</span></div>`,
      footerTemplate: `<div style="font-family:Pretendard;font-size:8px;color:#8a8175;width:100%;padding:0 17mm;display:flex;justify-content:space-between"><span>조피디 창업 프로젝트 · 2026.11 작성 · 대외비</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
    });
    execFileSync('pdfunite', [tmpCover, tmpBody, out]);
    fs.unlinkSync(tmpCover); fs.unlinkSync(tmpBody);
    console.log('pdf', out);
  }
  await browser.close();
})();
