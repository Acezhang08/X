// ===== 蓝图引擎：所有画面都是时间 t 的纯函数 =====
const W = 1920, H = 1080;
const C = { bg: '#0E2A47', line: '#F4F1EA', cyan: '#6FD3F7', amber: '#FFB547', red: '#E5484D' };
const cv = document.getElementById('c'); cv.width = W; cv.height = H;
const g = cv.getContext('2d');
const MONO = '"JB", "DejaVu Sans Mono", monospace', HAND = '"AD", "Architects Daughter", cursive';
let TL = null;
let IDM = {}; const rid = id => IDM[id] || id;      // 旧画面代码用的是 5 分钟版编号，按段临时映射到 v2 编号
const S = id => TL.byId[rid(id)].start, E = id => TL.byId[rid(id)].end, D = id => E(id) - S(id);
const mapped = (m, fn) => t => { const o = IDM; IDM = m; try { fn(t); } finally { IDM = o; } };
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const eo = x => 1 - Math.pow(1 - x, 3);
const eio = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const ap = (t, t0, d = .8) => eo(clamp((t - t0) / d));       // 0→1 渐入
const lin = (t, t0, d) => clamp((t - t0) / d);
const lerp = (a, b, k) => a + (b - a) * k;
// 估算某个短语在一句旁白里被读到的时刻（按字符权重比例）
function WT(id, phrase) {
  const L = TL.byId[rid(id)], s = L.en, i = s.indexOf(phrase); if (i < 0) return L.start;
  const wgt = (str) => { let w = 0; for (const ch of str) w += /[0-9]/.test(ch) ? 2.6 : /[,:;—]/.test(ch) ? 5 : /[.?!]/.test(ch) ? 9 : 1; return w; };
  return L.start + (L.end - L.start) * wgt(s.slice(0, i)) / wgt(s);
}
// ---------- 线条原语 ----------
function plen(pts) { let L = 0; for (let i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); return L; }
function cut(pts, p) {
  if (p >= 1) return pts; if (p <= 0) return [];
  const target = plen(pts) * p, out = [pts[0]]; let acc = 0;
  for (let i = 1; i < pts.length; i++) {
    const seg = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    if (acc + seg >= target) { const k = (target - acc) / seg; out.push([lerp(pts[i - 1][0], pts[i][0], k), lerp(pts[i - 1][1], pts[i][1], k)]); return out; }
    out.push(pts[i]); acc += seg;
  }
  return out;
}
function P(pts, p = 1, o = {}) {
  const q = cut(o.close ? [...pts, pts[0]] : pts, p); if (q.length < 2) return;
  g.save(); g.globalAlpha = (o.alpha ?? 1) * g.globalAlpha; g.strokeStyle = o.c || C.line; g.lineWidth = o.w || 3; g.lineJoin = 'round'; g.lineCap = o.cap || 'round';
  if (o.dash) { g.setLineDash(o.dash); g.lineDashOffset = o.off || 0; }
  g.beginPath(); g.moveTo(q[0][0], q[0][1]); for (let i = 1; i < q.length; i++) g.lineTo(q[i][0], q[i][1]); g.stroke(); g.restore();
}
const ln = (x1, y1, x2, y2, p = 1, o) => P([[x1, y1], [x2, y2]], p, o);
const rcP = (x, y, w, h) => [[x, y], [x + w, y], [x + w, y + h], [x, y + h], [x, y]];
const rc = (x, y, w, h, p = 1, o) => P(rcP(x, y, w, h), p, o);
const arcP = (cx, cy, r, a0, a1, n = 48) => Array.from({ length: n + 1 }, (_, i) => { const a = lerp(a0, a1, i / n); return [cx + r * Math.cos(a), cy + r * Math.sin(a)]; });
const ci = (cx, cy, r, p = 1, o) => P(arcP(cx, cy, r, -Math.PI / 2, Math.PI * 1.5, 64), p, o);
function fillP(pts, col, a = .3) { g.save(); g.globalAlpha *= a; g.fillStyle = col; g.beginPath(); pts.forEach((q, i) => i ? g.lineTo(q[0], q[1]) : g.moveTo(q[0], q[1])); g.closePath(); g.fill(); g.restore(); }
function fillRc(x, y, w, h, col, a = .3) { fillP(rcP(x, y, w, h), col, a); }
function hatch(pts, sp = 18, ang = -Math.PI / 4, col = C.cyan, a = .8, w = 2, p = 1) {
  g.save(); g.beginPath(); pts.forEach((q, i) => i ? g.lineTo(q[0], q[1]) : g.moveTo(q[0], q[1])); g.closePath(); g.clip();
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; pts.forEach(q => { x0 = Math.min(x0, q[0]); y0 = Math.min(y0, q[1]); x1 = Math.max(x1, q[0]); y1 = Math.max(y1, q[1]); });
  const R = Math.hypot(x1 - x0, y1 - y0), cx = (x0 + x1) / 2, cy = (y0 + y1) / 2, ca = Math.cos(ang), sa = Math.sin(ang);
  g.strokeStyle = col; g.lineWidth = w; g.globalAlpha *= a * clamp(p); g.beginPath();
  for (let d = -R; d <= R; d += sp) { g.moveTo(cx + d * -sa - R * ca, cy + d * ca - R * sa); g.lineTo(cx + d * -sa + R * ca, cy + d * ca + R * sa); }
  g.stroke(); g.restore();
}
const hatchRc = (x, y, w, h, ...r) => hatch(rcP(x, y, w, h), ...r);
function drawRings(rings, ox, oy, sc, p = 1, o = {}) { for (const r of rings) P(r.map(q => [ox + q[0] * sc, oy + q[1] * sc]), p, { w: 2, ...o, close: true }); }
function fillRings(rings, ox, oy, sc, col, a = .3, hat) {
  for (const r of rings) { const pts = r.map(q => [ox + q[0] * sc, oy + q[1] * sc]); if (a) fillP(pts, col, a); if (hat) hatch(pts, hat, -Math.PI / 4, col, .7, 2); }
}
function tx(s, x, y, o = {}) {
  g.save(); g.globalAlpha *= o.al ?? 1; g.fillStyle = o.c || C.line; g.textBaseline = o.bl || 'alphabetic';
  g.font = `${o.b ? '700 ' : ''}${o.s || 32}px ${o.f === 'h' ? HAND : MONO}`; g.textAlign = { l: 'left', c: 'center', r: 'right' }[o.a || 'l'];
  if (o.p !== undefined) s = s.slice(0, Math.floor(s.length * clamp(o.p)) + (o.p > 0 && o.p < 1 ? 0 : 0));
  if (o.rot) { g.translate(x, y); g.rotate(o.rot); x = 0; y = 0; }
  g.fillText(s, x, y); g.restore();
}
const tw = (s, o = {}) => { g.save(); g.font = `${o.b ? '700 ' : ''}${o.s || 32}px ${o.f === 'h' ? HAND : MONO}`; const w = g.measureText(s).width; g.restore(); return w; };
function arrowHead(x, y, ang, sz = 16, o = {}) { P([[x - sz * Math.cos(ang - .45), y - sz * Math.sin(ang - .45)], [x, y], [x - sz * Math.cos(ang + .45), y - sz * Math.sin(ang + .45)]], 1, o); }
function arrow(x1, y1, x2, y2, p = 1, o = {}) { ln(x1, y1, x2, y2, p, o); if (p >= 1) arrowHead(x2, y2, Math.atan2(y2 - y1, x2 - x1), o.sz || 18, o); }
// 尺寸标注线
function dim(x1, y1, x2, y2, label, p = 1, o = {}) {
  const a = Math.atan2(y2 - y1, x2 - x1), nx = -Math.sin(a), ny = Math.cos(a), c = o.c || C.line;
  ln(x1, y1, x2, y2, p, { c, w: 2 });
  if (p > .02) { ln(x1 + nx * 14, y1 + ny * 14, x1 - nx * 14, y1 - ny * 14, 1, { c, w: 2 }); arrowHead(x1, y1, a + Math.PI, 14, { c, w: 2 }); }
  if (p >= 1) { ln(x2 + nx * 14, y2 + ny * 14, x2 - nx * 14, y2 - ny * 14, 1, { c, w: 2 }); arrowHead(x2, y2, a, 14, { c, w: 2 }); }
  if (label && p >= 1) { const mx = (x1 + x2) / 2 + (o.lx || 0), my = (y1 + y2) / 2 + (o.ly ?? -16); tx(label, mx, my, { a: 'c', c: o.lc || c, s: o.s || 32 }); }
}
// 数字滚动
const roll = (v, p, dec = 0) => (v * eo(clamp(p))).toFixed(dec);
// 印章（只能用 3 次）
function stamp(text, cx, cy, t, t0, o = {}) {
  const k = clamp((t - t0) / .28); if (k <= 0) return;
  const sc = lerp(2.2, 1, eo(k)), al = clamp(k * 1.6);
  const fs = o.s || 48; g.font = `700 ${fs}px ${MONO}`; const w = g.measureText(text).width + 64, h = fs + 44;
  g.save(); g.translate(cx, cy); g.rotate(o.rot ?? -.12); g.scale(sc, sc); g.globalAlpha *= al;
  g.fillStyle = 'rgba(14,42,71,0.55)'; g.fillRect(-w / 2, -h / 2, w, h);
  rc(-w / 2, -h / 2, w, h, 1, { c: C.red, w: 6 }); rc(-w / 2 + 12, -h / 2 + 12, w - 24, h - 24, 1, { c: C.red, w: 2 });
  tx(text, 0, fs * .35, { a: 'c', c: C.red, s: fs, b: 1 });
  g.restore();
  if (k >= 1 && t - t0 < .5) { const r = (t - t0 - .28) / .22; g.save(); g.globalAlpha *= (1 - r) * .5; g.strokeStyle = C.red; g.lineWidth = 3; g.strokeRect(cx - w / 2 - r * 40, cy - h / 2 - r * 40, w + r * 80, h + r * 80); g.restore(); }
}
// 引语卡片
function wrap(s, maxW, o) { const words = s.split(' '), lines = []; let cur = ''; for (const w of words) { const t2 = cur ? cur + ' ' + w : w; if (tw(t2, o) > maxW && cur) { lines.push(cur); cur = w; } else cur = t2; } if (cur) lines.push(cur); return lines; }
function quote(text, src, x, y, w, t, t0, o = {}) {
  const k = ap(t, t0, .6); if (k <= 0) return; const fs = o.s || 36, lh = fs * 1.4;
  const lines = wrap(text, w - 80, { s: fs, f: 'h' }), sl = wrap(src, w - 100, { s: 32 }), h = lines.length * lh + 90 + sl.length * 40;
  g.save(); g.globalAlpha *= k * (o.al ?? 1); g.translate(0, (1 - k) * 24);
  g.fillStyle = 'rgba(14,42,71,0.88)'; g.fillRect(x, y, w, h); rc(x, y, w, h, 1, { w: 3 }); rc(x + 8, y + 8, w - 16, h - 16, 1, { w: 1.5, alpha: .6 });
  tx('“', x + 22, y + 74, { s: 96, c: C.cyan, f: 'h' });
  lines.forEach((l, i) => tx(l, x + 76, y + 62 + i * lh, { s: fs, f: 'h' }));
  ln(x + 40, y + h - 26 - sl.length * 40, x + w - 40, y + h - 26 - sl.length * 40, 1, { w: 1.5, dash: [8, 6] });
  sl.forEach((l, i) => tx((i ? '  ' : '— ') + l, x + 40, y + h - 20 - (sl.length - 1 - i) * 40, { s: 32, c: C.cyan }));
  g.restore(); return h;
}
