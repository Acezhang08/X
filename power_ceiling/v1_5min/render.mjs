// 用法: node render.mjs <from> <to> <out.mp4>   （to 不含）
import { createRequire } from 'module'; import { spawn } from 'child_process';
const { chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright');
const [from, to, out] = process.argv.slice(2);
const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
pg.on('pageerror', e => console.error('[pageerror]', e.message));
await pg.goto('http://localhost:8124/index.html'); await pg.waitForFunction('window.READY===true', null, { timeout: 60000 });
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', '30', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p', '-r', '30', '-an', out], { stdio: ['pipe', 'inherit', 'inherit'] });
const t0 = Date.now();
for (let n = +from; n < +to; n++) {
  const u = await pg.evaluate(i => { window.renderFrame(i); return window.frameData('image/jpeg', .97); }, n);
  if (!ff.stdin.write(Buffer.from(u.split(',')[1], 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
  if ((n - from) % 300 === 0) console.log(out, n, ((Date.now() - t0) / 1000).toFixed(0) + 's');
}
ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); console.log('done', out);
