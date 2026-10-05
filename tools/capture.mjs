// 用法: node tools/capture.mjs <outDir> [from] [to] [step]   （to 不含）
import { createRequire } from 'module';
import fs from 'fs';
const { chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright');
const [out, from = 0, to = 540, step = 1] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--use-gl=angle'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
page.on('console', (m) => m.type() === 'error' && console.error('[page]', m.text()));
page.on('pageerror', (e) => console.error('[pageerror]', e.message));
await page.goto('http://localhost:8123/city/index.html');
await page.waitForFunction('window.READY === true', null, { timeout: 120000 });
for (let n = +from; n < +to; n += +step) {
  const t0 = Date.now();
  const url = await page.evaluate((i) => { window.renderFrame(i); return window.frameDataURL('image/png'); }, n);
  fs.writeFileSync(`${out}/f${String(n).padStart(4, '0')}.png`, Buffer.from(url.split(',')[1], 'base64'));
  console.log(n, Date.now() - t0, 'ms');
}
await browser.close();
