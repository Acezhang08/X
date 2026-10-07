// Bourbaki: deterministic 2D canvas scene. Everything is a pure function of time t (seconds),
// driven by ../build/timings.json (sentence start/end from the TTS pass).
const W = 1920, H = 1080, FPS = 30;
const cv = document.getElementById('c'), ctx = cv.getContext('2d');

// ---------- palette ----------
const PAPER = '#ecdfc4', PAPER2 = '#f3e9d2', INK = '#21170f', INK_SOFT = '#6a5846', RUST = '#b5382a';
const OXBLOOD = '#6f2a24', OLIVE = '#66673a', OCHRE = '#b8964a', BROWN = '#5a4630';
const SCREEN = '#f7f7f4', GRID = '#e7e7e2', DOT = '#e0452c', GRAY = '#b4b4ae';

// ---------- utils ----------
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const A = (t, a, b) => clamp((t - a) / (b - a));
const lerp = (a, b, k) => a + (b - a) * k;
const eIO = (k) => k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
const eO = (k) => 1 - Math.pow(1 - k, 3);
const eI = (k) => k * k * k;
const eOB = (k) => { const n = 7.5625, d = 2.75; if (k < 1 / d) return n * k * k; if (k < 2 / d) return n * (k -= 1.5 / d) * k + .75; if (k < 2.5 / d) return n * (k -= 2.25 / d) * k + .9375; return n * (k -= 2.625 / d) * k + .984375; };
const eOBack = (k) => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(k - 1, 3) + c1 * Math.pow(k - 1, 2); };
function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const mk = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };

let T = null, Ls = [];
const S = (i) => Ls[i - 1];          // sentence i (1-based): {start,end}
const T_END = () => T.duration;

// ---------- paper texture / overlays ----------
let paperTex, grainTiles = [], sheetTex;
function makePaper(w, h, base, seed, spread) {
  const c = mk(w, h), x = c.getContext('2d'), R = rng(seed);
  x.fillStyle = base; x.fillRect(0, 0, w, h);
  const id = x.getImageData(0, 0, w, h), d = id.data;
  for (let i = 0; i < d.length; i += 4) { const n = (R() - .5) * spread; d[i] += n; d[i + 1] += n; d[i + 2] += n * .9; }
  x.putImageData(id, 0, 0);
  for (let i = 0; i < 260; i++) { // fibres
    x.strokeStyle = `rgba(110,85,50,${.03 + R() * .05})`; x.lineWidth = .6 + R();
    const px = R() * w, py = R() * h, a = R() * 6.28, l = 6 + R() * 22;
    x.beginPath(); x.moveTo(px, py); x.lineTo(px + Math.cos(a) * l, py + Math.sin(a) * l); x.stroke();
  }
  for (let i = 0; i < 14; i++) { // soft stains
    const g = x.createRadialGradient(0, 0, 0, 0, 0, 1); const px = R() * w, py = R() * h, r = 80 + R() * 220;
    x.save(); x.translate(px, py); x.scale(r, r * (.6 + R() * .6));
    g.addColorStop(0, `rgba(140,105,55,${.05 + R() * .05})`); g.addColorStop(1, 'rgba(140,105,55,0)');
    x.fillStyle = g; x.beginPath(); x.arc(0, 0, 1, 0, 6.3); x.fill(); x.restore();
  }
  return c;
}
function makeGrain(seed) {
  const c = mk(512, 512), x = c.getContext('2d'), id = x.createImageData(512, 512), R = rng(seed);
  for (let i = 0; i < id.data.length; i += 4) { const v = R() * 255; id.data[i] = id.data[i + 1] = id.data[i + 2] = v; id.data[i + 3] = 255; }
  x.putImageData(id, 0, 0); return c;
}
function vignette(a) {
  const g = ctx.createRadialGradient(W / 2, H / 2, H * .42, W / 2, H / 2, H * 1.02);
  g.addColorStop(0, 'rgba(70,45,20,0)'); g.addColorStop(1, `rgba(70,45,20,${.34 * a})`);
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
}
function grain(t, a, frozen) {
  const k = frozen ? 7 : Math.floor(t * 12) % 3, R = rng(k * 977 + 3);
  ctx.save(); ctx.globalAlpha = .07 * a; ctx.globalCompositeOperation = 'multiply';
  ctx.drawImage(grainTiles[k % 3], -Math.floor(R() * 400), -Math.floor(R() * 400), 2200, 1400);
  ctx.restore();
}

// ---------- ink strokes ----------
function jit(pts, R, amp = .8, step = 12) {
  const out = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const [x1, y1] = pts[i], [x2, y2] = pts[i + 1], d = Math.hypot(x2 - x1, y2 - y1), n = Math.max(1, Math.round(d / step));
    for (let k = 0; k < n; k++) { const u = k / n; out.push([lerp(x1, x2, u) + (R() - .5) * amp * 2, lerp(y1, y2, u) + (R() - .5) * amp * 2]); }
  }
  out.push(pts[pts.length - 1]); return out;
}
function withLen(pts) { const cum = [0]; for (let i = 1; i < pts.length; i++) cum.push(cum[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])); return { pts, cum, len: cum[cum.length - 1] }; }
function strokeP(path, p, w, color = INK, alpha = 1) {
  if (p <= 0) return; const { pts, cum, len } = path, target = len * Math.min(1, p);
  ctx.save(); ctx.strokeStyle = color; ctx.globalAlpha = alpha; ctx.lineWidth = w; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
  for (let i = 1; i < pts.length; i++) {
    if (cum[i] <= target) ctx.lineTo(pts[i][0], pts[i][1]);
    else { const u = (target - cum[i - 1]) / Math.max(1e-6, cum[i] - cum[i - 1]); ctx.lineTo(lerp(pts[i - 1][0], pts[i][0], u), lerp(pts[i - 1][1], pts[i][1], u)); break; }
  }
  ctx.stroke(); ctx.restore();
}
function bez(p0, p1, p2, p3, n = 28) { const o = []; for (let i = 0; i <= n; i++) { const u = i / n, v = 1 - u; o.push([v * v * v * p0[0] + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u * u * u * p3[0], v * v * v * p0[1] + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u * u * u * p3[1]]); } return o; }
function qbez(p0, p1, p2, n = 24) { const o = []; for (let i = 0; i <= n; i++) { const u = i / n, v = 1 - u; o.push([v * v * p0[0] + 2 * v * u * p1[0] + u * u * p2[0], v * v * p0[1] + 2 * v * u * p1[1] + u * u * p2[1]]); } return o; }

// ---------- Paris street (ink drawing) ----------
let street = null, streetFull = null;
const STREET_END = 3.6;
function buildStreet() {
  const R = rng(11), P = [];
  const add = (g, pts, w = 2.2, color = INK, alpha = .92, amp = .8) => P.push({ g, path: withLen(jit(pts, R, amp)), w, color, alpha });
  const rect = (g, x, y, w, h, lw = 2) => add(g, [[x, y], [x + w, y], [x + w, y + h], [x, y + h], [x, y]], lw);
  // ground + cobbles
  add(0, [[0, 762], [1920, 762]], 3); add(0, [[0, 772], [1920, 772]], 1.6, INK, .5);
  for (let i = 0; i < 90; i++) { const x = R() * 1920, y = 778 + R() * 14; add(0, [[x, y], [x + 8 + R() * 14, y + (R() - .5) * 3]], 1.4, INK, .35); }
  // Eiffel tower
  const cx = 960, base = 762, top = 188;
  add(1, bez([cx - 170, base], [cx - 110, base - 120], [cx - 40, base - 320], [cx - 6, top + 10]), 2.8);
  add(1, bez([cx + 170, base], [cx + 110, base - 120], [cx + 40, base - 320], [cx + 6, top + 10]), 2.8);
  add(1, bez([cx - 150, base], [cx - 96, base - 110], [cx - 34, base - 300], [cx - 2, top + 20]), 1.4, INK, .6);
  add(1, bez([cx + 150, base], [cx + 96, base - 110], [cx + 34, base - 300], [cx + 2, top + 20]), 1.4, INK, .6);
  add(1, [[cx - 6, top + 10], [cx, top - 40], [cx + 6, top + 10]], 2.2);
  const levels = [[base - 150, 130], [base - 300, 76], [base - 440, 42]];
  levels.forEach(([y, hw]) => { add(1, [[cx - hw - 12, y], [cx + hw + 12, y]], 3); add(1, [[cx - hw - 6, y - 12], [cx + hw + 6, y - 12]], 1.6); });
  add(1, [[cx - 165, base - 4], [cx - 70, base - 150], [cx + 70, base - 4], [cx + 165, base - 150]], 1.3, INK, .55); // lattice
  add(1, [[cx + 165, base - 4], [cx + 70, base - 150], [cx - 70, base - 4], [cx - 165, base - 150]], 1.3, INK, .55);
  add(1, [[cx - 90, base - 150], [cx + 60, base - 300], [cx - 56, base - 300], [cx + 90, base - 150]], 1.2, INK, .5);
  add(1, bez([cx - 130, base - 4], [cx - 60, base - 100], [cx + 60, base - 100], [cx + 130, base - 4]), 1.6, INK, .7); // arch
  // distant skyline
  for (let x = 560; x < 1360; x += 52 + R() * 36) { const h = 120 + R() * 110, w = 44 + R() * 30; if (Math.abs(x + w / 2 - 960) < 120) continue;
    add(1, [[x, base], [x, base - h], [x + w * .5, base - h - 16], [x + w, base - h], [x + w, base]], 1.5, INK, .45);
    for (let k = 0; k < 3; k++) rect(1, x + 8 + k * 14, base - h + 18 + R() * 30, 6, 10, 1); }
  // Haussmann facades
  function facade(g, x, w, floors, top) {
    const fh = (base - top - 70) / floors, y0 = top + 70;
    add(g, [[x, base], [x, y0], [x + w, y0], [x + w, base]], 2.8);
    add(g, [[x - 6, y0], [x + w + 6, y0]], 3.4);
    for (let f = 1; f < floors; f++) add(g, [[x, y0 + f * fh], [x + w, y0 + f * fh]], f === 1 ? 2.6 : 1.5, INK, f === 1 ? .9 : .6);
    const nw = Math.max(2, Math.round(w / 78));
    for (let f = 0; f < floors; f++) for (let k = 0; k < nw; k++) {
      const wx = x + (k + .5) * (w / nw) - 14, wy = y0 + f * fh + fh * .16, wh = fh * .66;
      if (f === floors - 1 && k === 1 && nw === 3) { rect(g, wx - 2, wy + 6, 32, wh + 6, 1.6); add(g, [[wx + 14, wy + 6], [wx + 14, wy + wh + 12]], 1.2); continue; }
      rect(g, wx, wy, 28, wh, 1.7); add(g, [[wx + 14, wy], [wx + 14, wy + wh]], 1.1, INK, .6); add(g, [[wx - 4, wy - 3], [wx + 32, wy - 3]], 1.8); add(g, [[wx - 3, wy + wh + 3], [wx + 31, wy + wh + 3]], 2);
    }
    [2, floors - 1].forEach((f) => { if (f >= floors) return; const y = y0 + f * fh + fh * .8; add(g, [[x + 3, y], [x + w - 3, y]], 2); const zz = []; for (let xx = x + 3; xx < x + w - 3; xx += 8) { zz.push([xx, y]); zz.push([xx + 4, y + 11]); } if (zz.length > 1) add(g, zz, 1, INK, .55); });
    // mansard + dormers + chimneys
    add(g, [[x - 8, y0], [x + 24, top + 8], [x + w - 24, top + 8], [x + w + 8, y0]], 2.8);
    for (let yy = top + 20; yy < y0; yy += 12) add(g, [[x + 6 + (yy - top) * .1, yy], [x + w - 6 - (yy - top) * .1, yy]], .9, INK, .35);
    for (let k = 0; k < nw; k++) { const dx = x + (k + .5) * (w / nw) - 14, dy = top + 22; rect(g, dx, dy, 28, 30, 1.6); add(g, [[dx - 4, dy], [dx + 14, dy - 18], [dx + 32, dy]], 1.8); }
    const cxn = [x + w * .22, x + w * .78]; cxn.forEach((c, i) => { rect(g, c, top - 26 - i * 6, 14, 34 + i * 6, 1.8); add(g, [[c - 3, top - 26 - i * 6], [c + 17, top - 26 - i * 6]], 2); });
  }
  facade(2, -6, 306, 6, 66); facade(2, 300, 266, 5, 150);
  facade(3, 1352, 276, 5, 146); facade(3, 1628, 300, 6, 70);
  // lamp
  const lx = 1496;
  add(4, [[lx - 22, base], [lx - 10, base - 40], [lx + 10, base - 40], [lx + 22, base]], 2.4); add(4, [[lx, base - 40], [lx, 380]], 3);
  add(4, bez([lx, 470], [lx + 40, 470], [lx + 60, 440], [lx + 54, 410]), 1.8); add(4, bez([lx, 470], [lx - 40, 470], [lx - 60, 440], [lx - 54, 410]), 1.8);
  [lx - 54, lx + 54, lx].forEach((x, i) => { const y = i < 2 ? 396 : 352, r = i < 2 ? 16 : 24;
    add(4, [...Array(25)].map((_, k) => [x + Math.cos(k / 24 * 6.283) * r, y + Math.sin(k / 24 * 6.283) * r * 1.05]), 2); add(4, [[x - r * .6, y + r], [x + r * .6, y + r]], 2.4); add(4, [[x - r * .5, y - r], [x, y - r - 12], [x + r * .5, y - r]], 2); });
  // cafe
  add(5, [[24, 598], [466, 598]], 2.6);
  const sc = []; for (let x = 24; x <= 466; x += 36) { sc.push([x, 598]); sc.push([x, 660]); sc.push([x + 18, 676]); sc.push([x + 36, 660]); } add(5, sc.slice(0, -3), 1.8);
  for (let x = 24; x <= 466; x += 36) add(5, [[x + 18, 598], [x + 18, 676]], 1.1, INK, .5);
  add(5, [[24, 598], [24, base]], 2.4); add(5, [[466, 598], [466, base]], 2.4);
  [[150, 744], [330, 744]].forEach(([tx, ty]) => { add(5, [...Array(25)].map((_, k) => [tx + Math.cos(k / 24 * 6.283) * 46, ty + Math.sin(k / 24 * 6.283) * 11]), 2); add(5, [[tx, ty + 11], [tx, base - 2]], 2.2); add(5, [[tx - 24, base - 1], [tx + 24, base - 1]], 2.2);
    [-84, 84].forEach((dx) => { const cx2 = tx + dx; add(5, bez([cx2 - 18, 700], [cx2 - 14, 676], [cx2 + 14, 676], [cx2 + 18, 700]), 1.8); add(5, [[cx2 - 20, 718], [cx2 + 20, 718]], 2.2); add(5, [[cx2 - 18, 718], [cx2 - 24, base - 1]], 1.8); add(5, [[cx2 + 18, 718], [cx2 + 24, base - 1]], 1.8); }); });
  // group schedule
  const G = [[.15, 1.0], [.45, 1.9], [.8, 2.5], [1.0, 2.7], [1.9, 2.8], [2.1, 3.4]];
  const byG = {}; P.forEach((p) => (byG[p.g] = byG[p.g] || []).push(p));
  Object.entries(byG).forEach(([g, list]) => { const [a, b] = G[g]; list.forEach((p, i) => { const d = clamp(p.path.len / 1100, .3, b - a); p.t0 = a + (i / list.length) * (b - a - d); p.t1 = p.t0 + d; }); });
  return P;
}
function drawStreetAt(c, t) { // t in seconds from start
  street.forEach((p) => strokeP(p.path, eIO(A(t, p.t0, p.t1)), p.w, p.color, p.alpha));
}

// ---------- silhouettes ----------
function bust(x, y, s, hat, col, alpha = 1) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.globalAlpha = alpha; ctx.fillStyle = col;
  ctx.beginPath(); ctx.moveTo(-104, 96); ctx.bezierCurveTo(-104, 40, -92, 16, -50, 4); ctx.lineTo(-22, -14); ctx.lineTo(-22, -34); ctx.lineTo(22, -34); ctx.lineTo(22, -14); ctx.lineTo(50, 4);
  ctx.bezierCurveTo(92, 16, 104, 40, 104, 96); ctx.closePath(); ctx.fill();
  ctx.beginPath(); ctx.ellipse(0, -64, 33, 40, 0, 0, 6.3); ctx.fill();
  ctx.fillStyle = PAPER2; ctx.globalAlpha = alpha * .7; ctx.beginPath(); ctx.moveTo(-18, 2); ctx.lineTo(0, 38); ctx.lineTo(18, 2); ctx.lineTo(8, -10); ctx.lineTo(-8, -10); ctx.closePath(); ctx.fill();
  ctx.fillStyle = col; ctx.globalAlpha = alpha; ctx.beginPath(); ctx.moveTo(-5, 4); ctx.lineTo(5, 4); ctx.lineTo(8, 52); ctx.lineTo(0, 62); ctx.lineTo(-8, 52); ctx.closePath(); ctx.fill();
  if (hat === 1) { ctx.beginPath(); ctx.ellipse(0, -86, 64, 11, 0, 0, 6.3); ctx.fill(); ctx.beginPath(); ctx.moveTo(-36, -88); ctx.quadraticCurveTo(-38, -134, 0, -136); ctx.quadraticCurveTo(38, -134, 36, -88); ctx.closePath(); ctx.fill(); ctx.strokeStyle = PAPER2; ctx.globalAlpha = alpha * .6; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(-35, -96); ctx.lineTo(35, -96); ctx.stroke(); }
  else if (hat === 2) { ctx.save(); ctx.rotate(-.18); ctx.beginPath(); ctx.ellipse(8, -100, 54, 17, 0, 0, 6.3); ctx.fill(); ctx.beginPath(); ctx.arc(10, -118, 5, 0, 6.3); ctx.fill(); ctx.restore(); }
  else if (hat === 3) { ctx.beginPath(); ctx.ellipse(0, -88, 52, 9, 0, 0, 6.3); ctx.fill(); ctx.beginPath(); ctx.ellipse(0, -90, 34, 36, 0, Math.PI, 0); ctx.fill(); }
  else if (hat === 4) { ctx.beginPath(); ctx.ellipse(0, -80, 35, 30, 0, Math.PI * 1.05, Math.PI * 1.95); ctx.fill(); ctx.beginPath(); ctx.arc(0, -112, 15, 0, 6.3); ctx.fill(); }
  else { ctx.beginPath(); ctx.ellipse(0, -84, 35, 24, 0, Math.PI * 1.05, Math.PI * 1.95); ctx.fill(); }
  ctx.restore();
}
function arm(sx, sy, hx, hy, p, w0, w1, col, alpha = 1, sag = .18) {
  if (p <= 0) return; const dx = hx - sx, dy = hy - sy, mx = (sx + hx) / 2 - dy * sag, my = (sy + hy) / 2 + dx * sag * .0 + Math.abs(dx) * .12;
  const N = 22, L = [], Rr = []; for (let i = 0; i <= N; i++) { const u = i / N * p, v = 1 - u, x = v * v * sx + 2 * v * u * mx + u * u * hx, y = v * v * sy + 2 * v * u * my + u * u * hy;
    const u2 = Math.min(1, u + .01), v2 = 1 - u2, x2 = v2 * v2 * sx + 2 * v2 * u2 * mx + u2 * u2 * hx, y2 = v2 * v2 * sy + 2 * v2 * u2 * my + u2 * u2 * hy;
    const a = Math.atan2(y2 - y, x2 - x) + Math.PI / 2, w = lerp(w0, w1, i / N) / 2; L.push([x + Math.cos(a) * w, y + Math.sin(a) * w]); Rr.push([x - Math.cos(a) * w, y - Math.sin(a) * w]); }
  ctx.save(); ctx.globalAlpha = alpha; ctx.fillStyle = col; ctx.beginPath(); L.forEach((q, i) => i ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1])); for (let i = N; i >= 0; i--) ctx.lineTo(Rr[i][0], Rr[i][1]); ctx.closePath(); ctx.fill();
  if (p > .96) { ctx.beginPath(); ctx.arc(hx, hy, w1 * .85, 0, 6.3); ctx.fill(); } ctx.restore();
}
function seated(x, y, s, col, a) { // faceless café patron
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.globalAlpha = a; ctx.fillStyle = col;
  ctx.beginPath(); ctx.ellipse(0, -112, 13, 16, 0, 0, 6.3); ctx.fill();
  ctx.beginPath(); ctx.moveTo(-18, -94); ctx.quadraticCurveTo(-26, -60, -20, -22); ctx.lineTo(30, -18); ctx.lineTo(30, 20); ctx.lineTo(18, 20); ctx.lineTo(16, -6); ctx.lineTo(-12, -6); ctx.lineTo(-14, 20); ctx.lineTo(-24, 20); ctx.lineTo(-24, -20); ctx.quadraticCurveTo(-20, -60, -18, -94); ctx.fill();
  ctx.beginPath(); ctx.moveTo(-14, -90); ctx.quadraticCurveTo(10, -92, 16, -76); ctx.lineTo(10, -30); ctx.lineTo(-18, -34); ctx.closePath(); ctx.fill();
  ctx.beginPath(); ctx.ellipse(0, -126, 22, 5, 0, 0, 6.3); ctx.fill(); ctx.beginPath(); ctx.ellipse(0, -132, 12, 8, 0, Math.PI, 0); ctx.fill();
  ctx.restore();
}

// ---------- signature ----------
const SIG = { x: 640, base: 640, size: 150, text: 'N. Bourbaki', w: 0, rot: -.035 };
function sigFont() { return `italic ${SIG.size}px "Liberation Serif", "FreeSerif", serif`; }
const flourish = (() => { const R = rng(5); return withLen(jit(bez([650, 676], [900, 700], [1100, 650], [1240, 668], 40), R, .5, 10)); })();
function drawSig(p, alpha, extra) { // p: 0..1 write progress; extra = dissolve amount 0..1
  if (p <= 0 || alpha <= 0) return;
  ctx.save(); ctx.translate(SIG.x, SIG.base); ctx.rotate(SIG.rot); ctx.font = sigFont(); ctx.textBaseline = 'alphabetic';
  const w = SIG.w, edge = w * Math.min(1, p) , soft = 26;
  ctx.globalAlpha = alpha;
  const g = ctx.createLinearGradient(edge - soft, 0, edge, 0); g.addColorStop(0, INK); g.addColorStop(1, 'rgba(33,23,15,0)');
  ctx.save(); ctx.beginPath(); ctx.rect(-20, -SIG.size, edge + 6, SIG.size * 1.4); ctx.clip();
  ctx.fillStyle = INK; ctx.fillText(SIG.text, 0, 0); ctx.restore();
  if (extra > 0) { // dissolve: scatter ink specks
    const R = rng(77); ctx.fillStyle = INK;
    for (let i = 0; i < 90; i++) { const px = R() * w, py = -R() * SIG.size * .8, d = extra * (20 + R() * 70); ctx.globalAlpha = alpha * (.5 + R() * .4) * (1 - extra) ; ctx.beginPath(); ctx.arc(px + (R() - .5) * 30, py - d, 1.5 + R() * 3, 0, 6.3); ctx.fill(); }
  }
  ctx.restore();
  // flourish under the name
  const fp = A(p, .8, 1); if (fp > 0) strokeP(flourishCache, fp, 3.4, INK, alpha);
}
let flourishCache;
function nibPos(p) { // pen tip while writing
  const x = SIG.x + SIG.w * clamp(p), y = SIG.base - 28 - Math.sin(p * 40) * 18 + Math.sin(p * 13) * 10;
  return [x, y];
}

// ---------- books ----------
const BOOKS = [{ c: OXBLOOD, dx: -6 }, { c: OLIVE, dx: 10 }, { c: BROWN, dx: -12 }, { c: OCHRE, dx: 4 }];
function book(cx, y, w, h, col, label) {
  ctx.save(); ctx.fillStyle = 'rgba(30,20,10,.22)'; ctx.fillRect(cx - w / 2 + 6, y + h - 4, w, 10);
  ctx.fillStyle = col; ctx.fillRect(cx - w / 2, y, w, h); ctx.strokeStyle = INK; ctx.lineWidth = 2.6; ctx.strokeRect(cx - w / 2, y, w, h);
  ctx.fillStyle = PAPER2; ctx.fillRect(cx - w / 2 + 16, y + 11, w - 32, h - 22); ctx.strokeStyle = INK; ctx.lineWidth = 1.2; ctx.strokeRect(cx - w / 2 + 16, y + 11, w - 32, h - 22);
  ctx.fillStyle = INK; ctx.font = '600 15px "Liberation Serif", serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(label, cx, y + h / 2 + 1);
  ctx.strokeStyle = 'rgba(0,0,0,.35)'; ctx.lineWidth = 1.5; [w / 2 - 6, -w / 2 + 6].forEach((dx) => { ctx.beginPath(); ctx.moveTo(cx + dx, y + 3); ctx.lineTo(cx + dx, y + h - 3); ctx.stroke(); });
  ctx.restore();
}
function openBook(cx, cy, w, h, flip, alpha) { // pages flipping; flip in 0..1 (several pages)
  ctx.save(); ctx.globalAlpha = alpha; ctx.translate(cx, cy);
  ctx.fillStyle = 'rgba(30,20,10,.18)'; ctx.beginPath(); ctx.ellipse(0, h / 2 + 8, w * .55, 12, 0, 0, 6.3); ctx.fill();
  const page = (side) => { ctx.fillStyle = PAPER2; ctx.strokeStyle = INK; ctx.lineWidth = 2.2; ctx.beginPath(); ctx.moveTo(0, -h / 2); ctx.lineTo(side * w / 2, -h / 2 + 8); ctx.lineTo(side * w / 2, h / 2 + 4); ctx.lineTo(0, h / 2); ctx.closePath(); ctx.fill(); ctx.stroke();
    ctx.strokeStyle = 'rgba(33,23,15,.45)'; ctx.lineWidth = 1.4; for (let i = 0; i < 8; i++) { const y = -h / 2 + 26 + i * (h - 54) / 8; ctx.beginPath(); ctx.moveTo(side * 14, y); ctx.lineTo(side * (w / 2 - 14 - (i % 3) * 14), y + 3); ctx.stroke(); } };
  page(-1); page(1);
  const n = 6; for (let i = 0; i < n; i++) { const k = clamp(flip * (n + 1) - i, 0, 1); if (k <= 0 || k >= 1) continue; const ang = k * Math.PI, sx = Math.cos(ang);
    ctx.save(); ctx.scale(sx, 1); ctx.fillStyle = PAPER2; ctx.strokeStyle = INK; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(0, -h / 2); ctx.lineTo(w / 2, -h / 2 + 8 - Math.sin(ang) * 22); ctx.lineTo(w / 2, h / 2 + 4); ctx.lineTo(0, h / 2); ctx.closePath(); ctx.fill(); ctx.stroke();
    ctx.strokeStyle = 'rgba(33,23,15,.4)'; ctx.lineWidth = 1.4; for (let j = 0; j < 6; j++) { const y = -h / 2 + 30 + j * (h - 60) / 6; ctx.beginPath(); ctx.moveTo(14, y); ctx.lineTo(w / 2 - 20 - (j % 3) * 14, y + 3); ctx.stroke(); } ctx.restore(); }
  ctx.strokeStyle = INK; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0, -h / 2); ctx.lineTo(0, h / 2); ctx.stroke(); ctx.restore();
}

// ---------- sheet (desk paper) ----------
function sheet(a, dy) {
  ctx.save(); ctx.translate(960, 460 + dy); ctx.rotate(-.012); ctx.globalAlpha = a;
  ctx.shadowColor = 'rgba(40,25,10,.38)'; ctx.shadowBlur = 36; ctx.shadowOffsetY = 14; ctx.fillStyle = PAPER2; ctx.fillRect(-520, -310, 1040, 620); ctx.shadowColor = 'transparent';
  ctx.drawImage(sheetTex, -520, -310); ctx.strokeStyle = 'rgba(33,23,15,.2)'; ctx.lineWidth = 1.5; ctx.strokeRect(-520, -310, 1040, 620);
  ctx.strokeStyle = 'rgba(100,80,50,.16)'; ctx.lineWidth = 1.4; for (let y = -250; y < 300; y += 44) { ctx.beginPath(); ctx.moveTo(-480, y); ctx.lineTo(480, y); ctx.stroke(); }
  ctx.strokeStyle = 'rgba(160,60,40,.22)'; ctx.beginPath(); ctx.moveTo(-440, -310); ctx.lineTo(-440, 310); ctx.stroke();
  ctx.restore();
}

// ---------- "newspaper-like" abstract paper ----------
function paperSheet(cx, cy, rot, sc, alpha, head, flip, redCount, t) {
  ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(sc, sc); ctx.globalAlpha = alpha;
  const w = 760, h = 560; ctx.shadowColor = 'rgba(40,25,10,.4)'; ctx.shadowBlur = 40; ctx.shadowOffsetY = 18; ctx.fillStyle = '#f1ece0'; ctx.fillRect(-w / 2, -h / 2, w, h); ctx.shadowColor = 'transparent';
  ctx.strokeStyle = 'rgba(33,23,15,.35)'; ctx.lineWidth = 2; ctx.strokeRect(-w / 2, -h / 2, w, h);
  const R = rng(31); ctx.fillStyle = 'rgba(33,23,15,.22)';
  for (let col = 0; col < 3; col++) for (let r = 0; r < 9; r++) { const x = -w / 2 + 36 + col * 238, y = -h / 2 + 190 + r * 30, ww = 150 + R() * 52; ctx.fillRect(x, y, ww, 9); }
  ctx.strokeStyle = 'rgba(33,23,15,.4)'; ctx.lineWidth = 2; ctx.strokeRect(-w / 2 + 36, -h / 2 + 118, 210, 56); ctx.beginPath(); ctx.moveTo(-w / 2 + 36, -h / 2 + 118); ctx.lineTo(-w / 2 + 246, -h / 2 + 174); ctx.moveTo(-w / 2 + 246, -h / 2 + 118); ctx.lineTo(-w / 2 + 36, -h / 2 + 174); ctx.stroke();
  // headline band with card flip
  const fy = head.fy; ctx.save(); ctx.translate(0, -h / 2 + 62); ctx.scale(1, Math.max(.001, Math.abs(Math.cos(fy * Math.PI))));
  const second = fy > .5; ctx.fillStyle = second ? RUST : INK; ctx.fillRect(-w / 2 + 28, -40, w - 56, 80);
  ctx.fillStyle = PAPER2; ctx.font = '700 46px "Liberation Mono", "DejaVu Sans Mono", monospace'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  const txt = second ? head.b : head.a; ctx.fillText(txt.slice(0, Math.max(0, Math.floor(second ? txt.length : head.typed))), 0, 3); ctx.restore();
  ctx.restore();
}

// ---------- ink blot + empty set ----------
function blotPath(cx, cy, r, seed, lobes = 9, amp = .22) { const R = rng(seed), ph = [], am = []; for (let i = 0; i < lobes; i++) { ph.push(R() * 6.28); am.push(.4 + R() * .6); }
  const pts = []; for (let k = 0; k <= 72; k++) { const a = k / 72 * 6.2832; let rr = 1; for (let i = 0; i < lobes; i++) rr += Math.sin(a * (i + 2) + ph[i]) * amp * am[i] / (1 + i * .55); pts.push([cx + Math.cos(a) * r * rr, cy + Math.sin(a) * r * rr]); } return pts; }
function emptySet(t0, t, cx, cy, scale) {
  const R = 170, k1 = A(t, t0, t0 + .55), k2 = A(t, t0 + .45, t0 + 1.35), k3 = A(t, t0 + 1.2, t0 + 2.0);
  ctx.save(); ctx.translate(cx, cy); ctx.scale(scale, scale); ctx.fillStyle = INK; ctx.strokeStyle = INK; ctx.lineCap = 'round';
  const ro = lerp(0, 46, eO(k1)) + (R - 46) * eIO(k2), wall = lerp(ro, 24, eIO(k2));
  // droplets
  const Rd = rng(9); for (let i = 0; i < 16; i++) { const a = Rd() * 6.28, d = 60 + Rd() * 190, rr = 3 + Rd() * 9, kk = A(t, t0 + .1 + Rd() * .3, t0 + .6 + Rd() * .3); if (kk <= 0) continue; ctx.globalAlpha = .8 * (1 - A(t, t0 + 1.6, t0 + 2.2)); ctx.beginPath(); ctx.arc(Math.cos(a) * d * eO(kk), Math.sin(a) * d * eO(kk), rr * kk, 0, 6.3); ctx.fill(); }
  ctx.globalAlpha = 1;
  const outer = blotPath(0, 0, Math.max(1, ro), 4, 9, .12 * (1 - k2 * .85)), inner = blotPath(0, 0, Math.max(0, ro - wall), 8, 7, .08 * (1 - k2 * .8));
  ctx.beginPath(); outer.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])); ctx.closePath();
  if (ro - wall > 1) { inner.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])); ctx.closePath(); }
  ctx.fill('evenodd');
  if (k3 > 0) { const a = [-R * 1.18, R * 1.18], b = [R * 1.18, -R * 1.18], p = eIO(k3); const sl = withLen(jit([[a[0], a[1]], [b[0], b[1]]], rng(21), 1.6, 10)); strokeP(sl, p, 26, INK, 1);
    // tendrils creeping out of the blot toward the slash
    ctx.globalAlpha = 1 - p; ctx.beginPath(); ctx.arc(0, 0, 36 * (1 - p), 0, 6.3); ctx.fill(); }
  ctx.restore();
}

// ---------- modern world ----------
let tileSlots = [], flightFrom = [520, 340];
const N_PAGES = 722, COLS = 12, TW = 30, TH = 10, PX = 33, PY = 11.9, TOWER_X = 1250, TOWER_BASE = 806;
function slot(i) { const c = i % COLS, r = Math.floor(i / COLS); return [TOWER_X + c * PX, TOWER_BASE - (r + 1) * PY]; }
function emitTime(i, t0, dur) { return t0 + dur * Math.sqrt(i / N_PAGES); }
function pageRect(x, y, a = 1, i = 0) { // a page seen edge-on in the tower
  ctx.globalAlpha = a; ctx.fillStyle = (i % 2) ? '#ffffff' : '#f1f1ec'; ctx.fillRect(x, y, TW, TH); ctx.strokeStyle = '#6f6f69'; ctx.lineWidth = 1.4; ctx.strokeRect(x + .7, y + .7, TW - 1.4, TH - 1.4);
  ctx.fillStyle = '#a4a49e'; ctx.fillRect(x + 4, y + 3.4, TW - 12 - (i % 5) * 2, 1.6); ctx.fillRect(x + 4, y + 6, TW - 16 - (i % 3) * 3, 1.6); ctx.globalAlpha = 1;
}
function pageSprite() { ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, 26, 34); ctx.strokeStyle = '#6f6f69'; ctx.lineWidth = 2; ctx.strokeRect(1, 1, 24, 32); ctx.fillStyle = '#a4a49e'; for (let k = 0; k < 4; k++) ctx.fillRect(5, 6 + k * 6, 16 - (k % 2) * 4, 2); }
function screenBg() {
  ctx.fillStyle = SCREEN; ctx.fillRect(0, 0, W, H); ctx.strokeStyle = GRID; ctx.lineWidth = 1; ctx.beginPath();
  for (let x = 0; x <= W; x += 60) { ctx.moveTo(x + .5, 0); ctx.lineTo(x + .5, H); } for (let y = 0; y <= H; y += 60) { ctx.moveTo(0, y + .5); ctx.lineTo(W, y + .5); } ctx.stroke();
  ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, 64); ctx.fillStyle = '#e4e4de'; ctx.fillRect(0, 64, W, 2);
  ['#d7d7d1', '#d7d7d1', '#d7d7d1'].forEach((c, i) => { ctx.fillStyle = c; ctx.beginPath(); ctx.arc(40 + i * 28, 32, 8, 0, 6.3); ctx.fill(); });
  ctx.fillStyle = '#8a8a84'; ctx.font = '500 24px "DejaVu Sans Mono", monospace'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('openai / math', W / 2, 33);
}
function dotGlow(x, y, t, r = 34, a = 1) {
  ctx.save(); ctx.globalAlpha = a;
  for (let i = 0; i < 3; i++) { const k = ((t * .9 + i / 3) % 1); ctx.strokeStyle = DOT; ctx.globalAlpha = a * (1 - k) * .45; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(x, y, r + k * 90, 0, 6.3); ctx.stroke(); }
  const g = ctx.createRadialGradient(x, y, 0, x, y, r * 2.6); g.addColorStop(0, 'rgba(224,69,44,.35)'); g.addColorStop(1, 'rgba(224,69,44,0)'); ctx.globalAlpha = a; ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r * 2.6, 0, 6.3); ctx.fill();
  ctx.fillStyle = DOT; ctx.beginPath(); ctx.arc(x, y, r, 0, 6.3); ctx.fill(); ctx.restore();
}
function uiChip(x, y, label, value, k) {
  if (k <= 0) return; const w = 700, h = 104; ctx.save(); ctx.globalAlpha = eO(k); ctx.translate(x, y + (1 - eO(k)) * 14);
  ctx.shadowColor = 'rgba(0,0,0,.14)'; ctx.shadowBlur = 20; ctx.shadowOffsetY = 6; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.roundRect(-w / 2, -h / 2, w, h, 16); ctx.fill(); ctx.shadowColor = 'transparent';
  ctx.strokeStyle = '#dcdcd6'; ctx.lineWidth = 2; ctx.stroke(); ctx.textBaseline = 'middle'; ctx.textAlign = 'left'; ctx.fillStyle = '#9a9a94'; ctx.font = '600 34px "Inter", sans-serif'; ctx.fillText(label, -w / 2 + 30, 0);
  ctx.fillStyle = '#1b1b19'; ctx.font = '700 42px "Inter", sans-serif'; const vis = value.slice(0, Math.floor(value.length * clamp(k * 1.4))); ctx.fillText(vis, -w / 2 + 170, 0); ctx.restore();
}
function modern(t, tw, bg = true) {
  const e0 = S(13).start + .12, dur = 3.0, flight = .5;
  if (bg) screenBg();
  const landed = Math.floor(N_PAGES * Math.pow(clamp((tw - flight - e0) / dur), 2));
  // landed tiles
  for (let i = 0; i < Math.min(N_PAGES, landed); i++) { const [x, y] = slot(i); pageRect(x, y, 1, i); }
  // in flight
  for (let i = Math.max(0, landed); i < N_PAGES; i++) { const te = emitTime(i, e0, dur); if (te > tw) break; const k = clamp((tw - te) / flight); if (k >= 1) { const [x, y] = slot(i); pageRect(x, y, 1, i); continue; }
    const [sx, sy] = flightFrom, [ex, ey] = slot(i), u = eIO(k), cxp = (sx + ex) / 2, cyp = Math.min(sy, ey) - 140; const x = (1 - u) * (1 - u) * sx + 2 * (1 - u) * u * cxp + u * u * ex, y = (1 - u) * (1 - u) * sy + 2 * (1 - u) * u * cyp + u * u * ey;
    ctx.save(); ctx.translate(x + TW / 2, y + TH / 2); ctx.rotate((1 - u) * 1.1); ctx.scale(lerp(1, TW / 26, u), lerp(1, TH / 34, u)); ctx.translate(-13, -17); pageSprite(); ctx.restore(); }
  // dot
  const appear = eOBack(A(tw, S(13).start - .35, S(13).start + .2));
  dotGlow(flightFrom[0], flightFrom[1], tw, 34 * appear, clamp(appear));
  // counter
  const shown = Math.min(N_PAGES, landed), big = shown >= N_PAGES;
  const pulse = big ? 1 + .06 * Math.max(0, 1 - (tw - (e0 + dur + flight)) * 3) : 1;
  ctx.save(); ctx.translate(flightFrom[0], 600); ctx.scale(pulse, pulse); ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic'; ctx.fillStyle = '#1b1b19'; ctx.font = '800 232px "Inter", sans-serif'; ctx.globalAlpha = clamp(A(tw, S(13).start + .1, S(13).start + .6));
  ctx.fillText(String(shown), 0, 0); ctx.font = '600 46px "Inter", sans-serif'; ctx.fillStyle = '#80807a'; ctx.fillText('math papers', 0, 66); ctx.restore();
  uiChip(flightFrom[0], 176, 'author', 'unnamed model', A(tw, S(14).start - .1, S(14).start + 1.6));
}

// ---------- scene H: old signature | modern dot ----------
function finale(t) {
  const k = eIO(A(t, S(17).start - .55, S(17).start + .05)), tn = t - S(17).start;
  // left cream panel with signature, right white panel with dot
  ctx.save(); ctx.fillStyle = SCREEN; ctx.fillRect(0, 0, W, H); ctx.strokeStyle = GRID; ctx.lineWidth = 1; ctx.beginPath(); for (let x = 960; x <= W; x += 60) { ctx.moveTo(x + .5, 0); ctx.lineTo(x + .5, H); } for (let y = 0; y <= H; y += 60) { ctx.moveTo(960, y + .5); ctx.lineTo(W, y + .5); } ctx.stroke(); ctx.restore();
  ctx.save(); ctx.beginPath(); ctx.rect(0, 0, 960, H); ctx.clip(); ctx.translate(-(1 - k) * 960, 0); ctx.drawImage(paperTex, 0, 0, W, H); vignette(.8);
  ctx.save(); ctx.translate(480, 500); ctx.rotate(-.05); ctx.font = `italic 120px "Liberation Serif", "FreeSerif", serif`; ctx.textAlign = 'center'; ctx.fillStyle = INK; ctx.globalAlpha = .96; ctx.fillText('N. Bourbaki', 0, 0); ctx.restore(); strokeP(withLen(jit(bez([230, 540], [400, 570], [560, 520], [700, 536], 30), rng(3), .5, 10)), 1, 3, INK, .9); ctx.restore();
  ctx.save(); ctx.fillStyle = 'rgba(33,23,15,.25)'; ctx.fillRect(959, 0, 2, H); ctx.restore();
  // dot on the right
  const da = clamp(k * 1.5); dotGlow(1440, 500, t, 46, da);
  // question mark in the middle
  const qk = eOBack(A(t, S(17).start - .1, S(17).start + .55)); if (qk > 0) { ctx.save(); ctx.translate(960, 500); const s = .6 + .4 * qk; ctx.scale(s, s); ctx.globalAlpha = clamp(qk); ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = '700 420px "Liberation Serif", serif'; ctx.lineJoin = 'round';
    ctx.strokeStyle = SCREEN; ctx.lineWidth = 34; ctx.strokeText('?', 0, 18); ctx.fillStyle = RUST; ctx.fillText('?', 0, 18); ctx.restore(); }
}

// ---------- old world ----------
const SLOTS = [[960, 215, 1.0], [760, 232, .95], [1160, 232, .95], [560, 272, .9], [1360, 272, .9], [380, 350, .85], [1540, 350, .85], [230, 432, .8], [1690, 432, .8]];
const HATS_A = [1, 0, 2, 3, 4, 1, 2, 0, 3], HATS_B = [3, 4, 1, 0, 2, 4, 0, 1, 2];
function persons(t) {
  const sigP = A(t, S(6).start, S(6).end - .1), nib = (t < S(6).start) ? [660, 612] : nibPos(sigP), nibRest = nibPos(1);
  const popT = (k) => S(5).start - .1 + k * .17, leaveT = (k) => S(7).start + .1 + k * .38;
  const fadeAll = 1 - A(t, S(9).start - .1, S(9).start + .5);
  if (fadeAll <= 0) return;
  const order = [0, 1, 2, 3, 4, 5, 6, 7, 8], sel = [8, 7, 6, 5, 4, 3, 2, 1, 0];
  const nibNow = (t > S(6).end - .1) ? nibRest : nib;
  // back to front: draw busts first then arms
  const state = SLOTS.map((s, k) => { const idx = sel[k]; // leave outer ones first, centre last
    const tl = leaveT(k); const [x, y, sc] = SLOTS[idx];
    const popK = eOBack(A(t, popT(idx), popT(idx) + .45)), leaveK = A(t, tl, tl + .55), enterK = A(t, tl + .3, tl + .85);
    return { idx, x, y, sc, popK, leaveK, enterK, tl }; });
  // we want people at slot idx to leave at order k: map by idx
  state.sort((a, b) => a.y - b.y);
  state.forEach((st) => {
    const { idx, x, y, sc, popK, leaveK, enterK } = st; const dir = Math.sign(960 - x) || 1;
    const out = eI(leaveK) * 460 * (-dir);          // walk away from the centre
    const alphaA = clamp(popK) * (1 - A(leaveK, .4, 1)) * fadeAll;
    const alphaB = eO(enterK) * fadeAll;
    if (alphaA > 0.01 && t < S(9).start + .6) {
      const yy = y - (1 - clamp(popK)) * 40; bust(x + out, yy, sc * (.7 + .3 * clamp(popK)), HATS_A[idx], INK, alphaA);
      if (leaveK > 0 && leaveK < 1) badge(x + out, yy - 170 * sc, 1 - Math.abs(leaveK - .3) * 1.2);
    }
    if (enterK > 0) { bust(x, y - (1 - eO(enterK)) * 70, sc, HATS_B[idx], '#5d4a3a', alphaB); }
  });
  // arms (only to the pen): each current occupant reaches
  state.forEach((st) => {
    const { idx, x, y, sc, popK, leaveK, enterK } = st; const dir = Math.sign(960 - x) || 1;
    const reach = eIO(A(t, S(5).end - .95, S(6).start + .1)), retract = 1 - A(leaveK, 0, .4);
    const sx = x + dir * 62 * sc, sy = y + 22 * sc;
    const aA = reach * retract * (1 - A(leaveK, .4, 1)) * fadeAll * clamp(popK);
    if (aA > 0 && leaveK < .6) arm(sx + eI(leaveK) * 460 * (-dir), sy, nibNow[0] + (idx - 4) * 1.5, nibNow[1] - 6 + (idx % 3) * 3, aA, 20 * sc, 9, INK, 1, .16);
    const aB = reach * eO(A(enterK, .3, 1)) * fadeAll; if (aB > 0 && enterK > 0) arm(sx, sy, nibNow[0] + (idx - 4) * 1.5, nibNow[1] - 6 + (idx % 3) * 3, aB, 20 * sc, 9, '#5d4a3a', 1, .16);
  });
  // the one pen
  const penA = clamp(A(t, S(5).end - .6, S(5).end) ) * fadeAll; if (penA > 0) { ctx.save(); ctx.globalAlpha = penA; ctx.strokeStyle = INK; ctx.lineWidth = 8; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(nibNow[0], nibNow[1]); ctx.lineTo(nibNow[0] + 54, nibNow[1] - 190); ctx.stroke(); ctx.fillStyle = INK; ctx.beginPath(); ctx.moveTo(nibNow[0] - 4, nibNow[1] + 2); ctx.lineTo(nibNow[0] + 2, nibNow[1] - 22); ctx.lineTo(nibNow[0] + 10, nibNow[1] - 18); ctx.closePath(); ctx.fill(); ctx.restore(); }
}
function badge(x, y, a) { if (a <= 0) return; ctx.save(); ctx.globalAlpha = clamp(a); ctx.strokeStyle = RUST; ctx.lineWidth = 4; ctx.beginPath(); ctx.arc(x, y, 30, 0, 6.3); ctx.stroke(); ctx.fillStyle = RUST; ctx.font = '700 32px "Liberation Mono", monospace'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('50', x, y + 2); ctx.restore(); }

function oldWorld(t) {
  const frozen = t >= S(2).end && t < S(3).start;
  ctx.drawImage(paperTex, 0, 0, W, H);
  // street
  const dimK = 1 - .62 * A(t, 3.1, 4.0) - .26 * A(t, S(11).start - .4, S(11).start + .2);
  if (t < STREET_END) drawStreetAt(ctx, t); else ctx.drawImage(streetFull, 0, 0);
  // seated patrons fade in
  const pa = A(t, 2.8, 3.5); if (pa > 0) { seated(238, 768, 1.0, INK, pa * .9); seated(280, 768, .96, '#4a3a2c', pa * .9); seated(398, 768, 1.0, INK, pa * .9); }
  if (dimK < 1) { ctx.fillStyle = PAPER; ctx.globalAlpha = 1 - dimK; ctx.fillRect(0, 0, W, H); ctx.globalAlpha = 1; }
  // desk sheet group
  const outK = eI(A(t, S(11).start - .45, S(11).start + .1)), grpA = (1 - outK), grpDy = outK * 160;
  const inK = eO(A(t, 3.05, 3.9));
  if (grpA > 0 && inK > 0) {
    sheet(clamp(inK) * grpA, (1 - inK) * 260 + grpDy);
    ctx.save(); ctx.translate(0, grpDy); ctx.globalAlpha = grpA;
    // signature
    const w1 = A(t, S(1).end - 1.75, S(1).end + .1);
    if (t < S(3).start) drawSig(w1, 1, 0);
    else if (t < S(6).start) { const f = A(t, S(4).start - .05, S(4).end); drawSig(1, 1 - .93 * eIO(f), f < 1 ? f : 0); }
    else if (t < S(6).end - .1) { drawSig(1, .07, 0); drawSig(A(t, S(6).start, S(6).end - .1), 1, 0); }
    else drawSig(1, 1, 0);
    ctx.restore();
    // books + open book
    ctx.save(); ctx.translate(0, grpDy); ctx.globalAlpha = grpA;
    BOOKS.forEach((b, i) => { const t0 = S(2).start + .1 + i * .55, k = A(t, t0, t0 + .5); if (k <= 0) return; const yFinal = 762 - 66 * (i + 1) - 2; const y = lerp(yFinal - 520, yFinal, eOB(k)); book(1650 + b.dx, y, 300 - i * 8, 64, b.c, i === 3 ? 'ÉLÉMENTS DE MATHÉMATIQUE' : 'N. BOURBAKI'); });
    const ob = A(t, S(2).start + 2.35, S(2).start + 2.95); if (ob > 0) openBook(1650, 400 - (1 - eO(ob)) * 0, 340, 150, A(t, S(2).start + 2.5, S(2).end - .12), clamp(ob * 2));
    ctx.restore();
  }
  persons(t);
  // newspaper-like paper
  const flyIn = eO(A(t, S(9).start - .05, S(9).start + .8)), flyOut = eI(A(t, S(11).start - .5, S(11).start + .1));
  if (flyIn > 0 && flyOut < 1) {
    const x = lerp(2300, 960, flyIn) - flyOut * 1500, y = lerp(-120, 470, flyIn) - flyOut * 500, rot = lerp(.55, -.035, flyIn) - flyOut * .5, sc = lerp(.35, 1, flyIn);
    const head = { a: 'BOURBAKI = PSEUDONYM', b: 'B.O.A.S. = ACRONYM?', typed: (A(t, S(9).start + .85, S(9).end - .15)) * 20, fy: A(t, S(10).start - .05, S(10).start + .5) };
    paperSheet(x, y, rot, sc, 1, head, head.fy, 0, t);
    // question marks popping
    const Q = [[-250, -60, 130, .4], [260, 10, 160, .75], [-120, 150, 110, 1.2], [90, -10, 190, 1.7]];
    Q.forEach(([qx, qy, qs, d], i) => { const k = eOBack(A(t, S(10).start + .35 + d * .6, S(10).start + .8 + d * .6)); if (k <= 0) return; ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc); ctx.translate(qx, qy + 40); ctx.rotate((i - 1.5) * .15); ctx.scale(k, k); ctx.font = `700 ${qs}px "Liberation Serif", serif`; ctx.fillStyle = RUST; ctx.globalAlpha = .9; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('?', 0, 0); ctx.restore(); });
  }
  // empty set
  const e0 = S(11).start + .1; if (t > e0 - .05 && t < S(13).start) { const sc = lerp(1, 1.5, eIO(A(t, e0 + 1.4, S(12).end))); emptySet(e0, t, 960, 430, sc); }
  vignette(1); grain(t, 1, frozen);
}

// ---------- compose ----------
function frame(t) {
  ctx.clearRect(0, 0, W, H);
  const wipeA = S(12).end + .02, wipeB = S(13).start - .02;
  if (t < wipeB) {
    oldWorld(t);
    if (t > wipeA) { // clean screen sweeps in from the left
      const k = eIO(A(t, wipeA, wipeB)), x = lerp(-60, W + 120, k);
      ctx.save(); ctx.beginPath(); ctx.rect(0, 0, x, H); ctx.clip(); modern(t, S(13).start - .3); ctx.restore();
      ctx.fillStyle = DOT; ctx.fillRect(x - 3, 0, 6, H);
    }
  } else if (t < S(17).start - .6) {
    // modern, then shrink to the right while "many people -> one name" appears on the left
    const k = eIO(A(t, S(15).start - .25, S(15).start + .5));
    screenBg();
    ctx.save(); const sc = lerp(1, .6, k); ctx.translate(lerp(0, 880, k), lerp(0, 110, k)); ctx.scale(sc, sc); modern(t, t, false); ctx.restore();
    peoplePanel(t, k);
  } else finale(t);
  if (t >= S(17).start - .6 && t < S(17).start + .1) { /* crossfade handled in finale via panel slide */ }
}
function peoplePanel(t, k) {
  const a = clamp(k) * (1 - .55 * A(t, S(16).start, S(16).start + .6)); if (a <= 0) return;
  const cx = 500, cy = 500; const kk = A(t, S(15).start + .1, S(15).end - .1);
  ctx.save(); ctx.globalAlpha = a;
  const R = 260; for (let i = 0; i < 9; i++) { const ang = i / 9 * 6.283 - 1.5, ix = cx + Math.cos(ang) * R * 1.12, iy = cy + Math.sin(ang) * R * .9, k2 = eOBack(A(kk, i * .06, i * .06 + .3));
    const ln = A(kk, .45 + i * .03, .85 + i * .03); ctx.strokeStyle = '#c9c9c3'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(ix, iy); ctx.lineTo(lerp(ix, cx, ln * .72), lerp(iy, cy, ln * .72)); ctx.stroke();
    ctx.save(); ctx.translate(ix, iy); ctx.scale(k2, k2); ctx.fillStyle = '#9a9a94'; ctx.beginPath(); ctx.arc(0, -16, 17, 0, 6.3); ctx.fill(); ctx.beginPath(); ctx.moveTo(-30, 30); ctx.quadraticCurveTo(-30, 0, 0, 0); ctx.quadraticCurveTo(30, 0, 30, 30); ctx.closePath(); ctx.fill(); ctx.restore(); }
  const ck = eOBack(A(kk, .55, 1)); ctx.translate(cx, cy); ctx.scale(ck, ck); ctx.fillStyle = '#fff'; ctx.shadowColor = 'rgba(0,0,0,.15)'; ctx.shadowBlur = 24; ctx.shadowOffsetY = 8; ctx.beginPath(); ctx.roundRect(-190, -52, 380, 104, 18); ctx.fill(); ctx.shadowColor = 'transparent'; ctx.strokeStyle = '#d6d6d0'; ctx.lineWidth = 2; ctx.stroke();
  ctx.fillStyle = INK; ctx.font = 'italic 58px "Liberation Serif", serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('N. Bourbaki', 0, 4); ctx.restore();
}

// ---------- boot ----------
window.READY = false;
window.renderFrame = (i) => frame(i / FPS);
window.renderTime = (t) => frame(t);
window.frameDataURL = (type = 'image/png') => cv.toDataURL(type);
(async () => {
  T = await (await fetch('../build/timings.json')).json(); Ls = T.lines; window.FRAMES = Math.round(T.duration * FPS);
  paperTex = makePaper(W, H, PAPER, 1, 14); sheetTex = makePaper(1040, 620, PAPER2, 2, 8); grainTiles = [makeGrain(1), makeGrain(2), makeGrain(3)];
  ctx.font = sigFont(); SIG.size = 150; ctx.save(); ctx.font = sigFont(); SIG.w = ctx.measureText(SIG.text).width; ctx.restore();
  SIG.x = 960 - SIG.w / 2 - 20; flourishCache = withLen(jit(bez([SIG.x + 10, SIG.base + 36], [SIG.x + SIG.w * .35, SIG.base + 62], [SIG.x + SIG.w * .7, SIG.base + 14], [SIG.x + SIG.w + 10, SIG.base + 30], 40), rng(5), .5, 10));
  street = buildStreet(); streetFull = mk(W, H); cacheStreet(streetFull.getContext('2d'));
  await document.fonts.ready; window.READY = true;
})();
function cacheStreet(c2) { // finished drawing, cached so later frames are cheap
  street.forEach((p) => { const pts = p.path.pts; c2.save(); c2.strokeStyle = p.color; c2.globalAlpha = p.alpha; c2.lineWidth = p.w; c2.lineCap = 'round'; c2.lineJoin = 'round'; c2.beginPath(); c2.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) c2.lineTo(pts[i][0], pts[i][1]); c2.stroke(); c2.restore(); });
}
