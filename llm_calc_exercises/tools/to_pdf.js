// svg/*.svg を 1 枚ずつ PDF（SVG と同じ大きさ）に変換して pdf/ に書き出す。
// 使い方: NODE_PATH=$(npm root -g) node llm_calc_exercises/tools/to_pdf.js
// その後 pdfunite で 1 冊にまとめる（README 参照）。
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const svgDir = path.join(root, 'svg');
const pdfDir = path.join(root, 'pdf');

(async () => {
  fs.mkdirSync(pdfDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const f of fs.readdirSync(svgDir).filter((n) => n.endsWith('.svg')).sort()) {
    const svg = fs.readFileSync(path.join(svgDir, f), 'utf8');
    const w = Number(svg.match(/width="([\d.]+)"/)[1]);
    const h = Number(svg.match(/height="([\d.]+)"/)[1]);
    await page.setContent(`<style>@page{margin:0}html,body{margin:0}</style>${svg}`);
    await page.pdf({
      path: path.join(pdfDir, f.replace('.svg', '.pdf')),
      width: `${w}px`,
      height: `${Math.ceil(h) + 1}px`,
      printBackground: true,
      pageRanges: '1',
    });
    console.log('wrote', f.replace('.svg', '.pdf'));
  }
  await browser.close();
})();
