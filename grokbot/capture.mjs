// 用法: node grokbot/capture.mjs <outDir> <from> <to> [step]   （帧号，to 不含）
//       node grokbot/capture.mjs <outDir> --times 1.5,8,20   （按秒截图，用于自查）
import { createRequire } from 'module';
import fs from 'fs';
const { chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright');
const [out, a, b, c] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--use-gl=angle'] });
const page = await browser.newPage({ viewport: { width: 1000, height: 600 } });
page.on('console', (m) => m.type() === 'error' && console.error('[page]', m.text()));
page.on('pageerror', (e) => console.error('[pageerror]', e.message));
await page.goto(`http://localhost:${process.env.PORT || 8124}/grokbot/scene/index.html`);
await page.waitForFunction('window.READY === true', null, { timeout: 180000 });
const save = (name, url) => fs.writeFileSync(`${out}/${name}`, Buffer.from(url.split(',')[1], 'base64'));
if (a === '--times') {
  for (const t of b.split(',').map(Number)) {
    const url = await page.evaluate((t) => { window.renderTime(t); return window.frameDataURL('image/png'); }, t);
    save(`t${t.toFixed(2).padStart(6, '0')}.png`, url);
    console.log('t', t);
  }
} else {
  const to = Math.min(+b, await page.evaluate('window.FRAMES'));
  for (let n = +a; n < to; n += +(c || 1)) {
    const t0 = Date.now();
    const url = await page.evaluate((i) => { window.renderFrame(i); return window.frameDataURL('image/png'); }, n);
    save(`f${String(n).padStart(4, '0')}.png`, url);
    if (n % 30 === 0) console.log(n, Date.now() - t0, 'ms');
  }
}
await browser.close();
