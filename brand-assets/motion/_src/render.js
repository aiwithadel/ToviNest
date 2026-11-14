// Render build/*.html to IG/TikTok-spec MP4s (1080x1920, SAR 1:1, H.264 yuv420p 30fps, AAC 48k stereo 192k, +faststart)
// by seeking every CSS animation frame by frame, plus a cover.jpg per video.
//   node render.js [filter]          render mp4 + cover
//   node render.js [filter] --qa     safe-zone + hold-time audit and overlay contact sheets (build/qa/)
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const FPS = 30;
const SAFE = { x0: 40, y0: 320, x1: 900, y1: 1400 };
const MIN_HOLD = 1.5;

async function seek(page, t) {
  await page.evaluate((ms) => { for (const a of document.getAnimations()) { a.pause(); a.currentTime = ms; } }, t * 1000);
}

// Every element that renders text (own text node, counter) or is marked .qa-t / .qa-m
async function snapshot(page) {
  return page.evaluate(() => {
    const els = document.querySelectorAll('.safe *');
    const out = [];
    els.forEach((el, i) => {
      if (!el.dataset.qid) el.dataset.qid = i;
      const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
      const marked = el.classList.contains('qa-t') || el.classList.contains('qa-m') || el.classList.contains('count');
      if (!own && !marked) return;
      const r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) return;
      let op = 1, p = el;
      while (p && p !== document.body) { op *= parseFloat(getComputedStyle(p).opacity); p = p.parentElement; }
      out.push({ id: el.dataset.qid, txt: (el.innerText || el.className).trim().slice(0, 40), op,
                 x0: r.left, y0: r.top, x1: r.right, y1: r.bottom, text: own || el.classList.contains('count') });
    });
    return out;
  });
}

async function qa(page, v, dir) {
  const issues = [], vis = {};
  const step = 1 / 15, n = Math.ceil(v.dur / step);
  for (let k = 0; k <= n; k++) {
    const t = Math.min(v.dur - 0.001, k * step);
    await seek(page, t);
    for (const e of await snapshot(page)) {
      if (e.op >= 0.3 && (e.x0 < SAFE.x0 - .5 || e.y0 < SAFE.y0 - .5 || e.x1 > SAFE.x1 + .5 || e.y1 > SAFE.y1 + .5))
        issues.push(`t=${t.toFixed(2)} OUT OF SAFE BOX: "${e.txt}" [${e.x0|0},${e.y0|0} - ${e.x1|0},${e.y1|0}]`);
      if (e.text) { (vis[e.id] ||= { txt: e.txt, on: [] }).on.push(e.op >= 0.5 ? t : null); }
    }
  }
  for (const [id, o] of Object.entries(vis)) {   // contiguous visible runs
    let s = null, last = null;
    const runs = [];
    o.on.forEach((t) => { if (t !== null) { if (s === null) s = t; last = t; } else if (s !== null) { runs.push([s, last]); s = null; } });
    if (s !== null) runs.push([s, last]);
    for (const [a, b] of runs) if (b - a + step < MIN_HOLD) issues.push(`HOLD ${(b - a + step).toFixed(2)}s < ${MIN_HOLD}s: "${o.txt}" at ${a.toFixed(2)}s`);
  }
  // contact sheet frames every 1 s with the safe box (red) and the IG 1080x1350 grid crop (blue)
  await page.evaluate(() => {
    const d = document.createElement('div'); d.id = 'qaov';
    d.innerHTML = '<div style="position:absolute;left:40px;top:320px;width:860px;height:1080px;outline:4px solid rgba(255,0,0,.85)"></div>' +
      '<div style="position:absolute;left:0;top:285px;width:1080px;height:1350px;outline:4px dashed rgba(0,90,255,.8)"></div>';
    d.style.cssText = 'position:absolute;inset:0;z-index:999;pointer-events:none';
    document.querySelector('.stage').appendChild(d);
  });
  fs.mkdirSync(dir, { recursive: true });
  for (let t = 0; t < v.dur; t += 1) {
    await seek(page, t + 0.5);
    await page.screenshot({ path: path.join(dir, `${v.name}_${String(t).padStart(2, '0')}.jpg`), type: 'jpeg', quality: 70 });
  }
  return issues;
}

(async () => {
  const vids = JSON.parse(fs.readFileSync(path.join(__dirname, 'build/videos.json')));
  const filt = process.argv.find((x, i) => i > 1 && !x.startsWith('--')) || '';
  const doQA = process.argv.includes('--qa');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  let total = 0;
  for (const v of vids) {
    if (filt && !v.name.includes(filt)) continue;
    await page.goto('file://' + v.html);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    if (doQA) {
      const issues = await qa(page, v, path.join(__dirname, 'build/qa', v.name));
      total += issues.length;
      console.log(`${v.name}: ${issues.length ? issues.length + ' issue(s)' : 'PASS (safe box + holds)'}`);
      issues.slice(0, 40).forEach(i => console.log('   ' + i));
      continue;
    }
    const wav = path.join(__dirname, 'build', `${v.name}.wav`);
    execFileSync('python3', [path.join(__dirname, 'music.py'), String(v.dur), wav, String(v.music)]);
    const out = path.join(__dirname, '..', `tovinest-${v.name}.mp4`);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-i', wav,
      '-map', '0:v', '-map', '1:a', '-vf', 'setsar=1', '-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
      '-r', String(FPS), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2', '-t', String(v.dur), '-movflags', '+faststart', out],
      { stdio: ['pipe', 'inherit', 'inherit'] });
    const n = Math.round(v.dur * FPS);
    for (let f = 0; f < n; f++) {
      await seek(page, f / FPS);
      const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
    await page.goto('file://' + v.cover);
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(__dirname, '..', `tovinest-${v.name}-cover.jpg`), type: 'jpeg', quality: 92 });
    console.log('wrote', out, n, 'frames + cover');
  }
  await browser.close();
  if (doQA && total) process.exitCode = 1;
})();
