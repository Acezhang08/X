// 用法: node snap.mjs outDir t1 t2 ...   抽帧检查
import { createRequire } from 'module'; import fs from 'fs';
const { chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright');
const [out, ...ts] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
pg.on('pageerror', e => console.error('[pageerror]', e.message)); pg.on('console', m => m.type() === 'error' && console.error('[console]', m.text()));
await pg.goto('http://localhost:8124/index.html'); await pg.waitForFunction('window.READY===true', null, { timeout: 60000 });
for (const t of ts) { const u = await pg.evaluate(n => { window.renderFrame(n); return window.frameData('image/png'); }, Math.round(+t * 30)); fs.writeFileSync(`${out}/t${String(t).padStart(6, '0')}.png`, Buffer.from(u.split(',')[1], 'base64')); }
await b.close();
