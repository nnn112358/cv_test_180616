const { chromium } = require('/opt/node-tools/node_modules/playwright');
const { spawn } = require('child_process');
const [,, mode, html, out] = process.argv;
(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', proxy, args: ['--ignore-certificate-errors-spki-list'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1358 }, deviceScaleFactor: 1, colorScheme: 'light', ignoreHTTPSErrors: true });
  page.on('pageerror', e => console.error('pageerror', e.message));
  await page.goto('file://' + html);
  await page.waitForFunction(() => window.__ready === true);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  console.log('fonts:', await page.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family).filter((v,i,a)=>a.indexOf(v)===i).join(', ')));
  if (mode === 'still') {
    await page.evaluate(t => window.renderAt(t), 4.5);
    await page.screenshot({ path: out });
  } else {
    const fps = 30, dur = 20;
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = 0; i < fps * dur; i++) {
      await page.evaluate(t => window.renderAt(t), i / fps);
      const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
