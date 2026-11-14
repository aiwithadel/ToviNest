// Render build/*.html to PNG. Usage: node render.js [filter]
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const man = JSON.parse(fs.readFileSync(path.join(__dirname, 'build/manifest.json')));
  const filt = process.argv[2] || '';
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  for (const m of man) {
    if (filt && !m.out.includes(filt)) continue;
    await page.setViewportSize({ width: 1080, height: m.h });
    await page.goto('file://' + m.html);
    await page.evaluate(() => document.fonts.ready);
    const out = path.join(__dirname, '..', m.out);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    await page.screenshot({ path: out, clip: { x: 0, y: 0, width: 1080, height: m.h } });
  }
  await browser.close();
  console.log('done');
})();
