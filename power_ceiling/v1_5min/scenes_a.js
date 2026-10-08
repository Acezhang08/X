// ===== 段 0–3 =====
const vis = (t, a, b, f = .4) => clamp((t - a) / f) * (b === Infinity ? 1 : clamp((b - t) / f));
const A = (al, fn) => { if (al <= .003) return; g.save(); g.globalAlpha *= al; fn(); g.restore(); };
function bigSheet(name, t0, t1, t) { A(vis(t, t0, t1, .3), () => { const p = lin(t, t0, .9); const s = name; tx(s, 960, 400, { a: 'c', s: 72, b: 1, p }); ln(960 - tw(s, { s: 72, b: 1 }) / 2, 430, 960 + tw(s, { s: 72, b: 1 }) / 2, 430, p, { c: C.cyan, w: 3 }); }); }
// 悬空的芯片 + 断开的插头
function chipRow(cx0, y, n, t, t0, gap = 230) {
  for (let i = 0; i < n; i++) { const cx = cx0 + i * gap, p = lin(t, t0 + i * .15, .6);
    chip(cx, y - 46, 70, p);
    if (p >= 1) { plug(cx + 100, y - 46, 40, 1); socket(cx + 175, y - 46, 44, 1); const fl = (Math.sin(t * 17 + i * 3) > .3) ? 1 : 0; if (fl) { ln(cx + 128, y - 46, cx + 150, y - 40, 1, { c: C.cyan, w: 2 }); ln(cx + 132, y - 56, cx + 150, y - 50, 1, { c: C.cyan, w: 2 }); } }
  }
  ln(cx0 - 80, y, cx0 + (n - 1) * gap + 210, y, lin(t, t0, .8), { w: 3 });
}
function shelves(t, t0, x0 = 120) { for (let r = 0; r < 3; r++) chipRow(x0 + 70, 330 + r * 160, 4, t, t0 + r * .25); }
function sec0(t) {
  const t01 = S('0.1'), t02 = S('0.2'), t03 = S('0.3'), t04 = S('0.4'), t05 = S('0.5');
  // 0.1 CEO 剪影 + 微软大楼
  A(vis(t, t01, t02 + .05, .5), () => {
    const p = lin(t, t01, 1.4);
    person(600, 470, 400, p); tx('CEO', 600, 740, { a: 'c', s: 36, f: 'h', al: p });
    rc(1000, 300, 420, 440, p, { w: 3 }); for (let i = 0; i < 4; i++) for (let j = 0; j < 3; j++) rc(1040 + j * 120, 340 + i * 95, 80, 60, p, { w: 1.5 });
    tx('MICROSOFT', 1210, 280, { a: 'c', s: 40, b: 1, p: lin(t, t01 + .6, .8) });
    const bp = lin(t, t01 + 1.4, .6); P([[760, 320], [980, 320], [980, 440], [830, 440], [790, 490], [800, 440], [760, 440], [760, 320]], bp, { w: 3 });
    tx('?!', 870, 405, { a: 'c', s: 64, b: 1, al: bp });
  });
  // 0.2 / 0.3 货架 + 引语卡片
  const aShelf = vis(t, t02, t04 + .05, .5) * (1 - .88 * ap(t, t03, .5));
  A(aShelf, () => { shelves(t, t02); tx('INVENTORY', 120, 215, { s: 40, b: 1, p: lin(t, t02 + .3, .6) }); dim(120, 240, 1000, 240, '', lin(t, t02 + .5, .8)); });
  quote('…you may actually have a bunch of chips sitting in inventory that I can’t plug in.', 'Satya Nadella, Microsoft CEO — BG2 Pod, Nov 2025', 1100, 200, 700, t, t02 + .9, { al: (1 - ap(t, t03, .35)) * vis(t, t02, t04 + .05, .3) });
  quote('The biggest issue we are now having is not a compute glut, but it’s power.', 'Satya Nadella, Microsoft CEO — BG2 Pod, Nov 2025', 1100, 200, 700, t, t03 + .45, { al: vis(t, t03, t04 + .05, .3) });
  // 0.3 插头特写
  A(vis(t, t03 + .3, t04 + .05, .5) * .95, () => { const p = lin(t, t03 + .3, .8);
    plug(430, 620, 190, p); socket(760, 620, 210, p);
    if (p >= 1) { const j = Math.sin(t * 21) > 0; if (j) { P([[560, 600], [590, 630], [575, 640], [610, 670]], 1, { c: C.cyan, w: 3 }); } dim(560, 720, 700, 720, 'GAP', 1, { s: 32 }); } });
  A(vis(t, t03 + 1.6, t04 + .05, .05) , () => stamp('NO POWER', 640, 470, t, t03 + 1.6, { s: 56 }));
  // 0.4 / 0.5 建筑剖面 + 琥珀虚线屋顶
  A(vis(t, t04, Infinity, .5), () => {
    const p = lin(t, t04, 1.3);
    P([[600, 360], [600, 740], [1320, 740], [1320, 360]], p, { w: 4 });
    ln(600, 487, 1320, 487, p, { w: 2 }); ln(600, 613, 1320, 613, p, { w: 2 });
    for (let f = 0; f < 3; f++) for (let k = 0; k < 6; k++) rc(640 + k * 112, 395 + f * 126, 70, 70, p, { w: 1.5 });
    const end = lerp(1450, 960, eio(lin(t, t05 + 1.2, 1.0)));
    const roof = [[480, 360], [end, 360]]; P(roof, lin(t, t04 + .2, 1.0), { c: C.amber, w: 5, dash: [22, 14] });
    tx('CEILING?', 700, 300, { s: 72, b: 1, c: C.amber, p: lin(t, t04 + .9, .7), al: 1 - .0 });
  });
}
// ---------- 段 1 ----------
function sec1(t) {
  const t11 = S('1.1'), t12 = S('1.2'), t13 = S('1.3'), t14 = S('1.4'), t15 = S('1.5'), t16 = S('1.6'), t17 = S('1.7'), t18 = S('1.8');
  bigSheet('SHEET 1 — LOAD', t11, t12 - .1, t);
  // 1.2 计数器 → 1.3 缩到左上
  const mv = ap(t, t13, .8), cs = lerp(200, 72, mv), cxn = lerp(960, 100, mv), cyn = lerp(470, 150, mv), al = vis(t, t12, t15 + .05, .4);
  A(al, () => {
    A(1 - mv, () => dc(960, 215, 140, lin(t, t12, .8)));
    const v = roll(415, (t - WT('1.2', '415') + 1.6) / 1.6), wF = tw('415', { s: cs, b: 1 }), wU = tw('TWh', { s: cs * .45 });
    const x0 = lerp(960 - (wF + wU + 20) / 2, 100, mv);
    tx(v, x0 + wF, cyn, { s: cs, b: 1, a: 'r' }); tx('TWh', x0 + wF + 20, cyn, { s: cs * .45, c: C.cyan });
    tx('DATA CENTERS, 2024', lerp(960, 100, mv), cyn + lerp(90, 44, mv), { s: 36, a: mv > .5 ? 'l' : 'c', p: lin(t, t12 + .3, .9) });
  });
  // 1.3 全球圆 + 1.5% 扇形
  A(vis(t, t13 + .2, t15 + .05, .5), () => {
    const cx = 1150, cy = 440, r = 250, p = lin(t, t13 + .2, 1.0);
    ci(cx, cy, r, p, { w: 4 }); ci(cx, cy, r + 16, p, { w: 1.5, alpha: .5 });
    tx('ALL ELECTRICITY USED IN THE WORLD', cx, cy - r - 36, { a: 'c', s: 32, al: p });
    const a0 = -Math.PI / 2, a1 = a0 + .094 * clamp(lin(t, t13 + 1.3, .6) * 1);
    if (t > t13 + 1.2) { const pts = [[cx, cy], ...arcP(cx, cy, r, a0, a0 + 0.094, 8)]; fillP(pts, C.cyan, .9);
      ln(cx + 10, cy - r + 30, cx + 360, cy - r + 10, lin(t, t13 + 1.6, .5), { c: C.cyan, w: 2 }); tx('1.5%', cx + 380, cy - r + 36, { s: 80, b: 1, c: C.cyan, p: lin(t, t13 + 1.9, .4) }); }
    A(ap(t, t14, .5), () => tx('?', cx + 20, cy + 60, { a: 'c', s: 220, b: 1, c: C.cyan, al: .9 }));
  });
  // 1.5 柱子 + Japan
  A(vis(t, t15 - .2, t17 + .05, .5), () => {
    const base = 740, k = .52, x1 = 460, x2 = 800;
    ln(340, base, 1760, base, lin(t, t15 - .1, .6), { w: 3 });
    const h1 = 415 * k * ap(t, t15, .7); rc(x1, base - h1, 180, h1, 1, { w: 3 }); hatchRc(x1, base - h1, 180, h1, 16, -Math.PI / 4, C.line, .4, 1.5);
    tx('415 TWh', x1 + 90, base - h1 - 14, { a: 'c', s: 40, al: ap(t, t15 + .3, .4) });
    tx('2024', x1 + 90, base + 44, { a: 'c', s: 32 }); tx('2030', x2 + 90, base + 44, { a: 'c', s: 32 });
    const t945 = WT('1.5', '945') - .2, pk = clamp((t - t945) / 1.2), h2 = 945 * k * eo(pk) ;
    rc(x2, base - h2, 180, h2, 1, { w: 3 }); hatchRc(x2, base - h2, 180, h2, 16, -Math.PI / 4, C.cyan, .6, 1.5);
    tx('945 TWh', x2 + 90, base - h2 - 14, { a: 'c', s: 40, b: 1, al: pk > .6 ? 1 : 0 });
    A(ap(t, t945 + 1.2, .5), () => { const top1 = base - 415 * k, top2 = base - 945 * k;
      ln(x1 + 180, top1, 740, top1, 1, { dash: [8, 6], w: 2 }); ln(x2, top2, 740, top2, 1, { dash: [8, 6], w: 2 });
      dim(740, top1, 740, top2, '', lin(t, t945 + 1.2, .6), { c: C.amber }); tx('×2+', 690, (top1 + top2) / 2 + 24, { a: 'r', s: 72, b: 1, c: C.amber }); });
    // Japan
    A(ap(t, t16, .6), () => { const hJ = 945 * k, sc = hJ / GEO.japan._h * 1.0 * 1; const jx = 1230, jy = base - hJ;
      rc(jx - 30, jy - 10, GEO.japan.jp.reduce((m, r) => Math.max(m, ...r.map(q => q[0])), 0) * sc + 60, hJ + 10, 1, { w: 1.5, dash: [6, 8], alpha: .5 });
      drawRings(GEO.japan.jp, jx, jy, sc, lin(t, t16, 1.0), { c: C.cyan, w: 3 });
      ln(x2 + 180, jy, jx - 30, jy, lin(t, t16 + .2, .6), { dash: [8, 6], w: 2 }); tx('JAPAN, TODAY', jx + 190, base + 46, { a: 'c', s: 36, b: 1, p: lin(t, t16 + .5, .6) });
      tx('≈', 1100, jy + 12, { a: 'c', s: 72, b: 1, al: lin(t, t16 + .8, .3) }); });
  });
  // 1.7 世界地图
  A(vis(t, t17 - .1, t18 + .05, .5), () => {
    const sc = 1.0, ox = 80, oy = 200, p = lin(t, t17 - .1, 1.0);
    drawRings(GEO.world.land, ox, oy, sc, p, { c: C.line, w: 1.8, alpha: .8 });
    const ap2 = lin(t, WT('1.7', 'The United') - .3, .8); fillRings(GEO.world.usa, ox, oy, sc, C.cyan, .22 * ap2, 12); drawRings(GEO.world.usa, ox, oy, sc, ap2, { c: C.cyan, w: 3 });
    const us = GEO.world.usa[0]; const ux = ox + us.reduce((s, q) => s + q[0], 0) / us.length * sc, uy = oy + us.reduce((s, q) => s + q[1], 0) / us.length * sc;
    A(ap2, () => { P([[ux, uy], [ux, 150], [1190, 150], [1190, 300]], 1, { c: C.cyan, w: 2 }); tx('45%', 1210, 350, { s: 160, b: 1, c: C.cyan }); tx('OF WORLD DATA CENTER', 1200, 410, { s: 36 }); tx('ELECTRICITY IS USED', 1200, 454, { s: 36 }); tx('IN THE UNITED STATES', 1200, 498, { s: 36 }); });
  });
  // 1.8 向上箭头
  A(vis(t, t18 - .1, Infinity, .5), () => {
    const p = lin(t, t18 - .1, 1.2), pts = [[620, 110], [800, 330], [710, 330], [710, 740], [530, 740], [530, 330], [440, 330]];
    P(pts, p, { w: 4, close: true });
    const h = ap(t, WT('1.8', 'nearly half') - .2, 1.0);
    if (h > 0) { const y1 = lerp(740, 425, h); fillRc(530, y1, 180, 740 - y1, C.cyan, .35); hatchRc(530, y1, 180, 740 - y1, 14, -Math.PI / 4, C.cyan, .7, 2); ln(430, 425, 810, 425, h, { c: C.cyan, w: 2, dash: [10, 8] }); }
    A(h, () => { tx('≈ 50% OF GROWTH', 900, 430, { s: 56, b: 1, c: C.cyan }); tx('IN US ELECTRICITY DEMAND', 900, 500, { s: 36 }); tx('THROUGH 2030', 900, 548, { s: 36 }); tx('= DATA CENTERS', 900, 596, { s: 36, c: C.cyan }); });
  });
}
// ---------- 段 2 ----------
function sec2(t) {
  const [t21, t22, t23, t24, t25, t26, t27, t28, t29, t210] = ['2.1', '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '2.8', '2.9', '2.10'].map(S);
  // 2.1 沿导线平移 → 2.2 断开 + 沙漏
  A(vis(t, t21 - .2, t23 + .05, .4), () => {
    const cam = 1500 * eio(lin(t, t21 - .1, 1.7));
    g.save(); g.translate(-cam, 0);
    ln(-200, 430, 2380, 430, 1, { c: C.cyan, w: 4 }); ln(2540, 430, 3200, 430, 1, { c: C.cyan, w: 4 });
    for (let k = 0; k < 6; k++) { tower(300 + k * 620, 540, 460, 1); }
    for (let k = 0; k < 5; k++) P(Array.from({ length: 21 }, (_, i) => { const x = 300 + k * 620 + i * 31; return [x, 410 + Math.sin(i / 20 * Math.PI) * 50]; }), 1, { w: 2, alpha: .7 });
    dc(3060, 560, 200, 1); g.restore();
    const brk = ap(t, t22 + .6, .5);
    A(brk, () => { const hx = 960; hourglass(hx, 430, 170, 1, .5 + .5 * Math.sin(t * 2) * .3 + .1); tx('ELECTRICITY', 330, 220, { s: 40, b: 1, c: C.cyan }); tx('DATA CENTER', 1630, 220, { s: 40, b: 1, a: 'r' }); tx('TIME TO CONNECT', 960, 290, { a: 'c', s: 40, b: 1 }); });
  });
  // 2.3 供电链
  const xs = [300, 700, 1130, 1560], names = ['POWER PLANTS', 'TRANSMISSION LINES', 'TRANSFORMERS', 'DATA CENTER'];
  A(vis(t, t23, t25 + .05, .4), () => {
    const times = [WT('2.3', 'power plants') - .3, WT('2.3', 'transmission') - .3, WT('2.3', 'transformers') - .3, t23 + .8];
    const ps = times.map(tt => lin(t, tt, .8));
    plant(xs[0], 380, 220, ps[0]); tower(xs[1], 380, 260, ps[1]); trafo(xs[2], 380, 230, ps[2]); dc(xs[3], 380, 190, ps[3]);
    [0, 1, 2].forEach(i => { ln(xs[i] + 120, 470, xs[i + 1] - 120, 470, Math.min(ps[i], ps[i + 1]) > 0 ? lin(t, times[i + 1] + .2, .6) : 0, { c: C.cyan, w: 4 }); });
    names.forEach((n, i) => tx(n, xs[i], 640, { a: 'c', s: 32, p: ps[i] }));
    // 2.4 排队计时器
    xs.forEach((x, i) => { const k = ap(t, t24 + .25 * i, .5); if (k > 0) { const o = { al: k }; A(k, () => { clock(x, 170, 44, t + i, 1); for (let j = 0; j < 4; j++) { ci(x - 60 + j * 40, 262, 9, 1, { w: 2.5 }); } dim(x - 70, 120, x + 70, 120, '', 1, { w: 1 }); tx('QUEUE', x, 98, { a: 'c', s: 32 }); }); } });
  });
  // 2.5 输电线时间轴
  A(vis(t, t25 - .1, t26 + .05, .4), () => {
    tower(400, 430, 560, lin(t, t25 - .1, 1.0));
    const x0 = 760, x1 = 1700, u = (x1 - x0) / 8, y = 560, p = lin(t, t25 + .2, 1.0);
    ln(x0, y, x1, y, p, { w: 3 }); for (let i = 0; i <= 8; i++) { ln(x0 + i * u, y - 14, x0 + i * u, y + 14, p, { w: 2 }); if (i % 2 == 0) tx(String(i), x0 + i * u, y + 56, { a: 'c', s: 36, al: p }); }
    tx('YEARS TO BUILD', x0, y + 120, { s: 32, al: p });
    const q = lin(t, WT('2.5', 'four to eight') - .2, 1.0); fillRc(x0 + 4 * u, y - 80, 4 * u * q, 80, C.cyan, .25); hatchRc(x0 + 4 * u, y - 80, 4 * u * q, 80, 14, -Math.PI / 4, C.cyan, .7, 2);
    A(q > .8 ? 1 : 0, () => { dim(x0 + 4 * u, y - 130, x1, y - 130, '', 1); tx('4–8 YRS', (x0 + 4 * u + x1) / 2, y - 160, { a: 'c', s: 72, b: 1 }); tx('NEW TRANSMISSION LINE · ADVANCED ECONOMIES', 760, 250, { s: 32 }); });
  });
  // 2.6 变压器
  A(vis(t, t26 - .1, t27 + .05, .4), () => {
    trafo(470, 430, 400, lin(t, t26 - .1, 1.0)); tx('LARGE POWER TRANSFORMER', 470, 700, { a: 'c', s: 32 });
    const x0 = 960, x1 = 1720, y = 330; ln(x0, y, x1, y, lin(t, t26 + .1, .8), { w: 3 }); for (let i = 0; i <= 4; i++) { ln(x0 + i * (x1 - x0) / 4, y - 12, x0 + i * (x1 - x0) / 4, y + 12, 1, { w: 2, alpha: lin(t, t26 + .3, .4) }); tx(String(i), x0 + i * (x1 - x0) / 4, y + 52, { a: 'c', s: 32, al: lin(t, t26 + .3, .4) }); }
    const q = lin(t, WT('2.6', 'up to four') - .1, .9); fillRc(x0, y - 70, (x1 - x0) * q, 70, C.cyan, .3); hatchRc(x0, y - 70, (x1 - x0) * q, 70, 12, -Math.PI / 4, C.cyan, .7, 2);
    tx('LEAD TIME, YEARS', x0, y - 100, { s: 32 }); A(q > .9 ? 1 : 0, () => tx('≤ 4 YRS', x1, y - 100, { a: 'r', s: 64, b: 1 }));
    const pk = lin(t, WT('2.6', 'prices') - .1, 1.2); arrow(1050, 700, 1050, lerp(700, 470, eo(pk)), 1, { w: 6, c: C.cyan }); A(pk > .7 ? 1 : 0, () => { tx('+80%', 1120, 560, { s: 110, b: 1, c: C.cyan }); tx('PRICE, LAST 5 YEARS', 1120, 620, { s: 32 }); });
  });
  // 2.7 燃气轮机 + 印章
  A(vis(t, t27 - .1, t28 + .05, .4), () => {
    turbine(960, 400, 260, lin(t, t27 - .1, 1.3)); tx('GAS TURBINE', 960, 190, { a: 'c', s: 40, b: 1 }); tx('MAKER: GE VERNOVA', 960, 232, { a: 'c', s: 32, al: lin(t, t27 + .5, .6) });
    stamp('SOLD OUT → 2028', 960, 640, t, WT('2.7', 'sold out') - .1, { s: 52 });
  });
  // 2.8 十栋数据中心
  A(vis(t, t28 - .1, t29 + .05, .4), () => {
    tx('PLANNED DATA CENTER PROJECTS', 960, 230, { a: 'c', s: 40, b: 1, p: lin(t, t28, .8) });
    const flip = lin(t, WT('2.8', '20 percent') - .2, .8);
    for (let i = 0; i < 10; i++) { const x = 200 + i * 170, risk = i >= 8; if (risk && flip > .1) { A(1 - flip, () => dc(x, 420, 100, lin(t, t28 + i * .08, .5))); dc(x, 420, 100, 1, { dash: 1, c: C.line }); } else dc(x, 420, 100, lin(t, t28 + i * .08, .5)); }
    A(flip > .9 ? 1 : 0, () => { dim(1480, 520, 1810, 520, '', 1); tx('≈20% AT RISK', 1645, 590, { a: 'c', s: 44, b: 1 }); tx('DELAYED?', 1645, 640, { a: 'c', s: 32 }); });
  });
  // 2.9 / 2.10 缺口 32 GW
  A(vis(t, t29 - .1, Infinity, .4), () => {
    const p = lin(t, t29 - .1, 1.0), x = 460, y = 220, w = 1000, h = 420;
    tx('US DATA CENTER POWER NEED THROUGH 2028', 960, 180, { a: 'c', s: 36, b: 1 });
    rc(x, y, w, h, p, { w: 4 });
    const q = lin(t, WT('2.9', 'a shortfall') - .1, 1.0), gx = x + w * (1 - .34 * q);
    if (q > 0) { hatchRc(gx, y, x + w - gx, h, 22, -Math.PI / 4, C.line, .6, 2); ln(gx, y, gx, y + h, 1, { dash: [10, 8], w: 3 }); }
    const fl = t > t210 ? Math.max(0, Math.sin((t - t210) * 5)) * clamp((t - t210 + .2) / .3) * clamp(1 - (t - t210 - 1.4) / .3) : 0;
    if (fl > 0) { fillRc(gx, y, x + w - gx, h, C.amber, .55 * fl); hatchRc(gx, y, x + w - gx, h, 22, -Math.PI / 4, C.amber, .9 * fl, 3); }
    A(q > .9 ? 1 : 0, () => { fillRc(gx + 24, 360, 270, 140, C.bg, .85); tx('−32 GW', gx + 160, 440, { a: 'c', s: 84, b: 1, c: fl > .3 ? C.amber : C.line }); dim(gx, y + h + 50, x + w, y + h + 50, '', 1); tx('≈ 1/3 OF NEED', (gx + x + w) / 2, y + h + 110, { a: 'c', s: 36, b: 1 }); });
  });
}
