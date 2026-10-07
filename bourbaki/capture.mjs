// node capture.mjs <outDir> <from> <to>   (frame numbers; to exclusive)
//      node capture.mjs <outDir> --times 1.5,8,20
import { createRequire } from 'module';
import fs from 'fs';
const { chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright');
const [out, a, b] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
page.on('console', (m) => m.type() === 'error' && console.error('[page]', m.text()));
page.on('pageerror', (e) => console.error('[pageerror]', e.message));
await page.goto(`http://localhost:${process.env.PORT || 8125}/bourbaki/scene/index.html`);
await page.waitForFunction('window.READY === true', null, { timeout: 120000 });
const save = (name, url) => fs.writeFileSync(`${out}/${name}`, Buffer.from(url.split(',')[1], 'base64'));
if (a === '--times') {
  for (const t of b.split(',').map(Number)) {
    const url = await page.evaluate((t) => { window.renderTime(t); return window.frameDataURL('image/png'); }, t);
    save(`t${t.toFixed(2).padStart(6, '0')}.png`, url);
  }
} else {
  const to = Math.min(+b, await page.evaluate('window.FRAMES'));
  for (let n = +a; n < to; n++) {
    const url = await page.evaluate((i) => { window.renderFrame(i); return window.frameDataURL('image/png'); }, n);
    save(`f${String(n).padStart(4, '0')}.png`, url);
    if (n % 60 === 0) console.log(n);
  }
}
await browser.close();
