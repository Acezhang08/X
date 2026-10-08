// ===== v2 新增画面 + 段落装配 =====
function rack(cx, top, w, h, p, o = {}) { // 机柜正视图
  const x = cx - w / 2, c = o.c || C.line, n = o.slots || 10, sh = (h - 30) / n;
  rc(cx - w / 2, top, w, h, p, { c, w: 4 });
  for (let i = 0; i < n; i++) { rc(x + 14, top + 15 + i * sh + 3, w - 28, sh - 8, p, { c, w: 1.5, alpha: .8 }); if (p >= 1) ci(x + w - 32, top + 15 + i * sh + sh / 2 - 1, 3, 1, { c: C.cyan, w: 3 }); }
}
function blockArrow(x, y, len, th, p, col, a = .35) { // 向右的粗箭头，th 为轴粗
  const hd = Math.max(th * .7, 26), L = len * p; if (L < 4) return;
  const pts = [[x, y - th / 2], [x + Math.max(L - hd, 0), y - th / 2], [x + Math.max(L - hd, 0), y - th / 2 - hd * .5], [x + L, y], [x + Math.max(L - hd, 0), y + th / 2 + hd * .5], [x + Math.max(L - hd, 0), y + th / 2], [x, y + th / 2]];
  fillP(pts, col, a); P(pts, 1, { c: col, w: 3, close: true });
}
// 两条时间轴：芯片周期 vs 电力周期。mode 'abstract' | 'calendar'；shrink 0..1 把电力条缩短（7.6）
function twoTimelines(t, t0, mode = 'abstract', shrink = 0, marks = 0) {
  const x0 = 300, x1 = 1700, p = lin(t, t0, 1.0), yc = 290, yp = 560;
  tx('CHIPS — PRODUCT CYCLES', x0, yc - 120, { s: 40, b: 1, p }); tx('POWER — PERMITS + CONSTRUCTION', x0, yp - 120, { s: 40, b: 1, c: C.cyan, p });
  ln(x0, yc, x1, yc, p, { w: 3 }); ln(x0, yp, x1, yp, p, { w: 3, c: C.cyan });
  const q = lin(t, t0 + .6, 1.6);
  for (let i = 0; i <= 28; i++) { const x = x0 + i * (x1 - x0) / 28; if ((i / 28) <= q) { ln(x, yc - 16, x, yc + 16, 1, { w: 2.5 }); if (i % 4 === 2) chip(x, yc - 56, 26, 1, {}); } }
  if (mode === 'abstract') {
    const L0 = (x1 - x0) * .66, L = lerp(L0, (x1 - x0) * .22, eio(shrink));
    const bq = lin(t, t0 + 1.0, 1.4); fillRc(x0, yp - 40, L * bq, 80, C.cyan, .22); hatchRc(x0, yp - 40, L * bq, 80, 14, -Math.PI / 4, C.cyan, .7, 2);
    rc(x0, yp - 40, L * bq, 80, 1, { c: C.cyan, w: 3 });
    A(bq > .9 ? 1 : 0, () => { tx(shrink > .6 ? '2–3 YRS' : '5+ YRS', x0 + L + 24, yp - 16, { s: 56, b: 1 }); ln(x0 + L, yp - 40, x0 + L, yp + 40, 1, { w: 3 }); });
  } else {
    for (let y = 2026; y <= 2036; y += 2) { const x = x0 + (y - 2026) * (x1 - x0) / 10; ln(x, yp + 10, x, yp + 24, p, { c: C.cyan, w: 2 }); tx(String(y), x, yp + 62, { a: 'c', s: 32, al: p }); }
    const xf = x0 + 4 * 140, xr = x0 + 9 * 140, m1 = lin(t, t0 + marks, .8), m2 = lin(t, t0 + marks + 1.4, .8);
    P([[x0, yp], [xf, yp]], m1, { c: C.cyan, w: 10 }); P([[xf, yp], [xr, yp]], m2, { c: C.cyan, w: 10, dash: [18, 12] });
    A(m1 > .9 ? 1 : 0, () => { fillP(arcP(xf, yp, 16, 0, 6.3, 16), C.cyan, 1); tx('FIRST: 2030', xf, yp - 40, { a: 'c', s: 40, b: 1 }); });
    A(m2 > .9 ? 1 : 0, () => { fillP(arcP(xr, yp, 16, 0, 6.3, 16), C.cyan, 1); tx('REST: 2035', xr, yp - 40, { a: 'c', s: 40, b: 1 }); });
  }
}
function plantMini(cx, cy, s, p, o) { plant(cx, cy, s, p, o); }
// ---------- 段 1 新增（1.1–1.7） ----------
function sec1New(t) {
  const [t11, t12, t13, t14, t15, t16, t17] = ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7'].map(S);
  bigSheet('SHEET 1 — LOAD', t11, E('1.1') + .2, t);
  // 1.2–1.5 机柜
  A(vis(t, t12 - .1, t16 + .6, .45), () => {
    rack(560, 200, 240, 440, lin(t, t12 - .1, 1.4));
    dim(400, 200, 400, 640, 'RACK', lin(t, t12 + .8, .7), { lx: -64, ly: 12, s: 36 });
    tx('AVERAGE, 2024', 560, 150, { a: 'c', s: 36, b: 1, p: lin(t, t12 + .4, .8) });
    const c1 = lin(t, t13 - .1, .9); P([[160, 700], [560, 700], [560, 640]], c1, { c: C.cyan, w: 3 });
    A(c1 > .9 ? 1 : 0, () => tx('< 8 kW (avg)', 560, 765, { a: 'c', s: 48, b: 1 }));
    A(ap(t, t14 - .1, .5), () => { rack(1260, 200, 240, 440, lin(t, t14 - .1, 1.0)); tx('NVIDIA GB200', 1260, 150, { a: 'c', s: 36, b: 1 }); });
    const c2 = lin(t, WT('1.4', 'estimated'), 1.2);
    if (c2 > 0) { P([[900, 700], [1260, 700], [1260, 640]], c2, { c: C.cyan, w: 30, alpha: .25 }); P([[900, 700], [1260, 700], [1260, 640]], c2, { c: C.cyan, w: 18 }); }
    A(ap(t, WT('1.4', 'around') - .1, .4), () => tx('≈ 120 kW', 1260, 765, { a: 'c', s: 56, b: 1, c: C.cyan }));
    const x15 = lin(t, t15, .8); dim(710, 420, 1110, 420, '', x15); A(x15 > .9 ? 1 : 0, () => tx('×15', 910, 385, { a: 'c', s: 104, b: 1 }));
  });
  // 1.6 园区 + xAI
  A(vis(t, t16 - .1, t17 + .05, .5), () => {
    tx('ONE CAMPUS', 560, 200, { a: 'c', s: 40, b: 1, p: lin(t, t16, .8) });
    for (let r = 0; r < 2; r++) for (let c = 0; c < 4; c++) { const x = 230 + c * 200, y = 250 + r * 200, q = lin(t, t16 + .2 + (r * 4 + c) * .14, .5);
      rc(x, y, 160, 150, q, { w: 3 }); for (let i = 1; i < 4; i++) ln(x + 20, y + i * 34, x + 140, y + i * 34, q, { w: 1.5, alpha: .7 }); }
    const k = lin(t, WT('1.6', 'Elon') - .3, .9);
    A(k, () => { tx('xAI · MEMPHIS', 1430, 215, { a: 'c', s: 44, b: 1 });
      for (let i = 0; i < 4; i++) turbine(1300 + (i % 2) * 280, 310 + Math.floor(i / 2) * 120, 56, lin(t, WT('1.6', 'Elon') + i * .2, .8)); });
    A(ap(t, WT('1.6', 'one and a half') - .2, .5), () => tx('≈ 1.5 GW on-site', 1430, 610, { a: 'c', s: 60, b: 1, c: C.cyan }));
  });
  // 1.7 一吉瓦 ≈ 80 万户
  A(vis(t, t17 - .1, S('1.8') + .05, .5), () => {
    const p = lin(t, t17 - .1, .8); rc(150, 270, 230, 230, p, { c: C.cyan, w: 4 }); hatchRc(150, 270, 230, 230, 16, -Math.PI / 4, C.cyan, .6, 2); tx('1 GW', 265, 400, { a: 'c', s: 64, b: 1, al: p });
    arrow(400, 385, 600, 385, lin(t, t17 + .4, .5), { w: 5 });
    const q = clamp((t - (t17 + .8)) / (D('1.7') * .62)), n = Math.floor(80 * q);
    for (let i = 0; i < n; i++) house(660 + (i % 10) * 70, 205 + Math.floor(i / 10) * 56, 38, 1);
    A(q > 0 ? 1 : 0, () => { tx('EACH ICON', 1450, 340, { s: 32 }); tx('= 10,000 HOMES', 1450, 384, { s: 36, b: 1 }); });
    tx(roll(800000, q).replace(/\B(?=(\d{3})+(?!\d))/g, ',') + '', 960, 738, { a: 'c', s: 90, b: 1, c: C.cyan, al: p });
    tx('AVERAGE US HOMES, ALL DAY, ALL YEAR', 960, 784, { a: 'c', s: 32, al: p });
  });
}
// ---------- 段 2（SHEET 2 — EFFICIENCY） ----------
function sec2New(t) {
  const [t21, t22, t23, t24, t25, t26] = ['2.1', '2.2', '2.3', '2.4', '2.5', '2.6'].map(S);
  bigSheet('SHEET 2 — EFFICIENCY', t21, t21 + 1.8, t);
  A(vis(t, t21 + 1.4, t22 + .05, .4), () => { const p = lin(t, t21 + 1.4, 1.0); chip(900, 440, 220, p); tx('?', 1150, 520, { s: 260, b: 1, c: C.cyan, al: p }); tx('CHIPS KEEP GETTING MORE EFFICIENT', 960, 740, { a: 'c', s: 36, b: 1, al: p }); });
  // 2.2 同功率 25 倍
  A(vis(t, t22 - .1, t23 + .05, .45), () => {
    const p = lin(t, t22 - .1, .9);
    chip(430, 420, 150, p); chip(1130, 420, 150, p);
    tx('PREVIOUS GEN', 430, 255, { a: 'c', s: 36, b: 1, al: p }); tx('NEWEST SYSTEM', 1130, 255, { a: 'c', s: 36, b: 1, al: p });
    for (const x of [430, 1130]) { P([[x, 700], [x, 520]], p, { c: C.cyan, w: 14 }); tx('SAME POWER', x, 745, { a: 'c', s: 32, al: p }); }
    blockArrow(530, 420, 250, 6, lin(t, t22 + 1.0, .8), C.line, .5);
    const k = lin(t, WT('2.2', 'up to') - .3, 1.3); blockArrow(1230, 420, 330, 150, k, C.cyan, .35);
    A(k > .8 ? 1 : 0, () => { tx('25× perf / same power*', 960, 175, { a: 'c', s: 60, b: 1, c: C.cyan }); });
    A(ap(t, WT('2.2', 'certain') - .2, .5), () => tx('*Nvidia claim, specific workloads only', 100, 785, { s: 32 }));
  });
  // 2.3 两条增长曲线
  A(vis(t, t23 - .1, t24 + .05, .45), () => {
    const p = lin(t, t23 - .1, .8), bx = 300, by = 700; ln(bx, by, 1620, by, p, { w: 3 }); ln(bx, by, bx, 190, p, { w: 3 });
    tx('2017', bx, by + 48, { a: 'c', s: 32, al: p }); tx('NOW', 1560, by + 48, { a: 'c', s: 32, al: p }); tx('ELECTRICITY USE (2017 = 1)', bx + 16, 190, { s: 32, al: p });
    const q = lin(t, WT('2.3', 'grown') - .2, 2.6), N = 40;
    const dcP = Array.from({ length: N + 1 }, (_, i) => { const k = i / N; return [bx + k * 1260, by - (Math.exp(2.3 * k) - 1) * 52]; });
    const ovP = Array.from({ length: N + 1 }, (_, i) => { const k = i / N; return [bx + k * 1260, by - k * 130]; });
    P(ovP, q, { w: 5 }); P(dcP, q, { w: 7, c: C.cyan });
    A(q > .95 ? 1 : 0, () => { tx('DATA CENTERS +12%/yr', 1000, 255, { s: 44, b: 1, c: C.cyan, a: 'r' }); tx('ALL ELECTRICITY', 1560, 530, { s: 32, a: 'r' }); });
    A(ap(t, WT('2.3', 'more than four') - .1, .6), () => tx('×4 faster', 1000, 330, { a: 'r', s: 72, b: 1 }));
  });
  // 2.4 杰文斯：蒸汽机 + 煤
  A(vis(t, t24 - .1, t25 + .05, .45), () => {
    const p = lin(t, t24 - .1, 1.4), cx = 640, cy = 470;
    rc(cx - 230, cy - 60, 360, 130, p, { w: 4 }); ln(cx - 230, cy - 20, cx + 130, cy - 20, p, { w: 2 }); ln(cx - 230, cy + 30, cx + 130, cy + 30, p, { w: 2 });
    P([[cx - 150, cy - 60], [cx - 150, cy - 200], [cx - 100, cy - 200], [cx - 100, cy - 60]], p, { w: 4 });
    rc(cx + 130, cy - 40, 120, 90, p, { w: 3 }); ln(cx + 190, cy - 40, cx + 190, cy - 120, p, { w: 3 }); rc(cx + 160, cy - 160, 60, 40, p, { w: 3 });
    const fx = cx + 340, fy = cy + 10; ci(fx, fy, 100, p, { w: 4 }); if (p >= 1) for (let i = 0; i < 6; i++) { const a = t * 1.2 + i * 1.047; ln(fx, fy, fx + Math.cos(a) * 100, fy + Math.sin(a) * 100, 1, { w: 2 }); }
    ln(cx + 250, cy + 5, fx - 100, fy, p, { w: 3 });
    tx('1865 — JEVONS', 960, 175, { a: 'c', s: 56, b: 1, p: lin(t, t24 + .6, 1.0) });
    const q = ap(t, WT('2.4', "didn't") - .3, .8); A(q, () => { // 煤堆
      fillP([[1250, 640], [1450, 360], [1650, 640]], C.line, .15); P([[1250, 640], [1450, 360], [1650, 640]], 1, { w: 4 }); for (let i = 0; i < 22; i++) fillP(arcP(1300 + (i * 53 % 300), 600 - (i * 37 % 180) * (1 - Math.abs(1450 - (1300 + (i * 53 % 300))) / 220) * .0 - (i * 37 % 150), 12, 0, 6.3, 8), C.line, .8);
      tx('COAL', 1450, 700, { a: 'c', s: 40, b: 1 }); });
    A(ap(t, WT('2.4', 'increased') - .4, .6), () => { arrow(1180, 330, 1450, 330, 1, { w: 5, c: C.cyan }); tx('MORE EFFICIENT → MORE COAL', 960, 790, { a: 'c', s: 36, b: 1, c: C.cyan }); });
  });
  // 2.5 煤堆变成芯片堆
  A(vis(t, t25 - .1, t26 + .05, .45), () => {
    const k = lin(t, t25, D('2.5')); const rows = 1 + Math.floor(7 * k);
    const base = 700;
    for (let r = 0; r < rows; r++) for (let c = 0; c < 9 - r; c++) chip(960 - (8 - r) * 36 + c * 72, base - 30 - r * 66, 44, 1, {});
    ln(500, base + 10, 1420, base + 10, 1, { w: 3 });
    tx('CHEAPER TO USE', 960, 190, { a: 'c', s: 56, b: 1, p: lin(t, t25, .9) }); tx('→ MORE USES', 960, 255, { a: 'c', s: 56, b: 1, c: C.cyan, p: lin(t, t25 + .9, .9) });
  });
  // 2.6 胃口
  A(vis(t, t26 - .1, Infinity, .45), () => {
    const p = lin(t, t26 - .1, .9), cx = 960, cy = 430, k = lin(t, WT('2.6', 'grows') - .6, 2.0), r0 = 90 + 60 * k;
    for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2, R = 470 - ((t * 60 + i * 40) % 330); P([[cx + Math.cos(a) * (R + 90), cy + Math.sin(a) * (R + 90) * .7], [cx + Math.cos(a) * R, cy + Math.sin(a) * R * .7]], p, { c: C.cyan, w: 3, alpha: .8 }); }
    ci(cx, cy, r0 + 40, p, { w: 3, dash: [8, 8] }); socket(cx, cy, 240 + 40 * k, p);
    tx('EFFICIENCY DOESN’T SHRINK THE BILL', 960, 745, { a: 'c', s: 40, b: 1, p: lin(t, WT('2.6', 'Efficiency') - .2, 1.4) });
    tx('IT GROWS THE APPETITE', 960, 785, { a: 'c', s: 36, c: C.cyan, p: lin(t, WT('2.6', 'It grows') - .2, 1.0) });
  });
}
// ---------- 段 3 新增（3.5–3.8、3.15） ----------
function sec3New(t) {
  const [t35, t36, t37, t38, t39] = ['3.5', '3.6', '3.7', '3.8', '3.9'].map(S), t315 = S('3.15');
  // 3.5 排队等接入电网
  A(vis(t, t35 - .1, t36 + .05, .45), () => {
    const p = lin(t, t35 - .1, .9); tower(220, 450, 300, p); tx('GRID', 220, 660, { a: 'c', s: 36, b: 1, al: p });
    tx('INTERCONNECTION QUEUE', 1010, 250, { a: 'c', s: 44, b: 1, p: lin(t, t35 + .4, 1.0) });
    for (let i = 0; i < 12; i++) { const q = lin(t, t35 + 1.2 + i * .35, .5); plant(480 + i * 112, 470, 90, q); if (q > .2) ln(480 + i * 112 - 40, 538, 480 + i * 112 + 40, 538, q, { w: 2, alpha: .6 }); }
    dim(440, 600, 1780, 600, '', lin(t, t35 + 2.0, 1.0)); tx('APPLY → WAIT YOUR TURN', 1110, 660, { a: 'c', s: 36, al: ap(t, t35 + 3.0, .5) });
  });
  // 3.6 2,061 GW
  A(vis(t, t36 - .1, t37 + .05, .45), () => {
    const q = lin(t, WT('3.6', 'more than') - .6, 3.2), n = Math.floor(168 * q);
    for (let i = 0; i < n; i++) plant(150 + (i % 28) * 62, 170 + Math.floor(i / 28) * 78, 44, 1);
    tx(roll(2061, q).replace(/\B(?=(\d{3})+(?!\d))/g, ',') + ' GW', 960, 738, { a: 'c', s: 110, b: 1, c: C.cyan });
    tx('GENERATION + STORAGE WAITING, END OF 2025', 960, 784, { a: 'c', s: 36 });
  });
  // 3.7 申请 → 投运 > 5 年
  A(vis(t, t37 - .1, t38 + .05, .45), () => {
    const x0 = 300, x1 = 1620, y = 520, u = (x1 - x0) / 7, p = lin(t, t37 - .1, .8);
    ln(x0, y, x1, y, p, { w: 3 }); for (let i = 0; i <= 7; i++) { ln(x0 + i * u, y - 14, x0 + i * u, y + 14, p, { w: 2 }); if (i % 1 === 0) tx(String(i), x0 + i * u, y + 56, { a: 'c', s: 32, al: p }); }
    tx('YEARS', x1, y + 108, { a: 'r', s: 32, al: p }); tx('APPLY', x0, y + 108, { s: 36, b: 1, al: p });
    const q = lin(t, WT('3.7', 'typical') - .2, 2.0); fillRc(x0, y - 70, 5 * u * q, 70, C.cyan, .3); hatchRc(x0, y - 70, 5 * u * q, 70, 14, -Math.PI / 4, C.cyan, .7, 2);
    A(q > .95 ? 1 : 0, () => { arrow(x0 + 5 * u, y - 35, x1 - 40, y - 35, 1, { c: C.cyan, w: 6 }); dim(x0, y - 150, x0 + 5 * u, y - 150, '', 1); tx('> 5 YRS (median)', (x0 + x0 + 5 * u) / 2, y - 180, { a: 'c', s: 72, b: 1 }); tx('SWITCHED ON', x1 - 40, y - 60, { a: 'r', s: 44, b: 1 }); });
    tx('PROJECTS THAT CAME ONLINE IN 2025', 960, 200, { a: 'c', s: 40, b: 1, al: p });
  });
  // 3.8 13% 建成
  A(vis(t, t38 - .1, t39 + .05, .45), () => {
    let s = 11; const R = () => (s = (s * 16807) % 2147483647) / 2147483647;
    const order = Array.from({ length: 100 }, (_, i) => i).sort(() => R() - .5), built = new Set(order.slice(0, 13));
    const fade = lin(t, WT('3.8', 'only 13') - .8, 1.2);
    for (let i = 0; i < 100; i++) { const x = 360 + (i % 10) * 76, y = 220 + Math.floor(i / 10) * 52, q = lin(t, t38 - .1 + i * .012, .5);
      if (built.has(i)) plant(x, y, 38, q, { c: C.cyan }); else { A(1 - fade, () => plant(x, y, 38, q)); A(fade, () => plant(x, y, 38, 1, { dash: 1, c: C.line })); } }
    A(fade > .6 ? 1 : 0, () => { tx('13% BUILT', 1330, 400, { s: 100, b: 1, c: C.cyan }); tx('APPLIED 2000–2020', 1330, 460, { s: 40 }); });
    tx('100 PROJECTS', 1330, 240, { s: 40, b: 1, p: lin(t, t38, .8) });
  });
  // 3.15 芯片周期 vs 电力周期
  A(vis(t, t315 - .1, Infinity, .45), () => twoTimelines(t, t315 - .1, 'abstract', 0));
}
// ---------- 段 5 新增（5.3 / 5.4 / 5.9 / 5.10） ----------
function sec5New(t) {
  const [t53, t54, t59, t510, t511] = ['5.3', '5.4', '5.9', '5.10', '5.11'].map(S);
  // 5.3 谷歌 Kairos
  A(vis(t, t53 - .1, t54 + .05, .45), () => {
    const p = lin(t, t53 - .1, 1.0);
    for (let i = 0; i < 3; i++) { const x = 300 + i * 250, y = 440; rc(x - 70, y - 150, 140, 300, p, { w: 4 }); ln(x - 70, y - 90, x + 70, y - 90, p, { w: 2 }); for (let j = -2; j <= 2; j++) ln(x + j * 22, y - 70, x + j * 22, y + 100, p, { w: 2, c: C.cyan }); ci(x, y - 120, 14, p, { w: 2 }); }
    tx('SMALL MODULAR REACTORS', 550, 200, { a: 'c', s: 36, b: 1, p }); tx('KAIROS POWER × GOOGLE', 550, 700, { a: 'c', s: 40, b: 1, c: C.cyan, p });
    A(ap(t, WT('5.3', 'up to') - .2, .5), () => { tx('≤ 500 MW', 1400, 330, { a: 'c', s: 100, b: 1 }); });
    const x0 = 1050, x1 = 1760, y = 520, q = lin(t, WT('5.3', 'first') - .3, 1.0); ln(x0, y, x1, y, lin(t, t53 + 1, .8), { w: 3 });
    const xa = x0 + 40, xb = x1 - 40; for (const [yr, x] of [[2030, xa], [2035, xb]]) { ln(x, y - 14, x, y + 14, q, { w: 3 }); tx(String(yr), x, y + 58, { a: 'c', s: 44, b: 1, al: q }); }
    P([[xa, y], [xb, y]], q, { c: C.cyan, w: 8 }); A(q > .9 ? 1 : 0, () => { tx('FIRST', xa, y - 40, { a: 'c', s: 32 }); tx('THE REST', xb, y - 40, { a: 'c', s: 32 }); });
  });
  // 5.4 电网的时钟
  A(vis(t, t54 - .1, S('5.5') + .05, .45), () => { twoTimelines(t, t54 - .1, 'calendar', 0, 1.2); tx('THE GRID’S CLOCK', 1700, 720, { a: 'r', s: 40, b: 1, c: C.cyan, p: lin(t, t54 + 3.0, 1.0) }); });
  // 5.9 只有约 2% 在运行
  A(vis(t, t59 - .1, t510 + .05, .45), () => {
    const sc = 1.1, ox = 110, oy = 140, d = dots(59), dim = lin(t, WT('5.9', 'only') - .6, 1.4);
    drawRings(GEO.us.all, ox, oy, sc, 1, { c: C.line, w: 1.5, alpha: .6 });
    d.forEach(([x, y], i) => { const on = i === 17, a = on ? 1 : 1 - .85 * dim; A(a, () => { ci(ox + x * sc, oy + y * sc, 8, 1, { c: C.cyan, w: 3 }); fillP(arcP(ox + x * sc, oy + y * sc, 5, 0, 6.3, 10), C.cyan, .9); }); });
    A(dim > .5 ? 1 : 0, () => { tx('~2 GW', 1350, 320, { s: 120, b: 1, c: C.cyan }); tx('ACTUALLY RUNNING', 1350, 370, { s: 36 }); tx('OF ~90 GW ANNOUNCED', 1350, 416, { s: 36 }); });
    stamp('2% BUILT', 1520, 600, t, WT('5.9', 'Roughly') - .1, { s: 60 });
  });
  // 5.10 宣布容易，建成才是瓶颈
  A(vis(t, t510 - .1, t511 + .05, .45), () => {
    for (let i = 0; i < 12; i++) { const x = 220 + (i % 3) * 520, y = 200 + Math.floor(i / 3) * 140, built = i === 11, q = lin(t, t510 - .1 + i * .12, .5);
      if (built) { rc(x, y, 460, 110, q, { w: 4, c: C.cyan }); plant(x + 70, y + 55, 80, q, { c: C.cyan }); tx('BUILT', x + 270, y + 70, { a: 'c', s: 56, b: 1, c: C.cyan, al: q }); }
      else { rc(x, y, 460, 110, q, { w: 2, dash: [10, 8], alpha: .7 }); tx('PLANNED', x + 230, y + 68, { a: 'c', s: 44, al: q * .8 }); } }
  });
}
// ---------- 段 7 新增（7.6） ----------
function sec7New(t) {
  const t76 = S('7.6'); A(vis(t, t76 - .1, Infinity, .45), () => {
    const k = lin(t, WT('7.6', 'new lines') - .3, 2.6); twoTimelines(t, t76 - .1, 'abstract', k);
    A(ap(t, WT('7.6', 'signal') - .2, .6), () => { tx('WATCH THIS', 1440, 690, { a: 'c', s: 64, f: 'h', c: C.cyan }); arrow(1440, 640, 1100, 600, 1, { c: C.cyan, w: 4 }); });
  });
}
// ---------- 段落装配 ----------
const M = (o, d = '') => o;
const M1 = { '1.2': '1.8', '1.3': '1.9', '1.4': '1.10', '1.5': '1.11', '1.6': '1.12', '1.7': '1.13', '1.8': '1.14' };
const M2 = { '2.1': '3.1', '2.2': '3.2', '2.3': '3.3', '2.4': '3.4', '2.5': '3.9', '2.6': '3.10', '2.7': '3.11', '2.8': '3.12', '2.9': '3.13', '2.10': '3.14' };
const M3 = Object.fromEntries(Array.from({ length: 10 }, (_, i) => ['3.' + (i + 1), '4.' + (i + 1)]));
const M4 = { '4.1': '5.1', '4.2': '5.2', '4.3': '5.5', '4.4': '5.6', '4.5': '5.7', '4.6': '5.8', '4.7': '5.11', '4.8': '5.12', '4.9': '5.13' };
const M5 = Object.fromEntries(Array.from({ length: 6 }, (_, i) => ['5.' + (i + 1), '6.' + (i + 1)]));
const M6 = Object.fromEntries(Array.from({ length: 5 }, (_, i) => ['6.' + (i + 1), '7.' + (i + 1)]));
const M7 = Object.fromEntries(Array.from({ length: 4 }, (_, i) => ['7.' + (i + 1), '8.' + (i + 1)]));
const SECS = [
  ['0', 'SHEET 0 — INTRO', sec0],
  ['1', 'SHEET 1 — LOAD', t => { mapped(M1, sec1)(t); sec1New(t); }],
  ['2', 'SHEET 2 — EFFICIENCY', sec2New],
  ['3', 'SHEET 3 — TIME', t => { mapped(M2, sec2)(t); sec3New(t); }],
  ['4', 'SHEET 4 — PRICE', mapped(M3, sec3)],
  ['5', 'SHEET 5 — WORKAROUND', t => { mapped(M4, sec4)(t); sec5New(t); }],
  ['6', 'SHEET 6 — FLIP', mapped(M5, sec5)],
  ['7', 'SHEET 7 — CALL', t => { mapped(M6, sec6)(t); sec7New(t); }],
  ['8', 'SHEET 8 — YOU', mapped(M7, sec7)],
];
