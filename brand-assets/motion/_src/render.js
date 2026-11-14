// Render build/*.html to 1080x1920 30fps MP4 by seeking every CSS animation frame by frame.
// Usage: node render.js [nameFilter] [--preview]   (--preview writes a few PNG stills instead)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const FPS = 30;
(async () => {
  const vids = JSON.parse(fs.readFileSync(path.join(__dirname, 'build/videos.json')));
  const filt = process.argv.find((x, i) => i > 1 && !x.startsWith('--')) || '';
  const preview = process.argv.includes('--preview');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  for (const v of vids) {
    if (filt && !v.name.includes(filt)) continue;
    await page.goto('file://' + v.html);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    const seek = (t) => page.evaluate((ms) => { for (const a of document.getAnimations()) { a.pause(); a.currentTime = ms; } }, t * 1000);
    if (preview) {
      const dir = path.join(__dirname, 'build', 'preview'); fs.mkdirSync(dir, { recursive: true });
      const times = JSON.parse(process.env.TIMES || '[1,3,5,7,9,11,13,15,17]');
      for (const t of times) { await seek(t); await page.screenshot({ path: path.join(dir, `${v.name}_${String(t).padStart(4, '0')}.png`) }); }
      continue;
    }
    const out = path.join(__dirname, '..', `tovinest-${v.name}.mp4`);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
      '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000',
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-r', String(FPS),
      '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    const n = Math.round(v.dur * FPS);
    for (let f = 0; f < n; f++) {
      await seek(f / FPS);
      const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
    console.log('wrote', out, n, 'frames');
  }
  await browser.close();
})();
