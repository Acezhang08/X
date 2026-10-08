// ===== 线稿图标：(cx, cy) 为中心，s 为高度，p 为描线进度 =====
function chip(cx, cy, s, p = 1, o = {}) {
  const h = s / 2, c = o.c || C.line;
  rc(cx - h, cy - h, s, s, p, { c, w: 3, dash: o.dash });
  rc(cx - h * .5, cy - h * .5, h, h, p, { c, w: 2, dash: o.dash });
  for (let i = 0; i < 4; i++) { const k = -h + s * (i + .5) / 4;
    ln(cx + k, cy - h, cx + k, cy - h - s * .16, p, { c, w: 2 }); ln(cx + k, cy + h, cx + k, cy + h + s * .16, p, { c, w: 2 });
    ln(cx - h, cy + k, cx - h - s * .16, cy + k, p, { c, w: 2 }); ln(cx + h, cy + k, cx + h + s * .16, cy + k, p, { c, w: 2 }); }
}
function plug(cx, cy, s, p = 1, o = {}) { // 朝右的插头，cx 是插头体中心，插针向右
  const c = o.c || C.line, h = s / 2, f = o.flip ? -1 : 1;
  const X = v => cx + v * f;
  P([[X(-h), cy - h * .7], [X(h * .4), cy - h * .7], [X(h * .4), cy + h * .7], [X(-h), cy + h * .7], [X(-h), cy - h * .7]], p, { c, w: 3 });
  ln(X(h * .4), cy - h * .35, X(h * 1.1), cy - h * .35, p, { c, w: 4 }); ln(X(h * .4), cy + h * .35, X(h * 1.1), cy + h * .35, p, { c, w: 4 });
  ln(X(-h), cy, X(-h * 2.2), cy, p, { c, w: 3 });
}
function socket(cx, cy, s, p = 1, o = {}) {
  const c = o.c || C.line, h = s / 2;
  rc(cx - h * .6, cy - h * .9, h * 1.2, h * 1.8, p, { c, w: 3 }); ci(cx, cy, h * .55, p, { c, w: 2 });
  ln(cx - h * .18, cy - h * .2, cx - h * .18, cy + h * .2, p, { c, w: 4 }); ln(cx + h * .18, cy - h * .2, cx + h * .18, cy + h * .2, p, { c, w: 4 });
}
function tower(cx, cy, s, p = 1, o = {}) {
  const c = o.c || C.line, t = cy - s / 2, b = cy + s / 2, w = s * .22;
  const pts = [[cx - w, b], [cx - w * .25, t + s * .1], [cx, t], [cx + w * .25, t + s * .1], [cx + w, b]];
  P(pts, p, { c, w: 3 });
  for (let i = 1; i <= 4; i++) { const k = i / 5, y = lerp(b, t + s * .1, k), hw = lerp(w, w * .25, k);
    ln(cx - hw, y, cx + hw, y, p, { c, w: 2 });
    const k2 = (i + 1) / 5; if (i < 4) { const y2 = lerp(b, t + s * .1, k2), hw2 = lerp(w, w * .25, k2); ln(cx - hw, y, cx + hw2, y2, p, { c, w: 1.5 }); ln(cx + hw, y, cx - hw2, y2, p, { c, w: 1.5 }); } }
  ln(cx - s * .3, t + s * .22, cx + s * .3, t + s * .22, p, { c, w: 3 }); ln(cx - s * .22, t + s * .08, cx + s * .22, t + s * .08, p, { c, w: 3 });
}
function trafo(cx, cy, s, p = 1, o = {}) {
  const c = o.c || C.line, w = s * 1.1, h = s * .7, x = cx - w / 2, y = cy - h / 2 + s * .08;
  rc(x, y, w, h, p, { c, w: 3 });
  for (let i = 1; i < 7; i++) ln(x + w * i / 7, y + 8, x + w * i / 7, y + h - 8, p, { c, w: 2 });
  for (let i = 0; i < 3; i++) { const bx = x + w * (.2 + .3 * i); P([[bx - 10, y], [bx - 10, y - s * .22], [bx + 10, y - s * .22], [bx + 10, y]], p, { c, w: 3 }); ln(bx, y - s * .22, bx, y - s * .36, p, { c, w: 3 }); }
}
function plant(cx, cy, s, p = 1, o = {}) {
  const c = o.c || C.line, b = cy + s / 2;
  rc(cx - s * .55, b - s * .45, s * .7, s * .45, p, { c, w: 3 });
  P([[cx + s * .2, b], [cx + s * .28, b - s * .85], [cx + s * .5, b - s * .85], [cx + s * .58, b]], p, { c, w: 3 });
  P([[cx + s * .28, b - s * .6], [cx + s * .54, b - s * .6]], p, { c, w: 2 });
  for (let i = 0; i < 3; i++) ln(cx - s * .45 + i * s * .2, b - s * .35, cx - s * .45 + i * s * .2, b - s * .1, p, { c, w: 2 });
}
function dc(cx, cy, s, p = 1, o = {}) { // 数据中心：楼 + 机架
  const c = o.c || C.line, w = s * 1.2, x = cx - w / 2, y = cy - s / 2;
  const d = o.dash ? { dash: [10, 8] } : {};
  rc(x, y, w, s, p, { c, w: 3, ...d });
  for (let i = 0; i < 3; i++) for (let j = 0; j < 4; j++) rc(x + w * (.1 + j * .22), y + s * (.12 + i * .28), w * .17, s * .2, p, { c, w: 1.5, ...d });
  if (p >= 1 && !o.dash && o.led) for (let j = 0; j < 4; j++) ci(x + w * (.185 + j * .22), y + s * .22, 3, 1, { c: C.cyan, w: 3 });
}
function house(cx, cy, s, p = 1, o = {}) {
  const c = o.c || C.line, w = s * .9, x = cx - w / 2, y = cy - s / 2;
  P([[x, y + s * .45], [cx, y], [x + w, y + s * .45], [x + w, y + s], [x, y + s], [x, y + s * .45]], p, { c, w: 3 });
  rc(cx - w * .12, y + s * .6, w * .24, s * .4, p, { c, w: 2 });
}
function turbine(cx, cy, s, p = 1, o = {}) { // 燃气轮机剖面：压气机→燃烧室→涡轮
  const c = o.c || C.line, L = s * 2.2, x = cx - L / 2;
  P([[x, cy - s * .18], [x + L * .38, cy - s * .3], [x + L * .38, cy + s * .3], [x, cy + s * .18], [x, cy - s * .18]], p, { c, w: 3 });
  rc(x + L * .38, cy - s * .3, L * .22, s * .6, p, { c, w: 3 });
  P([[x + L * .6, cy - s * .3], [x + L * .98, cy - s * .2], [x + L * .98, cy + s * .2], [x + L * .6, cy + s * .3]], p, { c, w: 3 });
  ln(x - s * .3, cy, x + L * 1.12, cy, p, { c, w: 4 });
  for (let i = 0; i < 7; i++) { const bx = x + L * (.04 + i * .05), hh = lerp(s * .16, s * .26, i / 6); ln(bx, cy - hh * .3, bx, cy - hh, p, { c, w: 2 }); ln(bx, cy + hh * .3, bx, cy + hh, p, { c, w: 2 }); }
  for (let i = 0; i < 3; i++) { const bx = x + L * (.66 + i * .1), hh = lerp(s * .2, s * .27, i / 2); ln(bx, cy - hh * .3, bx, cy - hh, p, { c, w: 2 }); ln(bx, cy + hh * .3, bx, cy + hh, p, { c, w: 2 }); }
  for (let i = 0; i < 5; i++) ln(x + L * .41 + i * L * .035, cy - s * .25, x + L * .41 + i * L * .035, cy + s * .25, p, { c: o.fire || c, w: 1.5 });
}
function hourglass(cx, cy, s, p = 1, sand = .5, o = {}) {
  const c = o.c || C.line, h = s / 2, w = s * .42;
  P([[cx - w, cy - h], [cx + w, cy - h], [cx + w * .08, cy], [cx + w, cy + h], [cx - w, cy + h], [cx - w * .08, cy], [cx - w, cy - h]], p, { c, w: 3 });
  ln(cx - w * 1.2, cy - h, cx + w * 1.2, cy - h, p, { c, w: 4 }); ln(cx - w * 1.2, cy + h, cx + w * 1.2, cy + h, p, { c, w: 4 });
  if (p >= 1) {
    const top = clamp(1 - sand), bot = clamp(sand);
    fillP([[cx - w * (1 - top), cy - h + h * top], [cx + w * (1 - top), cy - h + h * top], [cx + w * .08, cy - 2], [cx - w * .08, cy - 2]], C.cyan, .45);
    if (top < 1) fillP([[cx - w * .08, cy + h - h * bot * .9], [cx + w * .08, cy + h - h * bot * .9], [cx + w * bot, cy + h - 3], [cx - w * bot, cy + h - 3]], C.cyan, .45);
    if (top < 1 && bot < 1) ln(cx, cy, cx, cy + h * (1 - bot * .9), 1, { c: C.cyan, w: 2 });
  }
}
function coolingTower(cx, cy, s, p = 1, o = {}) {
  const c = o.c || C.line, h = s, b = cy + h / 2, t = cy - h / 2, pts = [];
  for (let i = 0; i <= 20; i++) { const k = i / 20, y = lerp(t, b, k), r = s * (.3 + .2 * Math.pow(Math.abs(k - .6) * 1.6, 2)); pts.push([cx - r, y]); }
  const pts2 = pts.map((q, i) => [cx + (cx - q[0]), q[1]]);
  const d = o.dash ? { dash: [12, 9] } : {};
  P(pts, p, { c, w: 3, ...d }); P(pts2, p, { c, w: 3, ...d });
  ln(pts[0][0], t, pts2[0][0], t, p, { c, w: 3, ...d }); ln(pts[20][0], b, pts2[20][0], b, p, { c, w: 3, ...d });
  for (let i = 1; i < 4; i++) ln(pts[i * 5][0] + 8, pts[i * 5][1], pts2[i * 5][0] - 8, pts2[i * 5][1], p, { c, w: 1.2, ...d, alpha: .6 });
}
function plane(cx, cy, s, p = 1, o = {}) { // 超音速客机侧视线稿
  const c = o.c || C.line, L = s * 2.6, x = cx - L / 2;
  const body = [[x, cy], [x + L * .22, cy - s * .08], [x + L * .8, cy - s * .08], [x + L * .98, cy - s * .02], [x + L, cy], [x + L * .98, cy + s * .02], [x + L * .8, cy + s * .08], [x + L * .22, cy + s * .08], [x, cy]];
  P(body, p, { c, w: 3, alpha: o.bodyA ?? 1 });
  P([[x + L * .45, cy - s * .08], [x + L * .78, cy - s * .55], [x + L * .84, cy - s * .55], [x + L * .72, cy - s * .08]], p, { c, w: 3, alpha: o.bodyA ?? 1 });
  P([[x + L * .86, cy - s * .08], [x + L * .95, cy - s * .3], [x + L * .99, cy - s * .3], [x + L * .98, cy - s * .08]], p, { c, w: 3, alpha: o.bodyA ?? 1 });
  for (let i = 0; i < 6; i++) ci(x + L * (.27 + i * .045), cy - s * .02, 5, p, { c, w: 1.5, alpha: o.bodyA ?? 1 });
  for (const ex of [.55, .66]) { rc(x + L * ex, cy + s * .08, L * .09, s * .16, p, { c: o.engC || C.cyan, w: 3 }); }
}
function windT(cx, cy, s, rot, p = 1, o = {}) {
  const c = o.c || C.line;
  ln(cx, cy + s / 2, cx, cy - s * .3, p, { c, w: 3 });
  for (let i = 0; i < 3; i++) { const a = rot + i * 2.094; ln(cx, cy - s * .3, cx + Math.cos(a) * s * .45, cy - s * .3 + Math.sin(a) * s * .45, p, { c, w: 3 }); }
}
function solar(cx, cy, s, p = 1, o = {}) {
  const c = o.c || C.cyan, w = s, h = s * .5;
  P([[cx - w / 2 + 10, cy - h / 2], [cx + w / 2 + 10, cy - h / 2], [cx + w / 2 - 10, cy + h / 2], [cx - w / 2 - 10, cy + h / 2], [cx - w / 2 + 10, cy - h / 2]], p, { c, w: 2.5 });
  for (let i = 1; i < 4; i++) { const k = i / 4; ln(lerp(cx - w / 2 + 10, cx + w / 2 + 10, k), cy - h / 2, lerp(cx - w / 2 - 10, cx + w / 2 - 10, k), cy + h / 2, p, { c, w: 1.5 }); }
  ln(cx - w * .2, cy + h / 2, cx - w * .2, cy + h / 2 + s * .22, p, { c, w: 2.5 });
}
function clock(cx, cy, r, t, p = 1, o = {}) {
  const c = o.c || C.line; ci(cx, cy, r, p, { c, w: 3 });
  if (p >= 1) { ln(cx, cy, cx + Math.sin(t * 1.2) * r * .7, cy - Math.cos(t * 1.2) * r * .7, 1, { c, w: 3 }); ln(cx, cy, cx + Math.sin(t * .1) * r * .5, cy - Math.cos(t * .1) * r * .5, 1, { c, w: 3 }); }
}
function person(cx, cy, s, p = 1, o = {}) { // 白色线条剪影，不画脸
  const c = o.c || C.line, h = s;
  ci(cx, cy - h * .38, h * .1, p, { c, w: 3 });
  P([[cx - h * .17, cy - h * .22], [cx + h * .17, cy - h * .22], [cx + h * .2, cy + h * .12], [cx + h * .08, cy + h * .12], [cx + h * .07, cy + h * .5], [cx - h * .07, cy + h * .5], [cx - h * .08, cy + h * .12], [cx - h * .2, cy + h * .12], [cx - h * .17, cy - h * .22]], p, { c, w: 3 });
}
function bill(x, y, w, h, p = 1, o = {}) {
  const c = o.c || C.line;
  P([[x, y], [x + w, y], [x + w, y + h], ...Array.from({ length: 7 }, (_, i) => [x + w - (i + 1) * w / 7, y + h + (i % 2 ? 0 : 16)]), [x, y + h], [x, y]], p, { c, w: 3 });
  if (p >= 1) for (let i = 0; i < 2; i++) ln(x + 36, y + 140 + i * 36, x + w - 36 - (i % 2) * 90, y + 140 + i * 36, 1, { c, w: 2, alpha: .5 });
}
