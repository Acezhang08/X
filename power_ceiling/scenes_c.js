// ===== 段 5–7 + 总帧 =====
function sec5(t) {
  const [t51, t52, t53, t54, t55, t56] = ['5.1', '5.2', '5.3', '5.4', '5.5', '5.6'].map(S);
  // 5.1 背面亚洲地图
  A(vis(t, t51 - .3, t52 + .05, .5), () => { const sc = .9, ox = 480, oy = 130, p = lin(t, t51 - .1, 1.2);
    drawRings(GEO.asia.all, ox, oy, sc, p, { c: C.line, w: 1.6, alpha: .6 }); fillRings(GEO.asia.china, ox, oy, sc, C.cyan, .25 * p, 14); drawRings(GEO.asia.china, ox, oy, sc, p, { c: C.cyan, w: 4 }); fillRc(860, 345, 280, 76, C.bg, .8 * p); tx('CHINA', 1000, 400, { a: 'c', s: 56, b: 1, c: C.cyan, al: p }); });
  // 5.2 发电量对比
  A(vis(t, t52 - .1, t53 + .05, .5), () => { const base = 720, k = lin(t, t52 - .1, .8); ln(420, base, 1500, base, k, { w: 3 }); tx('ELECTRICITY GENERATED', 420, 180, { s: 40, b: 1 });
    const h1 = 200 * ap(t, t52 + .2, .8), h2 = 440 * ap(t, t52 + .5, 1.0); rc(620, base - h1, 200, h1, 1, { w: 3 }); hatchRc(620, base - h1, 200, h1, 16, -Math.PI / 4, C.line, .4, 1.5); rc(1020, base - h2, 200, h2, 1, { w: 3 }); hatchRc(1020, base - h2, 200, h2, 16, -Math.PI / 4, C.cyan, .6, 1.5);
    tx('UNITED STATES', 720, base + 46, { a: 'c', s: 32 }); tx('CHINA', 1120, base + 46, { a: 'c', s: 32 });
    A(ap(t, t52 + 1.8, .5), () => { ln(820, base - h1, 1020, base - h1, 1, { w: 2, dash: [8, 6] }); dim(900, base - h1, 900, base - h2, '', 1); tx('> 2×', 880, base - 320, { a: 'r', s: 80, b: 1, c: C.cyan }); }); });
  // 5.3 风光
  A(vis(t, t53 - .1, t54 + .05, .5), () => { const gy = 700; ln(100, gy, 1820, gy, lin(t, t53 - .1, .8), { w: 3 });
    for (let i = 0; i < 6; i++) windT(250 + i * 190, gy - 160, 320, t * 1.3 + i, lin(t, t53 + i * .25, .6));
    for (let i = 0; i < 5; i++) solar(1450 + (i % 3) * 140, gy - 40 - Math.floor(i / 3) * 90, 120, lin(t, t53 + 1 + i * .15, .6));
    const v = roll(430, (t - WT('5.3', '430') + 1.8) / 1.8); tx(v + '+ GW', 960, 190, { a: 'c', s: 140, b: 1, c: C.cyan }); tx('WIND + SOLAR ADDED IN 2025 ALONE', 960, 240, { a: 'c', s: 36, b: 1 }); });
  // 5.4 方块
  A(vis(t, t54 - .1, t55 + .05, .5), () => { const y = 380, q = lin(t, t54 - .1, .6);
    rc(260, y, 110, 110, q, { w: 4 }); hatchRc(260, y, 110, 110, 14, -Math.PI / 4, C.line, .5, 1.5); tx('US', 315, y + 170, { a: 'c', s: 48, b: 1, al: q }); tx('×1', 315, y + 220, { a: 'c', s: 44, al: q });
    const n = clamp((t - WT('5.4', 'six times') + 1.2) / 3.0) * 6.4;
    for (let i = 0; i < 7; i++) { const f = clamp(n - i); if (f <= 0) continue; const w = 110 * f; rc(520 + i * 170, y, w, 110, 1, { w: 4, c: C.cyan }); fillRc(520 + i * 170, y, w, 110, C.cyan, .3); hatchRc(520 + i * 170, y, w, 110, 14, -Math.PI / 4, C.cyan, .7, 1.5); }
    A(n > 6 ? 1 : 0, () => { tx('CHINA', 1000, y + 170, { a: 'c', s: 48, b: 1, c: C.cyan }); tx('×6+', 1000, y + 220, { a: 'c', s: 44 }); tx('NEW GENERATION CAPACITY, NEXT 5 YEARS', 960, 250, { a: 'c', s: 36, b: 1 }); }); });
  // 5.5 分屏
  A(vis(t, t55 - .1, t56 + .05, .5), () => { const p = lin(t, t55 - .1, .8); ln(960, 100, 960, 590, p, { w: 3, dash: [12, 8] });
    tx('UNITED STATES', 510, 140, { a: 'c', s: 44, b: 1, p }); tx('CHINA', 1410, 140, { a: 'c', s: 44, b: 1, c: C.cyan, p });
    for (let r = 0; r < 2; r++) for (let c = 0; c < 3; c++) { const x = 270 + c * 240, y = 270 + r * 200; chip(x, y, 64, lin(t, t55 + .2 + (r * 3 + c) * .1, .5)); plug(x + 56, y + 90, 34, lin(t, t55 + .5, .5)); if (p >= 1) { ln(x, y + 38, x, y + 90, 1, { w: 2 }); } }
    for (let r = 0; r < 4; r++) ln(1040, 230 + r * 90, 1840, 230 + r * 90, lin(t, t55 + .3 + r * .1, .8), { c: C.cyan, w: 4 });
    for (let r = 0; r < 2; r++) for (let c = 0; c < 3; c++) { const x = 1150 + c * 240, y = 270 + r * 200; chip(x, y, 64, lin(t, t55 + .6, .6), { dash: [8, 6] }); }
    const k = ap(t, t55 + .3, .6); quote('…the US has the chips and is short on power, while China has the power and is short on chips.', 'IMD Business School, via Al Jazeera, May 2026', 110, 610, 1700, t, t55 + .6, { s: 32 }); });
  // 5.6 两张图纸、两条不同高度的虚线
  A(vis(t, t56 - .1, Infinity, .5), () => { const p = lin(t, t56 - .1, .9);
    rc(120, 150, 780, 560, p, { w: 3 }); rc(1020, 150, 780, 560, p, { w: 3 });
    dc(510, 600, 170, p); dc(1410, 600, 170, p);
    tx('UNITED STATES', 510, 200, { a: 'c', s: 36, b: 1, p }); tx('CHINA', 1410, 200, { a: 'c', s: 36, b: 1, p });
    const q = lin(t, WT('5.6', 'different ceiling') - 1.2, 1.0);
    ln(160, 400, 860, 400, q, { c: C.amber, w: 5, dash: [20, 12] }); ln(1060, 270, 1760, 270, q, { c: C.amber, w: 5, dash: [20, 12] });
    A(q > .8 ? 1 : 0, () => { dim(260, 400, 260, 515, '', 1, { c: C.amber }); dim(1160, 270, 1160, 515, '', 1, { c: C.amber }); tx('POWER', 510, 465, { a: 'c', s: 44, b: 1, c: C.amber }); tx('CHIPS', 1410, 335, { a: 'c', s: 44, b: 1, c: C.amber }); }); });
}
function sec6(t) {
  const [t61, t62, t63, t64, t65] = ['6.1', '6.2', '6.3', '6.4', '6.5'].map(S);
  // 6.2 绕过天花板
  A(vis(t, t62 - .1, t63 + .05, .5), () => {
    const p = lin(t, t62 - .1, .6); ln(560, 280, 1240, 280, p, { c: C.amber, w: 6, dash: [22, 14] }); tx('CEILING', 900, 240, { a: 'c', s: 44, b: 1, c: C.amber, al: p });
    const path = [...Array.from({ length: 31 }, (_, i) => { const k = i / 30; return [lerp(200, 700, k), lerp(740, 330, k) - Math.sin(k * Math.PI) * 0 + (1 - k) * (k) * -40]; }), [900, 322], [1100, 322], [1240, 324], ...arcP(1300, 280, 60, Math.PI / 2, -Math.PI / 4, 12), [1420, 160], [1500, 110]];
    const q = lin(t, t62 + .5, 3.2); P(path, eio(q), { c: C.cyan, w: 7 });
    if (q > .9) arrowHead(1500, 110, Math.atan2(-50, 80), 26, { c: C.cyan, w: 6 }); tx('AI', 200, 790, { s: 48, b: 1, c: C.cyan });
  });
  // 6.3 三行工程注释
  A(vis(t, t63 - .1, t64 + .05, .5), () => { tx('POWER WILL DECIDE THREE THINGS', 960, 140, { a: 'c', s: 44, b: 1, p: lin(t, t63, 1.2) }); const rows = [['1', 'SPEED', 'HOW FAST AI GROWS', 'how fast AI grows'], ['2', 'LOCATION', 'WHERE IT GETS BUILT', 'where it gets built'], ['3', 'WINNER', 'WHO WINS', 'who wins']];
    const ts = [WT('6.3', 'how fast'), WT('6.3', 'where'), WT('6.3', 'who wins')];
    rows.forEach(([n, a, b, c], i) => { const p = lin(t, ts[i] - 1.1, .8), y = 260 + i * 190; ci(420, y, 54, p, { w: 4 }); tx(n, 420, y + 18, { a: 'c', s: 64, b: 1, al: p }); tx(a, 540, y + 14, { s: 72, b: 1, p }); ln(540, y + 40, 1300, y + 40, p, { w: 2 }); tx(c, 1330, y + 14, { s: 36, f: 'h', c: C.cyan, p: lin(t, ts[i] + .3, .8) }); }); });
  // 6.4 插头插入 + 电流
  A(vis(t, t64 - .1, t65 + .05, .5), () => { const k = eio(lin(t, WT('6.4', 'locked') - .4, 1.2)); const px = lerp(560, 780, k);
    ln(120, 430, px - 100, 430, 1, { w: 4 }); plug(px, 430, 200, 1); socket(1010, 430, 230, 1); ln(1120, 430, 1760, 430, 1, { w: 4 });
    if (k >= 1) { const off = -t * 140; ln(120, 430, 1760, 430, 1, { c: C.cyan, w: 6, dash: [26, 22], off }); }
    A(ap(t, t64 + 1.2, .6), () => { tx('THE BEST MODELS', 330, 640, { a: 'c', s: 36 }); tx('POWER LOCKED IN EARLY', 1300, 640, { a: 'c', s: 36, b: 1, c: C.cyan }); }); });
  // 6.5 天平
  A(vis(t, t65 - .1, S('7.6') + .05, .5), () => { const p = lin(t, t65 - .1, .9), ang = .22 * eio(lin(t, WT('6.5', 'may be worth') - .4, 1.4)), cx = 960, by = 250, L = 330;
    ln(cx, by, cx, 720, p, { w: 5 }); ln(cx - 140, 720, cx + 140, 720, p, { w: 5 }); ci(cx, by, 16, p, { w: 4 });
    const lx = cx - L * Math.cos(ang), ly = by + L * Math.sin(ang), rx = cx + L * Math.cos(ang), ry = by - L * Math.sin(ang);
    ln(lx, ly, rx, ry, p, { w: 6 });
    for (const [x, y] of [[lx, ly], [rx, ry]]) { ln(x, y, x - 90, y + 150, p, { w: 2 }); ln(x, y, x + 90, y + 150, p, { w: 2 }); P(arcP(x, y + 150, 100, 0, Math.PI, 20), p, { w: 4 }); }
    socket(lx, ly + 90, 120, p); chip(rx, ry + 90, 66, p);
    A(p, () => { tx('GUARANTEED GRID', lx, ly + 320, { a: 'c', s: 36, b: 1, c: C.cyan }); tx('CONNECTION', lx, ly + 362, { a: 'c', s: 36, b: 1, c: C.cyan }); tx('CHIPS', rx, ry + 320, { a: 'c', s: 36, b: 1 }); }); });
}
function thumb(i, x, y, w, h, p) { rc(x, y, w, h, p, { w: 3 }); const cx = x + w / 2, cy = y + h / 2 + 8;
  [() => chip(cx, cy, 90, p), () => tower(cx, cy, 190, p), () => bill(cx - 70, cy - 90, 140, 170, p), () => plant(cx, cy, 170, p), () => dc(cx, cy, 130, p), () => { ln(cx - 60, cy + 70, cx + 60, cy + 70, p, { w: 3 }); P([[cx, cy - 70], [cx, cy + 70]], p, { w: 3 }); ln(cx - 70, cy - 40, cx + 70, cy - 40, p, { w: 3 }); }][i](); }
function sec7(t) {
  const [t71, t72, t73, t74] = ['7.1', '7.2', '7.3', '7.4'].map(S);
  A(vis(t, t71 - .3, t72 + .05, .4), () => { const z = lerp(3.4, 1, eio(lin(t, t71 - .35, 1.6))); g.save(); g.translate(960, 410); g.scale(z, z); g.translate(-960, -410);
    for (let i = 0; i < 6; i++) thumb(i, 140 + (i % 3) * 570, 110 + Math.floor(i / 3) * 340, 520, 300, 1); g.restore();
    A(lin(t, t71 + .8, .6), () => { tx('ALL SHEETS · ONE DRAWING', 960, 790, { a: 'c', s: 32 }); }); });
  A(vis(t, t72 - .1, t73 + .05, .5), () => { billDraw(t, t72 - .1, 750, 130); houses(520, 740, 5, t - t72, 220, 90); });
  A(vis(t, t73 - .1, t74 + .05, .5), () => { shelves(t, t73 - .1, 90); tx('THE CHIPS WERE THERE.', 1100, 330, { s: 48, b: 1, p: lin(t, t73 + 1.2, 1.4) }); tx('THE POWER WASN’T.', 1100, 410, { s: 48, b: 1, c: C.cyan, p: lin(t, WT('7.3', 'The power') - .2, 1.2) }); });
  A(vis(t, t74 - .1, Infinity, .5), () => { const p = lin(t, t74 - .1, .8); tx('WHICH RUNS OUT FIRST?', 960, 220, { a: 'c', s: 56, b: 1, p });
    rc(340, 300, 520, 240, p, { w: 4 }); rc(1060, 300, 520, 240, p, { w: 4, c: C.cyan }); tx('CHIPS', 600, 440, { a: 'c', s: 90, b: 1, p }); tx('POWER', 1320, 440, { a: 'c', s: 90, b: 1, c: C.cyan, p });
    if (p >= 1 && Math.floor(t * 2) % 2 == 0) ln(960, 340, 960, 500, 1, { w: 5 });
    tx('TELL ME IN THE COMMENTS', 960, 640, { a: 'c', s: 40, f: 'h' }); });
}
function bg(a = 1) {
  g.fillStyle = C.bg; g.fillRect(0, 0, W, H);
  g.save(); g.globalAlpha = .05 * a; g.strokeStyle = '#fff'; g.lineWidth = 1; g.beginPath(); for (let x = 0; x <= W; x += 24) { g.moveTo(x, 0); g.lineTo(x, H); } for (let y = 0; y <= H; y += 24) { g.moveTo(0, y); g.lineTo(W, y); } g.stroke();
  g.globalAlpha = .08 * a; g.lineWidth = 1.5; g.beginPath(); for (let x = 0; x <= W; x += 120) { g.moveTo(x, 0); g.lineTo(x, H); } for (let y = 0; y <= H; y += 120) { g.moveTo(0, y); g.lineTo(W, y); } g.stroke(); g.restore();
}
function titleBlock(name, t) {
  const x = 1380, y = 805, w = 480, h = 100; g.fillStyle = 'rgba(14,42,71,0.9)'; g.fillRect(x, y, w, h); rc(x, y, w, h, 1, { w: 3 }); ln(x, y + 50, x + w, y + 50, 1, { w: 2 });
  tx('DWG-08 / POWER CEILING', x + 16, y + 36, { s: 32, b: 1 }); tx(name, x + 16, y + 86, { s: 32, c: C.cyan });
}
function secIndex(t) { let k = 0; for (let i = 1; i < SECS.length; i++) if (t >= S(TL.first[i]) - .9) k = i; return k; }
function scene(k, t) { SECS[k][2](t); }
function frame(t) {
  g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.fillStyle = '#000'; g.fillRect(0, 0, W, H);
  const intro = S('0.1') ;
  if (t < 1.4) {
    if (t > .15) { const p = lin(t, .15, .6); ln(0, 540, W * eo(p), 540, 1, { w: 4 }); }
    if (t > .8) { const r = eo(lin(t, .8, .6)); g.save(); g.beginPath(); g.rect(0, 540 - 540 * r, W, 1080 * r); g.clip(); bg(r); g.restore(); }
    if (t > 1.0) { g.save(); g.globalAlpha = lin(t, 1.0, .4); titleBlock(SECS[0][1], t); g.restore(); }
    return;
  }
  const k = secIndex(t), start = S(TL.first[k]);
  const wp = k > 0 ? (t - (start - .9)) / .8 : 2;
  const drawFull = (kk) => { bg(); scene(kk, t); };
  if (k > 0 && wp < 1) {
    drawFull(k - 1);
    if (SECS[k][0] === '6') { const q = clamp(wp); if (q < .5) { g.save(); g.translate(960, 0); g.scale(Math.max(.001, Math.cos(q * Math.PI)), 1); g.translate(-960, 0); drawFull(k - 1); g.restore(); g.fillStyle = '#000'; } else { g.fillStyle = '#000'; g.fillRect(0, 0, W, H); g.save(); g.translate(960, 0); g.scale(Math.max(.001, -Math.cos(q * Math.PI)), 1); g.translate(-960, 0); drawFull(k); g.restore(); } }
    else { const wx = W * eio(clamp(wp)); g.save(); g.beginPath(); g.rect(0, 0, wx, H); g.clip(); drawFull(k); g.restore();
      const gr = g.createLinearGradient(wx, 0, wx + 60, 0); gr.addColorStop(0, 'rgba(0,0,0,.45)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(wx, 0, 60, H); ln(wx, 0, wx, H, 1, { w: 4 }); ln(wx + 10, 0, wx + 10, H, 1, { w: 1.5, c: C.cyan }); }
  } else drawFull(k);
  const nm = (t >= S('8.4') - .1) ? 'END OF DRAWING' : SECS[(k > 0 && wp < 1 && wp < .55) ? k - 1 : k][1]; titleBlock(nm, t);
}
