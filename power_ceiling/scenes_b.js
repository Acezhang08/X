// ===== 段 3–7 =====
function houses(cx0, y, n, p, gap = 230, s = 130) { for (let i = 0; i < n; i++) house(cx0 + i * gap, y, s, lin(p, i * .12, .5)); }
function billDraw(t, t0, x, y) {
  const p = lin(t, t0, .9); bill(x, y, 420, 520, p);
  tx('ELECTRIC BILL', x + 36, y + 56, { s: 36, b: 1, p: lin(t, t0 + .3, .6) }); tx('WASHINGTON, D.C.', x + 36, y + 96, { s: 32, c: C.cyan, p: lin(t, t0 + .5, .6) });
  const k = ap(t, t0 + 1.0, .6); A(k, () => { tx('+$21/mo', x + 210, y + 300, { a: 'c', s: 84, b: 1, c: C.amber }); ln(x + 80, y + 316, x + 340, y + 270, lin(t, t0 + 1.2, .4), { c: C.amber, w: 3, alpha: 0 }); tx('FROM JUN 2025', x + 210, y + 348, { a: 'c', s: 32 }); });
  const k2 = ap(t, t0 + 2.2, .6); A(k2, () => { tx('≈ $10 = CAPACITY', x + 210, y + 430, { a: 'c', s: 36, b: 1, c: C.cyan }); ln(x + 70, y + 450, x + 350, y + 450, k2, { c: C.cyan, w: 3 }); });
}
function sec3(t) {
  const [t31, t32, t33, t34, t35, t36, t37, t38, t39, t310] = ['3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10'].map(S);
  bigSheet('SHEET 4 — PRICE', t31, t32 - .1, t);
  // 3.2 PJM 地图 + 3.3 木槌
  A(vis(t, t32 - .1, t34 + .05, .5), () => {
    const sc = .9, ox = 100, oy = 190, p = lin(t, t32 - .1, 1.2);
    drawRings(GEO.us.all, ox, oy, sc, p, { c: C.line, w: 1.5, alpha: .55 });
    const q = lin(t, WT('3.2', 'across') - .2, .9); fillRings(GEO.us.pjm, ox, oy, sc, C.cyan, .2 * q); drawRings(GEO.us.pjm, ox, oy, sc, q, { c: C.cyan, w: 4 });
    A(vis(t, t32 + .5, t33 + .05, .4), () => { tx('PJM', 1100, 330, { s: 130, b: 1, c: C.cyan }); tx('13 STATES + D.C.', 1100, 400, { s: 48, b: 1 }); tx('POWER GRID OPERATOR', 1100, 450, { s: 32 }); });
    A(vis(t, t33 - .1, Infinity, .4), () => {
      tx('CAPACITY AUCTION', 1100, 230, { s: 44, b: 1, c: C.cyan }); tx('EVERY YEAR', 1100, 276, { s: 32 });
      const k = clamp((t - (t33 + .3)) / 1.2), rot = lerp(-.95, 0, k * k * k);
      rc(1190, 640, 320, 44, 1, { w: 3 }); ln(1150, 684, 1550, 684, 1, { w: 3 });
      g.save(); g.translate(1350, 640); g.rotate(rot); rc(-90, -110, 180, 70, 1, { w: 4 }); ln(0, -75, 210, -200, 1, { w: 6 }); g.restore();
      if (k >= 1) { const r = clamp((t - (t33 + 1.5)) / .6); if (r < 1) { ci(1350, 640, 60 + r * 140, 1, { c: C.cyan, w: 3, alpha: 1 - r }); ci(1350, 640, 30 + r * 90, 1, { c: C.cyan, w: 2, alpha: 1 - r }); } }
    });
  });
  // 3.4–3.6 价格柱状图
  const ch = vis(t, t34 - .1, t37 + .05, .5) ; A(ch, () => {
    const base = 710, k = .88;
    ln(300, base, 1620, base, lin(t, t34 - .1, .6), { w: 3 }); ln(300, base, 300, 200, lin(t, t34 - .1, .6), { w: 3 }); tx('$ / MW-DAY', 316, 190, { s: 32 });
    const h1 = 28.92 * k * ap(t, WT('3.4', 'about 29') - .2, .7); rc(560, base - h1, 240, h1, 1, { w: 3 }); fillRc(560, base - h1, 240, h1, C.line, .25);
    tx('$29', 680, base - h1 - 16, { a: 'c', s: 48, b: 1, al: ap(t, WT('3.4', 'about 29') + .2, .3) }); tx('2024/25', 680, base + 46, { a: 'c', s: 32 }); tx('2027/28', 1220, base + 46, { a: 'c', s: 32 });
    const t333 = WT('3.5', '333') - .5, pk = clamp((t - t333) / 1.0), h2 = 333.44 * k * eo(pk);
    rc(1100, base - h2, 240, h2, 1, { w: 3 }); fillRc(1100, base - h2, 240, h2, C.cyan, .3); hatchRc(1100, base - h2, 240, h2, 16, -Math.PI / 4, C.cyan, .6, 1.5);
    const capY = base - 333.44 * k; A(clamp((t - t333) / .6), () => { ln(960, capY, 1620, capY, 1, { c: C.amber, w: 4, dash: [18, 10] }); tx('CAP', 1620, capY - 14, { a: 'r', s: 44, b: 1, c: C.amber }); });
    A(pk > .8 ? 1 : 0, () => tx('$333', 1220, capY - 20, { a: 'c', s: 64, b: 1, c: C.amber }));
    const q = lin(t, t36 + .2, 1.1); if (q > 0) { const top = base - 530 * k; const hh = (333.44 - 0) * k + (530 - 333.44) * k * eo(q); ln(1100, capY, 1100, base - hh, 1, { w: 3, dash: [10, 8] }); ln(1340, capY, 1340, base - hh, 1, { w: 3, dash: [10, 8] }); ln(1100, base - hh, 1340, base - hh, 1, { w: 3, dash: [10, 8] });
      A(q > .8 ? 1 : 0, () => tx('≈$530 (uncapped)', 1100 - 30, top + 6, { a: 'r', s: 36, b: 1 })); }
  });
  // 3.7 目标线 vs 实际线
  A(vis(t, t37 - .1, t38 + .05, .5), () => {
    const base = 700, p = lin(t, t37 - .1, .8); ln(560, base, 1360, base, p, { w: 3 });
    rc(680, base - 420, 220, 420, p, { w: 3, dash: [14, 9] }); tx('TARGET', 790, base + 46, { a: 'c', s: 32 });
    const q = lin(t, t37 + .5, 1.0), ha = 330 * eo(q); rc(1020, base - ha, 220, ha, 1, { w: 3 }); hatchRc(1020, base - ha, 220, ha, 14, -Math.PI / 4, C.cyan, .7, 2); tx('AUCTION RESULT', 1130, base + 46, { a: 'c', s: 32 });
    A(q > .9 ? 1 : 0, () => { ln(700, base - 420, 1240, base - 420, 1, { w: 2, dash: [8, 6] }); dim(1290, base - 420, 1290, base - 330, '', 1, {}); tx('SHORT', 1320, base - 360, { s: 56, b: 1 }); tx('CAPACITY AUCTION VS. RELIABILITY TARGET', 960, 190, { a: 'c', s: 36, b: 1 }); });
  });
  // 3.8 需求台阶
  A(vis(t, t38 - .1, t39 + .05, .5), () => {
    const p = lin(t, t38 - .1, .8); ln(300, 700, 1560, 700, p, { w: 3 }); ln(300, 700, 300, 230, p, { w: 3 }); tx('PJM DEMAND FORECAST', 320, 210, { s: 36, b: 1 }); tx('MW', 270, 250, { a: 'r', s: 32 });
    const q = lin(t, t38 + .3, 1.0); P([[300, 560], [900, 560], [900, 560]], q > 0 ? clamp(q * 1.6) : 0, { w: 5 });
    const s = lin(t, WT('3.8', 'jumped') - .2, .7); const sy = lerp(560, 400, eo(s)); if (s > 0) { P([[900, 560], [900, sy], [1480, sy]], 1, { w: 5, c: C.cyan }); dim(1000, 560, 1000, sy, '', s, {}); dc(940, sy - 110, 90, s); }
    A(s > .9 ? 1 : 0, () => { tx('+5,250 MW', 1030, 500, { s: 64, b: 1, c: C.cyan }); tx('≈ ALL FROM DATA CENTERS', 1030, 580, { s: 36 }); });
  });
  // 3.9 → 房子；3.10 电费单
  A(vis(t, t39 - .1, t310 + .6, .5), () => { const p = lin(t, t39 - .1, 1.0); dc(260, 420, 170, p);
    ln(260, 520, 1700, 520, p, { c: C.cyan, w: 4 }); houses(720, 400, 5, (t - t39) , 240, 130); for (let i = 0; i < 5; i++) ln(720 + i * 240, 465, 720 + i * 240, 520, lin(t, t39 + .5 + i * .12, .3), { c: C.cyan, w: 3 });
    tx('RESIDENTS', 1200, 640, { a: 'c', s: 36, p: lin(t, t39 + .8, .6) }); tx('TECH', 260, 560, { a: 'c', s: 36 }); });
  A(vis(t, t310 + .5, Infinity, .5), () => billDraw(t, t310 + .5, 750, 130));
}
// ---------- 段 4 ----------
function inUS(x, y) { for (const r of GEO.us.all) { let c = false; for (let i = 0, j = r.length - 1; i < r.length; j = i++) { const [xi, yi] = r[i], [xj, yj] = r[j]; if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) c = !c; } if (c) return true; } return false; }
let DOTS = null; function dots(n) { if (DOTS) return DOTS; let s = 7; const R = () => (s = (s * 16807) % 2147483647) / 2147483647; DOTS = []; while (DOTS.length < n) { const x = R() * 1000, y = R() * GEO.us._h; if (inUS(x, y)) DOTS.push([x, y]); } return DOTS; }
function sec4(t) {
  const [t41, t42, t43, t44, t45, t46, t47, t48, t49] = ['4.1', '4.2', '4.3', '4.4', '4.5', '4.6', '4.7', '4.8', '4.9'].map(S);
  bigSheet('SHEET 5 — WORKAROUND', t41, t42 - .1, t);
  // 4.2 三哩岛
  A(vis(t, t42 - .1, S('5.3') + .05, .5), () => {
    const rev = ap(t, WT('4.2', 'now expected') - .6, .8);
    coolingTower(620, 400, 400, lin(t, t42 - .1, 1.2), { dash: 1 }); A(rev, () => { coolingTower(620, 400, 400, 1, {}); for (let i = 0; i < 3; i++) { const k = ((t * .5 + i / 3) % 1); ci(620 + Math.sin(k * 6 + i) * 30, 180 - k * 120, 22 + k * 40, 1, { c: C.cyan, w: 2, alpha: 1 - k }); } });
    tx('THREE MILE ISLAND', 620, 700, { a: 'c', s: 36, b: 1 }); tx('MICROSOFT DEAL', 620, 746, { a: 'c', s: 32, c: C.cyan });
    const x0 = 1000, x1 = 1760, y = 450, q = lin(t, t42 + .8, 1.0); ln(x0, y, x1, y, q, { w: 3 });
    const xa = x0 + 40, xb = x1 - 40; [[2019, xa, 'SHUT DOWN'], [2024, (xa + xb) / 2 + 10, ''], [2027, xb, 'BACK ONLINE']].forEach(([yr, x, lab]) => { ln(x, y - 14, x, y + 14, q, { w: 3 }); tx(String(yr), x, y + 58, { a: 'c', s: 40, b: 1, al: q }); if (lab) tx(lab, x, y - 40, { a: 'c', s: 32, al: q, c: yr == 2027 ? C.cyan : C.line }); });
    P([[xa, y], [xb, y]], rev, { c: C.cyan, w: 6 });
  });
  // 4.3 绕开电网
  A(vis(t, t43 - .1, t44 + .05, .5), () => {
    const p = lin(t, t43 - .1, .8); tower(230, 430, 380, p); dc(900, 430, 250, p); ln(300, 470, 780, 470, p, { c: C.cyan, w: 4 });
    const cutK = lin(t, t43 + .6, .4); A(cutK, () => { rc(480, 440, 90, 60, 1, { w: 1, alpha: 0 }); ln(500, 440, 560, 500, 1, { w: 6 }); ln(560, 440, 500, 500, 1, { w: 6 }); });
    if (cutK > .5) { P([[300, 470], [500, 470]], 1, { c: C.bg, w: 8, alpha: 0 }); }
    const q = lin(t, t43 + 1.0, 1.0); plant(1450, 430, 260, q); ln(1030, 470, 1340, 470, lin(t, t43 + 1.6, .5), { c: C.cyan, w: 4 });
    tx('GRID', 230, 680, { a: 'c', s: 36 }); tx('ON-SITE POWER', 1450, 680, { a: 'c', s: 36, b: 1, c: C.cyan, p: lin(t, t43 + .4, .9) });
  });
  // 4.4 地图 + 59 个点
  A(vis(t, t44 - .1, t45 + .05, .5), () => {
    const sc = 1.1, ox = 110, oy = 140, p = lin(t, t44 - .1, 1.0); drawRings(GEO.us.all, ox, oy, sc, p, { c: C.line, w: 1.5, alpha: .6 });
    const d = dots(59), t0 = t44 + 1.0, n = Math.floor(59 * clamp((t - t0) / 5.0)); for (let i = 0; i < n; i++) { const [x, y] = d[i], age = t - (t0 + i * 5 / 59); ci(ox + x * sc, oy + y * sc, 7 + 8 * Math.max(0, 1 - age * 3), 1, { c: C.cyan, w: 3 }); fillP(arcP(ox + x * sc, oy + y * sc, 5, 0, 6.3, 10), C.cyan, .9); }
    A(vis(t, t44 + .8, Infinity, .4), () => { tx(String(n), 1350, 330, { s: 170, b: 1, c: C.cyan }); tx('PROJECTS', 1350, 380, { s: 44 }); A(clamp((t - WT('4.4', 'about 90') + 1.1) / .2), () => { tx('~' + roll(90, (t - WT('4.4', 'about 90') + 1.0) / 1.0) + ' GW', 1350, 520, { s: 110, b: 1 }); tx('OWN ON-SITE POWER', 1350, 570, { s: 36 }); }); });
  });
  // 4.5 饼图 > 1/4
  A(vis(t, t45 - .1, t46 + .05, .5), () => {
    const cx = 960, cy = 420, r = 260, p = lin(t, t45 - .1, .8); ci(cx, cy, r, p, { w: 4 });
    const q = lin(t, t45 + .4, 1.0), a0 = -Math.PI / 2, a1 = a0 + Math.PI * 2 * .28 * eo(q);
    if (q > 0) { const pts = [[cx, cy], ...arcP(cx, cy, r, a0, a1, 40)]; fillP(pts, C.cyan, .35); hatch(pts, 16, -Math.PI / 4, C.cyan, .8, 2); ln(cx, cy, cx, cy - r, 1, { w: 3 }); ln(cx, cy, cx + r * Math.cos(a1), cy + r * Math.sin(a1), 1, { w: 3 }); }
    A(q > .8 ? 1 : 0, () => { tx('> 1/4', cx + 70, cy - 40, { s: 100, b: 1 }); tx('ON-SITE POWER', 960, 740, { a: 'c', s: 36, b: 1, c: C.cyan }); tx('SHARE OF ALL PLANNED DATA CENTER CAPACITY', 960, 790, { a: 'c', s: 32 }); });
  });
  // 4.6 时间轴点阵
  A(vis(t, t46 - .1, S('5.9') + .05, .5), () => {
    const x0 = 200, u = 405, y = 560, p = lin(t, t46 - .1, .8); ln(x0, y, x0 + 3.75 * u, y, p, { w: 3 });
    [2023, 2024, 2025, 2026].forEach((yr, i) => { ln(x0 + i * u, y - 14, x0 + i * u, y + 14, p, { w: 3 }); tx(String(yr), x0 + i * u, y + 58, { a: 'c', s: 36, al: p }); });
    ln(x0 + 2 * u, 200, x0 + 2 * u, y, p, { w: 2, dash: [10, 8] });
    const pts = []; for (let i = 0; i < 4; i++) pts.push([x0 + (.15 + i * .45) * u, y - 22]);
    let s = 3; const R = () => (s = (s * 16807) % 2147483647) / 2147483647;
    for (let i = 0; i < 46; i++) pts.push([x0 + 2 * u + 14 + (i % 15) * (1.7 * u - 28) / 14, y - 22 - Math.floor(i / 15) * 34 - R() * 6]);
    const t0 = t46 + .5, n = Math.floor(50 * clamp((t - t0) / 3.5)); pts.slice(0, n).forEach(([x, yy]) => fillP(arcP(x, yy, 11, 0, 6.3, 12), C.cyan, .9));
    A(ap(t, WT('4.6', '92 percent') + .3, .6), () => { dim(x0 + 2 * u, 190, x0 + 3.7 * u, 190, '', 1); tx('92%', x0 + 2.85 * u, 130, { a: 'c', s: 90, b: 1, c: C.cyan }); tx('ANNOUNCED SINCE START OF 2025', x0 + 2.85 * u, 250, { a: 'c', s: 36 }); });
  });
  // 4.7 飞机 → 发电机
  A(vis(t, t47 - .1, t48 + .05, .5), () => {
    const dis = ap(t, WT('4.7', 'ordered') + 2.4, 1.6);
    plane(960, 400, 230, lin(t, t47 - .1, 1.4), { bodyA: 1 - .9 * dis });
    A(dis, () => { turbine(960, 400, 150, 1); rc(1170, 345, 130, 110, 1, { w: 3 }); tx('GEN', 1235, 410, { a: 'c', s: 40, b: 1 }); ln(1100, 400, 1170, 400, 1, { w: 4 }); });
    tx('BOOM SUPERSONIC', 960, 190, { a: 'c', s: 40, b: 1, p: lin(t, t47 + 4.8, 1.2) }); tx('BEST KNOWN FOR SUPERSONIC JETS', 960, 232, { a: 'c', s: 32, p: lin(t, t47 + 5.0, 1.2) });
    tx('CRUSOE ORDERED 29 GAS TURBINES', 960, 700, { a: 'c', s: 44, b: 1, c: C.cyan, p: lin(t, WT('4.7', 'ordered') - .2, 1.4) });
  });
  // 4.8 订单划叉 + 印章
  A(vis(t, t48 - .1, t49 + .05, .5), () => {
    const p = lin(t, t48 - .1, .8); rc(560, 170, 560, 440, p, { w: 4 }); tx('PURCHASE ORDER', 840, 230, { a: 'c', s: 40, b: 1, p }); tx('CRUSOE ← BOOM', 600, 310, { s: 36, p }); tx('29 × GAS TURBINE', 600, 370, { s: 36, p }); for (let i = 0; i < 3; i++) ln(600, 430 + i * 36, 1060 - i * 80, 430 + i * 36, p, { w: 2, alpha: .5 });
    const x = lin(t, WT('4.8', 'walked') - .3, .7); ln(580, 190, 1100, 590, x, { w: 9 }); ln(1100, 190, 580, 590, clamp(x * 2 - 1), { w: 9 });
    stamp('CANCELLED', 840, 600, t, WT('4.8', 'walked') + .5, { s: 56 });
    A(ap(t, WT('4.8', 'turned') - .2, .6), () => { arrow(1160, 390, 1390, 390, 1, { w: 5, c: C.cyan }); rc(1400, 300, 400, 180, 1, { w: 4, c: C.cyan }); tx('GE VERNOVA', 1600, 380, { a: 'c', s: 44, b: 1 }); tx('ESTABLISHED', 1600, 424, { a: 'c', s: 32 }); tx('SUPPLIERS', 1600, 460, { a: 'c', s: 32 }); });
  });
  // 4.9 沙漏
  A(vis(t, t49 - .1, Infinity, .5), () => { hourglass(960, 430, 500, lin(t, t49 - .1, .9), lerp(.9, .06, lin(t, t49 + .6, D('4.9') - .6)));
    tx('TIME', 960, 750, { a: 'c', s: 44, b: 1, p: lin(t, t49 + .5, .6) }); });
}
