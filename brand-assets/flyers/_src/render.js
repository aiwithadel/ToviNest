// Render build/*.html at 2x -> ../<name>@2x.png ; email-ready JPEGs are made by post.py
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(path.join(__dirname, 'build/jobs.json')));
  const b = await chromium.launch();
  for (const j of jobs) {
    const p = await b.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: 2 });
    await p.goto('file://' + j.html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
    await p.screenshot({ path: path.join(__dirname, '..', `${j.name}@2x.png`), clip: { x: 0, y: 0, width: j.w, height: j.h } });
    await p.close();
  }
  await b.close(); console.log('rendered', jobs.length);
})();
