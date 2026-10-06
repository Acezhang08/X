import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

// ---------- 时间轴（来自配音） ----------
const W = 1920, H = 1080, FPS = 30;
const TM = await (await fetch('/grokbot/build/timings.json')).json();
const DUR = TM.duration, LN = TM.lines;
const S = (n) => LN[n - 1].start, E = (n) => LN[n - 1].end;
const at = (n, f) => S(n) + f * (E(n) - S(n)); // 第 n 句的 f 处
const B = (n) => (n === 1 ? 0 : S(n) - 0.25); // 画面节拍略早于人声

const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const ramp = (t, a, b) => clamp((t - a) / (b - a));
const ease = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const eOut = (x) => 1 - Math.pow(1 - x, 3);
const eIn = (x) => x * x * x;
const er = (t, a, b) => ease(ramp(t, a, b));
const backOut = (x) => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const pop = (t, a, d = 0.45) => backOut(ramp(t, a, a + d));
const lerp = (a, b, x) => a + (b - a) * x;
const win = (t, a, b, fi = 0.3, fo = 0.3) => Math.min(ramp(t, a, a + fi), 1 - ramp(t, b - fo, b));

// ---------- 配色 ----------
const C = {
  floor: 0xf2f3f2, wall: 0xeef0ef, side: 0xdde1df, inner: 0xe7eae8, desk: 0xfbfbfb, leg: 0xc5cbc8,
  dark: 0x27302d, bot: 0xf8f9f8, shade: 0xd3d9d6, accent: 0x22b573, line: 0xb8c3be,
};
const ACC = '#22b573', INK = '#1d2421', GREY = '#6c7672';
const DAY_BG = new THREE.Color(0xe8eceb), NIGHT_BG = new THREE.Color(0x2b3440);

await Promise.all(['500', '600', '700', '800'].map((w) => document.fonts.load(`${w} 40px Inter`)));

// ---------- 渲染器 ----------
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(W, H, false);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.NeutralToneMapping;
renderer.toneMappingExposure = 1.0;
renderer.outputColorSpace = THREE.SRGBColorSpace;
const out = document.createElement('canvas');
out.width = W; out.height = H;
document.body.appendChild(out);
const ctx = out.getContext('2d');

const scene = new THREE.Scene();
scene.background = new THREE.Color();
const camera = new THREE.PerspectiveCamera(30, W / H, 0.1, 300);

const hemi = new THREE.HemisphereLight(0xffffff, 0xd2d8d5, 2.0);
scene.add(hemi);
const sun = new THREE.DirectionalLight(0xf3f7ff, 2.3);
sun.position.set(-9, 22, 13);
sun.target.position.set(1, 0, 0);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, { left: -26, right: 26, top: 20, bottom: -20, near: 1, far: 80 });
sun.shadow.bias = -0.0004;
sun.shadow.normalBias = 0.03;
sun.shadow.radius = 5;
scene.add(sun, sun.target);

// ---------- 小工具 ----------
const mat = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.78, metalness: 0, ...o });
const basic = (color, o = {}) => new THREE.MeshBasicMaterial({ color, toneMapped: false, ...o });
function add(geo, m, x = 0, y = 0, z = 0, parent = scene, shadow = true) {
  const mesh = new THREE.Mesh(geo, m);
  mesh.position.set(x, y, z);
  mesh.castShadow = shadow; mesh.receiveShadow = true;
  parent.add(mesh);
  return mesh;
}
const box = (w, h, d, m, x, y, z, p, s) => add(new THREE.BoxGeometry(w, h, d), m, x, y, z, p, s);
const rbox = (w, h, d, r, m, x, y, z, p, s) => add(new RoundedBoxGeometry(w, h, d, 3, r), m, x, y, z, p, s);
function canvasTex(w, h, draw) {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  const g = c.getContext('2d');
  draw(g, w, h);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  t.userData = { c, g };
  return t;
}
const rr = (g, x, y, w, h, r) => { g.beginPath(); g.roundRect(x, y, w, h, r); };
const R = ((a) => () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; })(20261006);

function sprite(tex, w, h, parent = scene) {
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, depthTest: false, toneMapped: false }));
  s.scale.set(w, h, 1);
  s.renderOrder = 20;
  s.userData.base = [w, h];
  parent.add(s);
  return s;
}
function setSprite(s, k, opacity = 1) {
  s.visible = k > 0.001 && opacity > 0.001;
  s.scale.set(s.userData.base[0] * k, s.userData.base[1] * k, 1);
  s.material.opacity = opacity;
}
function pill(text, { w = 420, h = 110, font = '600 52px Inter', border = ACC, fg = INK, bg = '#ffffff' } = {}) {
  return canvasTex(w, h, (g) => {
    rr(g, 6, 6, w - 12, h - 12, (h - 12) / 2); g.fillStyle = bg; g.fill();
    g.lineWidth = 6; g.strokeStyle = border; g.stroke();
    g.font = font; g.fillStyle = fg; g.textAlign = 'center'; g.textBaseline = 'middle';
    g.fillText(text, w / 2, h / 2 + 2);
  });
}

// ---------- 场景：主办公室（等距剖面模型） ----------
const flMat = mat(C.floor), sideMat = mat(C.side), innerMat = mat(C.inner), wallMat = mat(C.wall);
box(17, 0.3, 11, flMat, 0, -0.15, 0);
box(17, 0.3, 11, sideMat, 0, -4.35, 0);
box(17, 3.9, 0.3, innerMat, 0, -2.25, -5.35);
box(0.3, 3.9, 11, innerMat, -8.35, -2.25, 0);
const fadeMat = mat(C.side, { transparent: true });
const frontPanel = box(17, 3.92, 0.3, fadeMat, 0, -2.25, 5.35, scene, false);
const rightPanel = box(0.3, 3.92, 10.7, fadeMat, 8.35, -2.25, 0, scene, false);
// 墙
box(17, 3.4, 0.3, wallMat, 0, 1.7, -5.35);
box(0.3, 3.4, 2.3, wallMat, -8.35, 1.7, -4.35);
box(0.3, 3.4, 4.7, wallMat, -8.35, 1.7, 3.15);
box(0.3, 0.9, 4.0, wallMat, -8.35, 0.45, -1.2);
box(0.3, 0.7, 4.0, wallMat, -8.35, 3.05, -1.2);
box(0.12, 1.8, 0.08, mat(0xd7dcda), -8.3, 1.8, -1.2);
const glass = new THREE.MeshStandardMaterial({ color: 0xd4e6ea, transparent: true, opacity: 0.22, roughness: 0.1 });
box(0.04, 1.8, 4.0, glass, -8.35, 1.8, -1.2, scene, false);
// 墙上细节：架子、绿植
box(3.2, 0.06, 0.4, mat(0xe0e4e2), -4.5, 2.1, -5.0);
[[-5.6, 0.32, 0xcfd6d3], [-5.1, 0.42, 0xffffff], [-3.6, 0.26, 0xa9dcc3]].forEach(([x, h, c]) => box(0.3, h, 0.28, mat(c), x, 2.13 + h / 2, -5.0));
function plant(x, z, s = 1) {
  const g = new THREE.Group(); g.position.set(x, 0, z); g.scale.setScalar(s); scene.add(g);
  add(new THREE.CylinderGeometry(0.28, 0.22, 0.5, 24), mat(0xffffff), 0, 0.25, 0, g);
  const leaf = mat(0x8cc4a7);
  [[0, 0.85, 0, 0.38], [0.2, 1.1, 0.1, 0.28], [-0.18, 1.05, -0.05, 0.3]].forEach(([a, b, c, r]) => add(new THREE.IcosahedronGeometry(r, 1), leaf, a, b, c, g));
  return g;
}
plant(-7.5, -4.5); plant(7.6, -4.6, 0.9);
// 地上的线（隔墙其实只是画的线）
const lineMat = basic(C.line);
[-2.5, 2.5].forEach((x) => add(new THREE.PlaneGeometry(0.07, 5.4), lineMat, x, 0.004, -0.75, scene, false).rotation.x = -Math.PI / 2);
const partitions = [-2.5, 2.5].map((x) => {
  const g = new THREE.Group(); g.position.set(x, 0, -0.75); scene.add(g);
  box(0.08, 1.5, 5.4, mat(0xe3e8e6), 0, 0.75, 0, g);
  box(0.1, 0.05, 5.4, basic(0x9fb1a9), 0, 1.52, 0, g);
  return g;
});

// ---------- 地下：唯一的那台大电脑 ----------
const pcMat = mat(0xf9faf9);
const bigPC = rbox(6.4, 2.0, 3.0, 0.12, pcMat, 0, -3.2, -0.4);
const ledMats = [];
for (let i = 0; i < 3; i++) {
  const m = basic(C.accent);
  ledMats.push(m);
  box(0.14, 1.4, 0.02, m, -1.9 + i * 1.9, -3.2, 1.11, scene, false);
  for (let k = 0; k < 5; k++) box(1.0, 0.04, 0.02, mat(0xd2d8d5), -1.9 + i * 1.9 + 0.62, -3.7 + k * 0.2, 1.11, scene, false);
}
const basementLight = new THREE.PointLight(0xffffff, 0, 16, 1.2);
basementLight.position.set(0, -1.6, 4.4);
scene.add(basementLight);

// ---------- 屏幕内容贴图 ----------
function screenTex(kind) {
  const t = canvasTex(512, 1024, (g, w, h) => {
    g.fillStyle = '#f6f9f7'; g.fillRect(0, 0, w, h);
    for (let y = 0; y < h; y += 64) {
      const r = R();
      if (kind === 'researcher' && r < 0.3) {
        for (let b = 0; b < 8; b++) { const bh = 10 + R() * 34; g.fillStyle = b === 5 ? ACC : '#c9d3cf'; g.fillRect(40 + b * 30, y + 52 - bh, 20, bh); }
        g.fillStyle = '#dfe6e3'; g.fillRect(320, y + 14, 150, 12); g.fillRect(320, y + 34, 110, 12);
      } else if (kind === 'finance' && r < 0.55) {
        g.font = '600 26px Inter'; g.fillStyle = '#8b9692';
        g.fillText((R() * 9000 + 100).toFixed(2), 40, y + 40);
        g.fillStyle = R() < 0.4 ? ACC : '#4d5753';
        g.fillText((R() < 0.5 ? '+' : '−') + (R() * 900).toFixed(2), 300, y + 40);
      } else {
        g.fillStyle = r < 0.12 ? ACC : '#cdd6d2';
        rr(g, 40, y + 16, 140 + R() * 300, 14, 7); g.fill();
        g.fillStyle = '#e1e7e4';
        rr(g, 40, y + 38, 100 + R() * 260, 12, 6); g.fill();
      }
    }
  });
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(1, 320 / 1024);
  return t;
}
function plateTex(text) {
  return canvasTex(512, 128, (g, w, h) => {
    g.fillStyle = '#ffffff'; g.fillRect(0, 0, w, h);
    g.fillStyle = ACC; g.fillRect(0, h - 14, w, 14);
    g.font = '800 62px Inter'; g.letterSpacing = '5px'; g.fillStyle = INK; g.textAlign = 'center'; g.textBaseline = 'middle';
    g.fillText(text, w / 2 + 2, h / 2 - 5);
  });
}
const keysTex = canvasTex(256, 80, (g, w, h) => {
  g.fillStyle = '#e9edeb'; g.fillRect(0, 0, w, h);
  g.fillStyle = '#ffffff';
  for (let r = 0; r < 4; r++) for (let c = 0; c < 12; c++) { rr(g, 6 + c * 20.5, 5 + r * 18.5, 17, 15, 3); g.fill(); }
});

// ---------- 小机器人（几何体） ----------
function makeBot(kind) {
  const g = new THREE.Group();
  const body = new THREE.Group(); g.add(body);
  const white = mat(C.bot, { roughness: 0.5 }), shade = mat(C.shade), visorM = mat(0x24302b, { roughness: 0.35 }), eye = basic(C.accent);
  const head = new THREE.Group(); body.add(head);
  add(new THREE.CylinderGeometry(0.24, 0.27, 0.1, 32), shade, 0, 0.05, 0, body);
  if (kind === 'researcher') {
    add(new THREE.CylinderGeometry(0.29, 0.31, 0.6, 32), white, 0, 0.4, 0, body);
    head.position.y = 0.98;
    add(new THREE.SphereGeometry(0.27, 32, 24), white, 0, 0, 0, head);
    add(new THREE.CylinderGeometry(0.015, 0.015, 0.22, 8), shade, 0, 0.36, 0, head);
    add(new THREE.SphereGeometry(0.05, 16, 12), eye, 0, 0.48, 0, head);
    rbox(0.36, 0.14, 0.1, 0.05, visorM, 0, 0.02, -0.215, head);
  } else if (kind === 'writer') {
    add(new THREE.CylinderGeometry(0.2, 0.35, 0.66, 32), white, 0, 0.43, 0, body);
    head.position.y = 1.0;
    add(new THREE.SphereGeometry(0.25, 32, 24), white, 0, 0, 0, head);
    add(new THREE.TorusGeometry(0.255, 0.025, 8, 40), basic(C.accent), 0, 0.03, 0, head).rotation.x = Math.PI / 2;
    rbox(0.34, 0.13, 0.1, 0.05, visorM, 0, 0.02, -0.195, head);
  } else {
    rbox(0.62, 0.58, 0.48, 0.09, white, 0, 0.39, 0, body);
    head.position.y = 0.92;
    rbox(0.5, 0.38, 0.42, 0.1, white, 0, 0, 0, head);
    rbox(0.38, 0.15, 0.06, 0.04, visorM, 0, 0.01, -0.205, head);
    add(new THREE.SphereGeometry(0.045, 16, 12), eye, 0, 0.23, 0, head);
  }
  const ez = kind === 'finance' ? -0.24 : kind === 'writer' ? -0.25 : -0.27;
  [-0.075, 0.075].forEach((x) => add(new THREE.CapsuleGeometry(0.022, 0.03, 4, 8), eye, x, 0.025, ez, head, false));
  const hands = [-1, 1].map((s) => add(new THREE.SphereGeometry(0.075, 16, 12), shade, s * (kind === 'finance' ? 0.38 : 0.35), 0.62, -0.16, body));
  return { g, body, head, hands, kind };
}

// ---------- 工位 ----------
const deskMat = mat(C.desk), legMat = mat(C.leg);
function makeStation(x, kind, label) {
  const g = new THREE.Group(); g.position.set(x, 0, -0.8); scene.add(g);
  rbox(2.6, 0.08, 1.3, 0.03, deskMat, 0, 0.76, 0, g);
  [[-1.2, -0.56], [1.2, -0.56], [-1.2, 0.56], [1.2, 0.56]].forEach(([a, b]) => box(0.06, 0.72, 0.06, legMat, a, 0.36, b, g));
  box(0.42, 0.03, 0.26, legMat, -0.15, 0.815, -0.38, g);
  box(0.08, 0.4, 0.06, legMat, -0.15, 1.0, -0.42, g);
  rbox(1.5, 0.92, 0.06, 0.03, mat(0x2d3532, { roughness: 0.4 }), -0.15, 1.5, -0.45, g);
  const tex = screenTex(kind);
  const scrMat = basic(0xffffff, { map: tex });
  const screen = add(new THREE.PlaneGeometry(1.4, 0.82), scrMat, -0.15, 1.5, -0.417, g, false);
  const kb = box(0.72, 0.025, 0.22, mat(0xffffff), -0.15, 0.812, 0.12, g);
  add(new THREE.PlaneGeometry(0.7, 0.2), basic(0xffffff, { map: keysTex }), -0.15, 0.826, 0.12, g, false).rotation.x = -Math.PI / 2;
  // 台灯
  add(new THREE.CylinderGeometry(0.12, 0.14, 0.03, 24), legMat, 1.0, 0.815, -0.35, g);
  box(0.03, 0.55, 0.03, legMat, 1.0, 1.08, -0.35, g);
  const shadeM = add(new THREE.ConeGeometry(0.16, 0.18, 24, 1, true), mat(0xffffff, { side: THREE.DoubleSide }), 0.92, 1.38, -0.3, g);
  shadeM.rotation.z = 0.5;
  const bulbMat = basic(0xffffff);
  add(new THREE.SphereGeometry(0.05, 12, 8), bulbMat, 0.9, 1.33, -0.29, g, false);
  const lamp = new THREE.PointLight(0xfff6ea, 0, 6, 1.4);
  lamp.position.set(0.85, 1.2, -0.2); g.add(lamp);
  add(new THREE.CylinderGeometry(0.06, 0.055, 0.13, 16), mat(C.accent), 0.55, 0.865, -0.15, g);
  // 名牌
  const plate = new THREE.Group(); plate.position.set(0.65, 0.8, 0.5); g.add(plate);
  const plateInner = new THREE.Group(); plate.add(plateInner);
  plateInner.rotation.x = -0.22;
  box(1.0, 0.25, 0.06, mat(0xf4f5f4), 0, 0.125, 0, plateInner);
  add(new THREE.PlaneGeometry(0.98, 0.245), basic(0xffffff, { map: plateTex(label) }), 0, 0.125, 0.031, plateInner, false);
  // 工位地面光圈
  const glowMat = basic(C.accent, { transparent: true, opacity: 0 });
  const glowTex = canvasTex(256, 256, (gg) => { rr(gg, 8, 8, 240, 240, 40); gg.lineWidth = 10; gg.strokeStyle = '#fff'; gg.stroke(); });
  glowMat.map = glowTex;
  const glow = add(new THREE.PlaneGeometry(3.3, 3.0), glowMat, 0, 0.006, 0.55, g, false);
  glow.rotation.x = -Math.PI / 2;
  const bot = makeBot(kind);
  bot.g.position.set(-0.55, 0, 1.1); g.add(bot.g);
  return { g, kind, tex, scrMat, screen, plate, lamp, bulbMat, glowMat, bot, kb, home: new THREE.Vector3(x, 0, -0.8) };
}
const ST = [makeStation(-5, 'researcher', 'RESEARCHER'), makeStation(0, 'writer', 'WRITER'), makeStation(5, 'finance', 'FINANCE')];
const [stR, stW, stF] = ST;
const tmpV = new THREE.Vector3();
const monitorTop = (st) => st.g.localToWorld(tmpV.set(-0.15, 1.98, -0.45)).clone();

// ---------- 发光线缆（从同一台电脑接到三块屏幕） ----------
function cable(points, radius = 0.06) {
  const curve = new THREE.CatmullRomCurve3(points.map((p) => new THREE.Vector3(...p)), false, 'catmullrom', 0.05);
  const geo = new THREE.TubeGeometry(curve, 160, radius, 8, false);
  const m = basic(C.accent, { transparent: true, opacity: 1 });
  const mesh = add(geo, m, 0, 0, 0, scene, false);
  mesh.userData.count = geo.index.count;
  geo.setDrawRange(0, 0);
  return mesh;
}
function setCable(c, p, opacity = 1) {
  const n = Math.floor(c.userData.count * clamp(p) / 6) * 6;
  c.geometry.setDrawRange(0, n);
  c.material.opacity = opacity;
  c.visible = n > 0 && opacity > 0.01;
}
const corner = (a, b, k = 0.12) => [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k];
function cablePath(x, pcx) {
  const P = [[x, 0.84, -1.2], [x, 0.84, -1.48], [x, 0.0, -1.48], [x, -1.5, -1.48], [x, -1.5, 0.5], [pcx, -1.5, 0.5], [pcx, -2.2, 0.5]];
  const pts = [P[0]];
  for (let i = 1; i < P.length - 1; i++) pts.push(corner(P[i], P[i - 1], 0.08), P[i], corner(P[i], P[i + 1], 0.08));
  pts.push(P[P.length - 1]);
  return pts;
}
const cables = [cable(cablePath(-5.15, -2.2)), cable(cablePath(-0.15, 0.1)), cable(cablePath(4.85, 2.2))];

// ---------- 钥匙串 ----------
const keyring = new THREE.Group(); keyring.position.set(0, 3.55, -0.6); scene.add(keyring);
const metal = mat(0xb9c1bd, { metalness: 0.6, roughness: 0.3 });
function makeKey(m = metal) {
  const k = new THREE.Group();
  add(new THREE.TorusGeometry(0.12, 0.035, 10, 28), m, 0, -0.12, 0, k);
  box(0.06, 0.5, 0.035, m, 0, -0.48, 0, k);
  box(0.12, 0.05, 0.035, m, 0.06, -0.62, 0, k);
  box(0.09, 0.05, 0.035, m, 0.045, -0.52, 0, k);
  return k;
}
add(new THREE.TorusGeometry(0.24, 0.028, 10, 36), metal, 0, 0, 0, keyring);
const keyA = makeKey(), keyB = makeKey(mat(C.accent, { metalness: 0.2, roughness: 0.35 }));
keyA.position.set(-0.08, -0.2, 0); keyA.rotation.z = 0.35;
keyB.position.set(0.08, -0.2, 0.02); keyB.rotation.z = -0.35;
keyring.add(keyA, keyB);
const tagFiles = sprite(pill('files', { w: 300 }), 0.95, 0.35, keyring);
tagFiles.position.set(-1.05, -0.62, 0);
const tagLogins = sprite(pill('browser logins', { w: 560 }), 1.75, 0.35, keyring);
tagLogins.position.set(1.45, -0.62, 0);
const keyLines = ST.map(() => {
  const m = basic(C.accent, { transparent: true });
  return add(new THREE.CylinderGeometry(0.018, 0.018, 1, 6), m, 0, 0, 0, scene, false);
});
const UP = new THREE.Vector3(0, 1, 0);
function setLine(mesh, a, b, p, opacity) {
  const bb = a.clone().lerp(b, clamp(p));
  const d = bb.clone().sub(a), len = d.length();
  mesh.visible = len > 0.01 && opacity > 0.01;
  if (!mesh.visible) return;
  mesh.position.copy(a).addScaledVector(d, 0.5);
  mesh.quaternion.setFromUnitVectors(UP, d.normalize());
  mesh.scale.set(1, len, 1);
  mesh.material.opacity = opacity;
}

// ---------- 窗外：家里的笔记本电脑 ----------
const home = new THREE.Group(); home.position.set(-11.8, 0, 7.4); home.rotation.y = 0.35; scene.add(home);
rbox(4.4, 0.4, 3.4, 0.06, mat(C.floor), 0, -0.2, 0, home);
rbox(4.4, 1.2, 3.4, 0.06, sideMat, 0, -1.0, 0, home);
rbox(1.6, 0.06, 0.9, 0.02, deskMat, 0.2, 0.72, -0.2, home);
[[-0.5, -0.5], [0.9, -0.5], [-0.5, 0.1], [0.9, 0.1]].forEach(([a, b]) => box(0.05, 0.7, 0.05, legMat, a, 0.35, b, home));
const laptop = new THREE.Group(); laptop.position.set(0.2, 0.75, -0.2); laptop.scale.setScalar(1.35); home.add(laptop);
box(0.86, 0.035, 0.6, mat(0xdfe3e1), 0, 0.017, 0, laptop);
const lid = new THREE.Group(); lid.position.set(0, 0.035, -0.3); laptop.add(lid);
box(0.86, 0.025, 0.6, mat(0xdfe3e1), 0, 0.0125, 0.3, lid);
const lapScreenMat = basic(0xffffff, { map: screenTex('writer') });
const lapScreen = add(new THREE.PlaneGeometry(0.78, 0.52), lapScreenMat, 0, -0.002, 0.3, lid, false);
lapScreen.rotation.x = Math.PI / 2;
const homePlant = plant(0, 0, 0.75); home.add(homePlant); homePlant.position.set(-1.4, 0, -0.9);
// 椅子
rbox(0.5, 0.08, 0.5, 0.03, mat(0xffffff), 0.2, 0.45, 0.5, home);
rbox(0.5, 0.5, 0.06, 0.03, mat(0xffffff), 0.2, 0.75, 0.75, home);
box(0.05, 0.42, 0.05, legMat, 0.2, 0.21, 0.5, home);

// ---------- 门（门上只有名字） ----------
const door = new THREE.Group(); door.position.set(2.5, 0, 1.25); scene.add(door);
const frameM = mat(0xd9dedc);
box(0.14, 2.2, 0.08, frameM, 0, 1.1, -0.56, door);
box(0.14, 2.2, 0.08, frameM, 0, 1.1, 0.56, door);
box(0.14, 0.1, 1.2, frameM, 0, 2.2, 0, door);
const panel = new THREE.Group(); panel.position.set(0, 0, -0.5); door.add(panel);
box(0.06, 2.1, 1.0, mat(0xfcfcfc), 0, 1.06, 0.5, panel);
const doorPlate = add(new THREE.PlaneGeometry(0.62, 0.155), basic(0xffffff, { map: plateTex('FINANCE') }), -0.033, 1.62, 0.5, panel, false);
doorPlate.rotation.y = -Math.PI / 2;
add(new THREE.SphereGeometry(0.045, 12, 8), metal, -0.06, 1.0, 0.88, panel);
box(0.03, 0.03, 0.16, metal, -0.09, 1.0, 0.83, panel);
add(new THREE.SphereGeometry(0.045, 12, 8), metal, 0.06, 1.0, 0.88, panel);
const note = new THREE.Group(); note.position.set(-0.036, 1.47, 0.5); panel.add(note);
const noteTex = canvasTex(256, 256, (g) => {
  g.fillStyle = '#e4f4e9'; g.fillRect(0, 0, 256, 256);
  g.fillStyle = 'rgba(255,255,255,0.65)'; g.fillRect(78, 0, 100, 26);
  g.fillStyle = '#26302c'; g.font = '800 50px Inter'; g.textAlign = 'center';
  g.fillText("don't open", 128, 118); g.fillText('finance', 128, 180);
});
const noteMesh = add(new THREE.PlaneGeometry(0.44, 0.44), mat(0xffffff, { map: noteTex, side: THREE.DoubleSide }), 0, -0.22, 0, note, false);
noteMesh.rotation.y = -Math.PI / 2;

// ---------- 规则 1：检查闸门 ----------
const gate = new THREE.Group(); scene.add(gate);
const belt = box(5.6, 0.06, 0.7, mat(0xc7cfcb), -3.8, 0.03, 3.9, gate);
for (let i = 0; i < 18; i++) box(0.04, 0.005, 0.66, basic(0xb1bbb6), -6.5 + i * 0.31, 0.063, 3.9, gate, false);
const slot = add(new THREE.PlaneGeometry(0.78, 0.78), basic(0x1f2725), -1.05, 0.01, 3.9, gate, false); slot.rotation.x = -Math.PI / 2;
const slotRim = add(new THREE.RingGeometry(0.42, 0.48, 4, 1), basic(C.accent), -1.05, 0.012, 3.9, gate, false); slotRim.rotation.x = -Math.PI / 2; slotRim.rotation.z = Math.PI / 4;
const gateM = mat(0xffffff);
box(0.14, 1.4, 0.14, gateM, -3.9, 0.7, 3.38, gate); box(0.14, 1.4, 0.14, gateM, -3.9, 0.7, 4.42, gate);
const beamMat = basic(0xcfd7d3);
box(0.16, 0.16, 1.2, beamMat, -3.9, 1.45, 3.9, gate);
const signTex = canvasTex(820, 150, (g, w, h) => {
  rr(g, 6, 6, w - 12, h - 12, 30); g.fillStyle = '#fff'; g.fill(); g.lineWidth = 6; g.strokeStyle = '#cfd7d3'; g.stroke();
  g.font = '700 60px Inter'; g.fillStyle = INK; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('Every bot may use?', w / 2, h / 2 + 2);
});
const gateSign = sprite(signTex, 2.1, 0.39, gate); gateSign.position.set(-3.9, 2.0, 3.9);
const badgeTex = (kind) => canvasTex(160, 160, (g) => {
  g.beginPath(); g.arc(80, 80, 72, 0, 7); g.fillStyle = kind === 'ok' ? ACC : '#39423f'; g.fill();
  g.strokeStyle = '#fff'; g.lineWidth = 16; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath();
  if (kind === 'ok') { g.moveTo(46, 82); g.lineTo(70, 106); g.lineTo(116, 56); } else { g.moveTo(54, 54); g.lineTo(106, 106); g.moveTo(106, 54); g.lineTo(54, 106); }
  g.stroke();
});
const okBadge = sprite(badgeTex('ok'), 0.55, 0.55, gate), noBadge = sprite(badgeTex('no'), 0.55, 0.55, gate);
okBadge.position.set(-2.5, 2.0, 3.9); noBadge.position.set(-2.5, 2.0, 3.9);
const docItem = new THREE.Group(); scene.add(docItem);
const docTex = canvasTex(200, 250, (g) => {
  g.fillStyle = '#fff'; g.fillRect(0, 0, 200, 250);
  g.fillStyle = ACC; g.fillRect(28, 34, 90, 16);
  g.fillStyle = '#ccd5d1'; for (let i = 0; i < 6; i++) g.fillRect(28, 74 + i * 26, 144 - (i % 3) * 24, 12);
});
rbox(0.42, 0.52, 0.06, 0.02, mat(0xffffff), 0, 0.32, 0, docItem);
add(new THREE.PlaneGeometry(0.4, 0.5), basic(0xffffff, { map: docTex }), 0, 0.32, 0.031, docItem, false);
const keyItem = new THREE.Group(); scene.add(keyItem);
const bigKey = makeKey(mat(0x39423f, { roughness: 0.4 })); bigKey.scale.setScalar(1.15); bigKey.rotation.z = Math.PI / 2; bigKey.position.set(0.4, 0.3, 0);
keyItem.add(bigKey);

// ---------- 规则 2：单独的小房间 ----------
const island = new THREE.Group(); scene.add(island);
box(6, 0.3, 6, flMat, 13, -0.15, 0, island);
box(6, 0.3, 6, sideMat, 13, -2.45, 0, island);
box(6, 2.0, 0.3, innerMat, 13, -1.3, -2.85, island);
box(0.3, 2.0, 6, innerMat, 10.15, -1.3, 0, island);
const smallPC = rbox(2.4, 1.3, 1.6, 0.1, pcMat, 13.3, -1.65, -1.2, island);
const smallLed = basic(C.accent); box(1.4, 0.06, 0.02, smallLed, 13.3, -1.6, -0.39, island, false);
const roomWalls = new THREE.Group(); roomWalls.position.set(0, 0, 0); island.add(roomWalls);
box(6, 2.6, 0.3, wallMat, 13, 1.3, -2.85, roomWalls);
box(0.3, 2.6, 3.3, wallMat, 10.15, 1.3, -1.35, roomWalls);
box(0.3, 2.6, 1.7, wallMat, 10.15, 1.3, 2.15, roomWalls);
box(0.3, 0.4, 1.0, wallMat, 10.15, 2.4, 0.8, roomWalls);
const glass2 = new THREE.MeshStandardMaterial({ color: 0xdcebe5, transparent: true, opacity: 0.2, roughness: 0.1 });
box(6, 2.6, 0.05, glass2, 13, 1.3, 2.97, roomWalls, false);
box(0.05, 2.6, 6, glass2, 15.97, 1.3, 0, roomWalls, false);
box(6, 0.06, 0.08, mat(0xd7dcda), 13, 2.6, 2.97, roomWalls);
box(0.08, 0.06, 6, mat(0xd7dcda), 15.97, 2.6, 0, roomWalls);
const lockedDoor = new THREE.Group(); lockedDoor.position.set(10.15, 0, 0.8); roomWalls.add(lockedDoor);
box(0.08, 2.18, 0.98, mat(0xfcfcfc), 0, 1.1, 0, lockedDoor);
const lockM = mat(C.accent, { roughness: 0.35 });
const shackles = [];
[-1, 1].forEach((s) => {
  const lk = new THREE.Group(); lk.position.set(s * 0.1, 1.05, 0.32); lockedDoor.add(lk);
  rbox(0.08, 0.22, 0.26, 0.03, lockM, 0, 0, 0, lk);
  const sh = add(new THREE.TorusGeometry(0.085, 0.022, 8, 20, Math.PI), metal, 0, 0.11, 0, lk);
  sh.rotation.y = Math.PI / 2;
  add(new THREE.CylinderGeometry(0.02, 0.02, 0.03, 8), mat(0x1f2725), s * 0.04, -0.02, 0, lk).rotation.z = Math.PI / 2;
  shackles.push(sh);
});
const lockBadge = sprite(badgeTex('ok'), 0.5, 0.5, island);
const islandCable = cable([[13.15, 0.84, -1.3], [13.15, 0.84, -1.6], ...[[13.15, 0, -1.6], [13.15, -0.6, -1.6]], [13.3, -0.95, -1.6]]);

// ---------- 规则 3：接管键盘的手 ----------
const hand = new THREE.Group(); scene.add(hand);
const skin = mat(0xf2ede7, { roughness: 0.6 }), sleeve = mat(0x8b9692);
const hpivot = new THREE.Group(); hand.add(hpivot);
add(new THREE.CylinderGeometry(0.1, 0.11, 0.6, 20), sleeve, 0, 0.0, 0.36, hpivot).rotation.x = Math.PI / 2;
add(new THREE.CylinderGeometry(0.075, 0.085, 0.12, 20), skin, 0, 0, 0.04, hpivot).rotation.x = Math.PI / 2;
rbox(0.24, 0.07, 0.24, 0.03, skin, 0, -0.01, -0.1, hpivot);
const fingers = [-0.08, -0.027, 0.027, 0.08].map((x, i) => {
  const f = add(new THREE.CapsuleGeometry(0.024, 0.1 - Math.abs(i - 1.5) * 0.015, 4, 8), skin, x, -0.03, -0.27, hpivot);
  f.rotation.x = Math.PI / 2 + 0.25;
  return f;
});
const thumb = add(new THREE.CapsuleGeometry(0.026, 0.08, 4, 8), skin, -0.15, -0.02, -0.12, hpivot);
thumb.rotation.set(Math.PI / 2, 0, 0.7);
function loginTex() {
  return canvasTex(512, 300, () => {});
}
const login = loginTex();
let loginKey = '';
function drawLogin(dots, done) {
  const key = dots + '|' + done;
  if (key === loginKey) return;
  loginKey = key;
  const { g } = login.userData, w = 512, h = 300;
  g.fillStyle = '#f6f9f7'; g.fillRect(0, 0, w, h);
  g.fillStyle = '#e3e9e6'; g.fillRect(0, 0, w, 34);
  ['#c9d1cd', '#c9d1cd', '#c9d1cd'].forEach((c, i) => { g.beginPath(); g.arc(22 + i * 22, 17, 6, 0, 7); g.fillStyle = c; g.fill(); });
  g.fillStyle = INK; g.font = '700 30px Inter'; g.textAlign = 'center'; g.fillText('Sign in', w / 2, 82);
  rr(g, 116, 104, 280, 44, 10); g.fillStyle = '#fff'; g.fill(); g.strokeStyle = '#cfd7d3'; g.lineWidth = 3; g.stroke();
  g.fillStyle = '#9aa5a0'; g.font = '500 20px Inter'; g.textAlign = 'left'; g.fillText('Username', 132, 133);
  rr(g, 116, 160, 280, 44, 10); g.fillStyle = '#fff'; g.fill(); g.strokeStyle = dots > 0 && !done ? ACC : '#cfd7d3'; g.stroke();
  g.fillStyle = INK; for (let i = 0; i < dots; i++) { g.beginPath(); g.arc(138 + i * 22, 182, 6, 0, 7); g.fill(); }
  rr(g, 176, 220, 160, 44, 22); g.fillStyle = ACC; g.fill();
  g.fillStyle = '#fff'; g.font = '700 20px Inter'; g.textAlign = 'center'; g.fillText('Sign in', w / 2, 249);
  if (done) {
    g.fillStyle = 'rgba(246,249,247,0.82)'; g.fillRect(0, 34, w, h);
    g.beginPath(); g.arc(w / 2, 165, 60, 0, 7); g.fillStyle = ACC; g.fill();
    g.strokeStyle = '#fff'; g.lineWidth = 14; g.lineCap = 'round'; g.lineJoin = 'round';
    g.beginPath(); g.moveTo(w / 2 - 28, 168); g.lineTo(w / 2 - 6, 190); g.lineTo(w / 2 + 30, 144); g.stroke();
  }
  login.needsUpdate = true;
}
const finScreenTex = stF.tex;

// ---------- 第 7 句：已登录：Bank ----------
const bankTex = canvasTex(660, 170, (g, w, h) => {
  rr(g, 6, 6, w - 12, h - 12, 34); g.fillStyle = '#fff'; g.fill(); g.lineWidth = 5; g.strokeStyle = '#d3dad7'; g.stroke();
  // 通用银行图标：山墙 + 柱子
  g.fillStyle = '#39423f';
  g.beginPath(); g.moveTo(40, 72); g.lineTo(88, 42); g.lineTo(136, 72); g.closePath(); g.fill();
  for (let i = 0; i < 4; i++) g.fillRect(48 + i * 24, 80, 12, 40);
  g.fillRect(40, 124, 96, 10);
  g.font = '600 50px Inter'; g.fillStyle = INK; g.textBaseline = 'middle';
  g.fillText('Signed in: Bank', 160, h / 2 + 2);
  g.beginPath(); g.arc(w - 54, h / 2, 22, 0, 7); g.fillStyle = ACC; g.fill();
  g.strokeStyle = '#fff'; g.lineWidth = 7; g.lineCap = 'round'; g.beginPath(); g.moveTo(w - 65, h / 2 + 1); g.lineTo(w - 57, h / 2 + 9); g.lineTo(w - 43, h / 2 - 8); g.stroke();
});
const bankBadges = ST.map(() => sprite(bankTex, 1.9, 0.49));

// ---------- 镜头 ----------
const shots = [];
function key(t, p, l, fov = 30, e = 'io') { shots.push({ t, p: new THREE.Vector3(...p), l: new THREE.Vector3(...l), fov, e }); }
const deskShot = (x, dz = 0) => [[x + 4.6, 4.6, 7.4 + dz], [x - 0.4, 1.05, -0.5]];
const cutT = at(12, 0.5);
key(0, [18, 15.5, 20], [0, 0.4, -0.6], 30);
key(B(2) - 0.15, [12.5, 9.5, 14.5], [-0.6, 0.7, -0.6], 30);
key(B(2) + 0.35, ...deskShot(-5), 30);
key(at(2, 0.4), ...deskShot(0, 0.2), 30, 'in');
key(B(3) - 0.05, ...deskShot(5, 0.4), 30, 'out');
key(B(3) + 1.0, [-4.2, 6.6, 18.6], [-7.2, 0.6, 2.4], 36);
key(B(4) - 0.1, [-4.8, 6.2, 17.6], [-7.0, 0.6, 2.2], 36);
key(B(4) + 0.6, [7.5, 6.6, 14.5], [-0.5, 0.9, -0.8], 31);
key(B(5), [6.6, 5.6, 12.2], [-0.4, 1.0, -0.9], 31);
key(B(5) + 1.7, [12.5, 0.9, 16.8], [0, -1.3, 0], 32);
key(B(6), [13.6, 1.5, 16.4], [0, -1.1, 0], 32);
key(B(7) - 0.01, [22, 13.5, 19], [0, 0.4, 0], 30);
key(B(7), [9.6, 4.1, 6.4], [4.6, 1.55, -0.9], 30, 'cut');
key(at(7, 0.5), [9.2, 4.3, 6.9], [4.4, 1.6, -0.9], 30);
key(B(8) - 0.15, [6.5, 7.6, 14.5], [-0.1, 1.5, -0.7], 30);
key(B(8), [-0.6, 2.3, 5.2], [2.5, 1.3, 1.0], 31, 'cut');
key(B(9) - 0.1, [-0.1, 2.2, 4.6], [2.6, 1.3, 0.9], 30);
key(B(9) + 0.9, [11, 21, 16], [0.5, 0, 0], 32);
key(B(10), [10, 21.5, 15.5], [0.5, 0, 0], 32);
key(B(10) + 0.8, [-3.4, 3.6, 10.9], [-3.8, 0.85, 3.9], 32);
key(B(11) - 0.05, [-3.1, 3.45, 10.4], [-3.7, 0.85, 3.9], 32);
key(B(11) + 1.0, [20, 11, 20], [7.5, 0.3, 0], 34);
key(cutT - 0.01, [21, 10.5, 18.5], [8.5, 0.4, 0], 34);
key(cutT, [12.85, 2.0, 1.05], [13.15, 1.22, -1.0], 38, 'cut');
key(B(13) - 0.01, [12.85, 1.9, 0.85], [13.15, 1.24, -1.0], 38);
key(B(13), [0.9, 1.7, 1.95], [2.45, 1.6, 1.3], 30, 'cut');
key(DUR - 0.2, [-3.6, 2.0, 5.2], [2.5, 1.3, 1.1], 30);
key(DUR + 1, [-3.6, 2.0, 5.2], [2.5, 1.3, 1.1], 30);
const curve = { io: ease, in: eIn, out: eOut, lin: (x) => x, cut: ease };
function placeCamera(t) {
  let i = 0;
  while (i < shots.length - 1 && shots[i + 1].t <= t) i++;
  const a = shots[i], b = shots[Math.min(i + 1, shots.length - 1)];
  const x = a === b ? 0 : curve[b.e](ramp(t, a.t, b.t));
  camera.position.lerpVectors(a.p, b.p, x);
  const l = a.l.clone().lerp(b.l, x);
  camera.fov = lerp(a.fov, b.fov, x);
  camera.updateProjectionMatrix();
  camera.lookAt(l);
}

// ---------- 2D 叠加层 ----------
function veil(a) { if (a <= 0) return; ctx.fillStyle = `rgba(243,246,245,${a})`; ctx.fillRect(0, 0, W, H); }
function shadowCard(x, y, w, h, r, alpha) {
  ctx.save(); ctx.globalAlpha = alpha;
  ctx.shadowColor = 'rgba(30,40,36,0.16)'; ctx.shadowBlur = 40; ctx.shadowOffsetY = 12;
  rr(ctx, x, y, w, h, r); ctx.fillStyle = '#fff'; ctx.fill();
  ctx.restore();
}
function drawQuote(t) {
  const a = win(t, B(6) + 0.1, B(7) - 0.05, 0.45, 0.35);
  if (a <= 0) return;
  veil(0.84 * a);
  ctx.save();
  const ty = (1 - eOut(ramp(t, B(6) + 0.1, B(6) + 0.8))) * 30;
  ctx.globalAlpha = a; ctx.translate(0, ty);
  ctx.font = '700 76px Inter';
  const L2 = 'not separate security boundaries.”', w2 = ctx.measureText(L2).width, X = Math.round((W - w2) / 2) + 30;
  ctx.fillStyle = ACC; ctx.font = '800 170px Inter'; ctx.textBaseline = 'alphabetic';
  ctx.fillText('“', X - 105, 440);
  const l1 = ramp(t, at(6, 0.3), at(6, 0.42)), l2 = ramp(t, at(6, 0.56), at(6, 0.68));
  ctx.fillStyle = INK; ctx.font = '700 76px Inter';
  ctx.globalAlpha = a * eOut(l1); ctx.fillText('separate work surfaces,', X, 410 + (1 - eOut(l1)) * 20);
  ctx.globalAlpha = a * eOut(l2); ctx.fillText(L2, X, 510 + (1 - eOut(l2)) * 20);
  const u = eOut(ramp(t, at(6, 0.8), at(6, 0.98)));
  if (u > 0) { ctx.globalAlpha = a; ctx.fillStyle = ACC; ctx.fillRect(X, 540, (w2 - 30) * u, 8); }
  ctx.globalAlpha = a * ramp(t, B(6) + 0.3, B(6) + 0.9);
  ctx.fillStyle = GREY; ctx.font = '600 40px Inter';
  ctx.fillText('— xAI Grok Bot docs', X + 4, 625);
  ctx.restore();
}
function noteIcon(x, y, s) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(-0.06);
  ctx.fillStyle = '#e4f4e9'; ctx.shadowColor = 'rgba(0,0,0,0.12)'; ctx.shadowBlur = 16; ctx.shadowOffsetY = 6;
  ctx.fillRect(-s / 2, -s / 2, s, s); ctx.shadowColor = 'transparent';
  ctx.fillStyle = 'rgba(255,255,255,0.7)'; ctx.fillRect(-s * 0.2, -s / 2 - 6, s * 0.4, 18);
  ctx.fillStyle = '#9aa8a2'; ctx.fillRect(-s * 0.3, -s * 0.12, s * 0.6, 8); ctx.fillRect(-s * 0.3, s * 0.08, s * 0.42, 8);
  ctx.restore();
}
function lockIcon(x, y, s, col = ACC) {
  ctx.save(); ctx.translate(x, y);
  ctx.strokeStyle = '#8f9a96'; ctx.lineWidth = s * 0.12; ctx.beginPath(); ctx.arc(0, -s * 0.12, s * 0.26, Math.PI, 0); ctx.lineTo(s * 0.26, s * 0.05); ctx.moveTo(-s * 0.26, -s * 0.12); ctx.lineTo(-s * 0.26, s * 0.05); ctx.stroke();
  rr(ctx, -s * 0.42, -s * 0.02, s * 0.84, s * 0.6, s * 0.1); ctx.fillStyle = col; ctx.fill();
  ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(0, s * 0.24, s * 0.07, 0, 7); ctx.fill(); ctx.fillRect(-s * 0.03, s * 0.24, s * 0.06, s * 0.15);
  ctx.restore();
}
function drawNotLock(t) {
  const a = win(t, at(8, 0.6), B(9), 0.3, 0.3);
  if (a <= 0) return;
  const k = backOut(ramp(t, at(8, 0.6), at(8, 0.6) + 0.45));
  ctx.save(); ctx.globalAlpha = a;
  shadowCard(960 - 260, 70, 520, 210, 40, a);
  ctx.translate(960, 175); ctx.scale(k, k);
  noteIcon(-140, 0, 110);
  ctx.fillStyle = INK; ctx.font = '800 110px Inter'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('≠', 0, 4);
  lockIcon(140, -10, 130);
  ctx.restore();
}
const RULES = ['Shared things only', 'Separate account', 'You sign in'];
function drawRules(t) {
  const a = win(t, at(9, 0.1), B(13), 0.35, 0.35);
  if (a <= 0) return;
  const x = 60, y = 56, w = 540;
  const slide = (1 - eOut(ramp(t, at(9, 0.1), at(9, 0.1) + 0.5))) * -40;
  ctx.save(); ctx.translate(slide, 0);
  shadowCard(x, y, w, 290, 32, a);
  ctx.globalAlpha = a;
  ctx.fillStyle = ACC; ctx.font = '800 30px Inter'; ctx.letterSpacing = '4px'; ctx.textBaseline = 'middle';
  ctx.fillText('3 RULES', x + 36, y + 50); ctx.letterSpacing = '0px';
  const starts = [B(10), B(11), B(12)];
  RULES.forEach((r, i) => {
    const on = ramp(t, starts[i], starts[i] + 0.35), cy = y + 112 + i * 66;
    const cur = t >= starts[i] && (i === 2 || t < starts[i + 1]);
    ctx.beginPath(); ctx.arc(x + 62, cy, 24, 0, 7);
    ctx.fillStyle = on > 0 ? `rgba(34,181,115,${on})` : '#fff'; ctx.fill();
    ctx.lineWidth = 3; ctx.strokeStyle = on > 0 ? ACC : '#c9d1cd'; ctx.stroke();
    ctx.fillStyle = on > 0.5 ? '#fff' : '#9aa5a0'; ctx.font = '800 26px Inter'; ctx.textAlign = 'center'; ctx.fillText(String(i + 1), x + 62, cy + 1);
    ctx.textAlign = 'left'; ctx.font = `${cur ? 700 : 600} 38px Inter`;
    ctx.fillStyle = on > 0 ? (cur ? INK : '#56615c') : '#b3bcb8';
    ctx.fillText(r, x + 108, cy + 2);
  });
  ctx.restore();
}
function drawChat(t) {
  const a = win(t, B(12) + 0.05, cutT, 0.35, 0.22);
  if (a <= 0) return;
  veil(0.72 * a);
  const x = 680, y = 170, w = 800, h = 470;
  const ty = (1 - eOut(ramp(t, B(12), B(12) + 0.6))) * 30;
  ctx.save(); ctx.translate(0, ty);
  shadowCard(x, y, w, h, 34, a);
  ctx.globalAlpha = a;
  ctx.fillStyle = '#eef2f0'; rr(ctx, x, y, w, 70, [34, 34, 0, 0]); ctx.fill();
  [0, 1, 2].forEach((i) => { ctx.beginPath(); ctx.arc(x + 40 + i * 28, y + 35, 9, 0, 7); ctx.fillStyle = '#cdd5d1'; ctx.fill(); });
  ctx.fillStyle = GREY; ctx.font = '600 30px Inter'; ctx.textBaseline = 'middle'; ctx.fillText('Chat', x + 140, y + 36);
  // 对方消息（灰条）
  ctx.fillStyle = '#eef2f0'; rr(ctx, x + 40, y + 110, 380, 64, 26); ctx.fill();
  ctx.fillStyle = '#c3ccc8'; rr(ctx, x + 70, y + 136, 300, 14, 7); ctx.fill();
  // 我要发的密码
  const bx = x + 250, by = y + 220, bw = 510, bh = 92;
  const k = eOut(ramp(t, B(12) + 0.3, B(12) + 0.7));
  ctx.globalAlpha = a * k;
  ctx.fillStyle = '#dff3e8'; rr(ctx, bx, by + (1 - k) * 20, bw, bh, 30); ctx.fill();
  ctx.fillStyle = INK; ctx.font = '600 40px Inter'; ctx.fillText('password: k9#Lm2!xQ', bx + 36, by + bh / 2 + 2 + (1 - k) * 20);
  const s = eOut(ramp(t, at(12, 0.2), at(12, 0.36)));
  if (s > 0) {
    ctx.fillStyle = INK; ctx.fillRect(bx + 24, by + bh / 2 - 3, (bw - 48) * s, 7);
    const xk = backOut(ramp(t, at(12, 0.36), at(12, 0.36) + 0.4));
    if (xk > 0) {
      ctx.save(); ctx.translate(bx + bw + 4, by + 6); ctx.scale(xk, xk);
      ctx.beginPath(); ctx.arc(0, 0, 36, 0, 7); ctx.fillStyle = '#39423f'; ctx.fill();
      ctx.strokeStyle = '#fff'; ctx.lineWidth = 8; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(-12, -12); ctx.lineTo(12, 12); ctx.moveTo(12, -12); ctx.lineTo(-12, 12); ctx.stroke();
      ctx.restore();
    }
  }
  ctx.globalAlpha = a;
  // 输入框
  ctx.strokeStyle = '#d3dad7'; ctx.lineWidth = 3; rr(ctx, x + 40, y + h - 100, w - 80, 64, 32); ctx.stroke();
  ctx.fillStyle = '#b3bcb8'; ctx.font = '500 30px Inter'; ctx.fillText('Message', x + 76, y + h - 67);
  ctx.restore();
}

// ---------- 每帧状态 ----------
function setOpacity(m, o) { m.opacity = o; }
function walkPath(pts, p) {
  // pts: [[x,z],...]，按长度均匀插值，返回 {x,z,dx,dz}
  const segs = []; let L = 0;
  for (let i = 1; i < pts.length; i++) { const l = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); segs.push(l); L += l; }
  let d = clamp(p) * L, i = 0;
  while (i < segs.length - 1 && d > segs[i]) { d -= segs[i]; i++; }
  const f = segs[i] ? d / segs[i] : 0, a = pts[i], b = pts[i + 1];
  return { x: lerp(a[0], b[0], f), z: lerp(a[1], b[1], f), dx: b[0] - a[0], dz: b[1] - a[1] };
}
const WR_REST = [-0.55, 0.3];
const PATH_IN = [WR_REST, [0.6, 1.2], [1.95, 1.2], [3.6, 1.2], [4.0, 0.6]];
const PATH_BACK = [[4.0, 0.6], [3.4, 2.4], [1.2, 2.4], [0.2, 1.4], WR_REST];
const yawTo = (dx, dz) => Math.atan2(-dx, -dz);
function angLerp(a, b, x) { let d = ((b - a + Math.PI * 3) % (Math.PI * 2)) - Math.PI; return a + d * x; }

function update(t) {
  // 昼夜
  const night = er(t, at(3, 0.15), at(3, 0.6)) * (1 - er(t, B(5) + 0.4, B(5) + 2.0));
  scene.background.copy(DAY_BG).lerp(NIGHT_BG, night);
  hemi.intensity = lerp(2.0, 0.45, night);
  hemi.color.setHex(0xffffff).lerp(new THREE.Color(0x9fb3cc), night);
  sun.intensity = lerp(2.5, 0.12, night);
  const lampOn = clamp(night * 1.2);
  ST.forEach((st) => { st.lamp.intensity = 7 * lampOn; st.bulbMat.color.setScalar(lerp(0.85, 1.6, lampOn)); });

  // 工位依次亮起
  const lightT = [at(2, 0.0), at(2, 0.27), at(2, 0.5)];
  const botT = [at(1, 0.52), at(1, 0.6), at(1, 0.68)];
  ST.forEach((st, i) => {
    const on = ramp(t, lightT[i], lightT[i] + 0.35);
    st.scrMat.color.setScalar(lerp(0.13, 1, on));
    const flash = Math.max(0, 1 - Math.abs(t - lightT[i] - 0.35) / 0.9);
    st.glowMat.opacity = on * 0.22 + flash * 0.5;
    st.plate.scale.setScalar(Math.max(0.0001, pop(t, lightT[i] + 0.05, 0.5)));
    const b = st.bot;
    b.g.scale.setScalar(Math.max(0.0001, pop(t, botT[i], 0.5)));
    const hello = ramp(t, botT[i] + 0.35, botT[i] + 0.8) - ramp(t, lightT[i] + 0.5, lightT[i] + 1.0);
    b.head.rotation.y = Math.PI * ease(clamp(hello)) * (i === 1 ? -1 : 1);
    // 工作中：屏幕滚动、打字
    const working = t > lightT[i] + 0.4;
    st.tex.offset.y = 1 - (working ? ((t - lightT[i]) * 0.035 * (1 + i * 0.3)) % 1 : 0) - 320 / 1024;
    const typ = working ? 1 : 0;
    b.hands[0].position.y = 0.62 + 0.035 * typ * Math.max(0, Math.sin(t * 17 + i));
    b.hands[1].position.y = 0.62 + 0.035 * typ * Math.max(0, Math.sin(t * 17 + i + Math.PI));
    b.body.position.y = 0.012 * Math.sin(t * 2.2 + i * 2);
  });

  // 家里的笔记本：第 3 句出现并合上
  const homeIn = er(t, B(3) - 0.2, B(3) + 0.8) * (1 - er(t, B(5) + 0.2, B(5) + 1.2));
  home.position.y = lerp(-9, 0, homeIn);
  home.visible = homeIn > 0.001;
  lid.rotation.x = lerp(-1.88, 0, er(t, at(3, 0.66), at(3, 0.9)));
  lapScreenMat.color.setScalar(lerp(1, 0.1, ramp(t, at(3, 0.8), at(3, 0.95))));

  // 第 5 句：反转
  const sink = er(t, B(5) + 0.2, B(5) + 1.3);
  partitions.forEach((p) => { p.scale.y = Math.max(0.0001, 1 - sink); p.visible = sink < 0.999; });
  const cut = er(t, B(5) + 0.5, B(5) + 1.6);
  fadeMat.opacity = 1 - cut;
  frontPanel.visible = rightPanel.visible = cut < 0.99;
  basementLight.intensity = 9 * cut;
  const cabP = ramp(t, B(5) + 0.9, at(5, 0.55));
  const finGone = 1 - er(t, at(11, 0.02), at(11, 0.2));
  cables.forEach((c, i) => setCable(c, eOut(cabP), i === 2 ? finGone : 1));
  ledMats.forEach((m, i) => m.color.setHex(C.accent).multiplyScalar(cut > 0 ? 0.55 + 0.45 * (Math.sin(t * 5 + i * 2) > 0 ? 1 : 0.4) : 0.4));
  // 钥匙串
  const krOut = 1 - er(t, B(8) - 0.35, B(8));
  const kr = pop(t, at(5, 0.52), 0.5) * krOut;
  keyring.visible = kr > 0.001;
  keyring.scale.setScalar(Math.max(0.0001, kr));
  keyring.rotation.z = 0.07 * Math.sin(t * 1.6);
  keyring.rotation.y = 0.25 * Math.sin(t * 0.7);
  const krPulse = 1 + 0.12 * Math.max(0, Math.sin((t - at(7, 0.55)) * 6)) * win(t, at(7, 0.55), at(7, 1), 0.1, 0.3);
  keyring.scale.multiplyScalar(krPulse);
  setSprite(tagFiles, pop(t, at(5, 0.6), 0.45) * krOut);
  setSprite(tagLogins, pop(t, at(5, 0.76), 0.45) * krOut);
  const lineP = eOut(ramp(t, at(5, 0.62), at(5, 0.95)));
  const ringBottom = keyring.localToWorld(new THREE.Vector3(0, -0.24, 0));
  ST.forEach((st, i) => setLine(keyLines[i], ringBottom, monitorTop(st), lineP * krOut, (i === 2 ? finGone : 1) * 0.9 * krOut));

  // 第 7 句：银行登录标签扩散
  const fin = monitorTop(stF).add(new THREE.Vector3(0, 0.42, 0));
  const fadeBank = 1 - ramp(t, B(8) - 0.3, B(8));
  setSprite(bankBadges[2], pop(t, at(7, 0.12), 0.5), fadeBank);
  bankBadges[2].position.copy(fin);
  [0, 1].forEach((i) => {
    const t0 = at(7, i === 1 ? 0.56 : 0.64), p = eOut(ramp(t, t0, t0 + 0.7));
    const dst = monitorTop(ST[i]).add(new THREE.Vector3(0, 0.42, 0));
    const pos = fin.clone().lerp(dst, p); pos.y += Math.sin(Math.PI * p) * 1.3;
    bankBadges[i].position.copy(pos);
    const land = 1 + 0.15 * Math.max(0, 1 - Math.abs(t - t0 - 0.8) / 0.25);
    setSprite(bankBadges[i], t > t0 ? lerp(0.6, 1, p) * land : 0, fadeBank);
    if (t > t0 + 0.6 && t < B(8)) ST[i].scrMat.color.setRGB(1 - 0.2 * win(t, t0 + 0.6, t0 + 1.3, 0.1, 0.4), 1, 1 - 0.2 * win(t, t0 + 0.6, t0 + 1.3, 0.1, 0.4));
  });

  // 第 8 句：门和便利贴
  const dIn = pop(t, B(8) - 0.05, 0.5);
  door.visible = dIn > 0.001;
  door.scale.set(1, Math.max(0.0001, dIn), 1);
  const open = er(t, at(8, 0.34), at(8, 0.47)) * (1 - er(t, at(8, 0.72), at(8, 0.95)));
  panel.rotation.y = 1.45 * open;
  const fl = (tt) => (tt > 0 ? Math.exp(-tt * 2.2) * Math.sin(tt * 15) : 0);
  note.rotation.z = -0.45 * Math.abs(fl(t - at(8, 0.34))) - 0.18 * Math.abs(fl(t - at(8, 0.74)));
  const noteA = 1 - ramp(t, B(9) + 0.3, B(9) + 0.6);
  note.visible = noteA > 0.001 && t > B(8) - 0.1;
  note.scale.setScalar(Math.max(0.0001, noteA));

  // 写手机器人推门而过，再绕回来
  const wb = stW.bot;
  let pos = WR_REST, yaw = 0, walking = 0;
  const pIn = ramp(t, at(8, 0.05), at(8, 0.66)), pBack = ramp(t, B(9) + 0.2, at(10, 0.75));
  if (t > at(8, 0.05) && pBack <= 0) {
    const w = walkPath(PATH_IN, ease(pIn));
    pos = [w.x, w.z]; walking = pIn < 1 ? 1 : 0;
    yaw = yawTo(w.dx, w.dz);
    if (pIn >= 1) yaw = angLerp(yaw, Math.PI * 0.9, er(t, at(8, 0.66), at(8, 0.8)));
    const turnIn = ramp(t, at(8, 0.05), at(8, 0.12));
    yaw = angLerp(0, yaw, turnIn);
  } else if (pBack > 0) {
    const w = walkPath(PATH_BACK, ease(pBack));
    pos = [w.x, w.z]; walking = pBack < 1 ? 1 : 0;
    yaw = pBack < 1 ? yawTo(w.dx, w.dz) : 0;
    yaw = angLerp(Math.PI * 0.9, yaw, ramp(t, B(9) + 0.2, B(9) + 0.4));
    if (pBack > 0.92) yaw = angLerp(yaw, 0, ramp(pBack, 0.92, 1));
  }
  wb.g.position.set(pos[0] - stW.home.x + 0, 0, pos[1] - stW.home.z);
  wb.g.rotation.y = yaw;
  if (walking) { wb.body.position.y = 0.05 * Math.abs(Math.sin(t * 11)); wb.body.rotation.z = 0.05 * Math.sin(t * 11); } else wb.body.rotation.z = 0;

  // 第 10 句：检查闸门
  const gIn = er(t, B(10) - 0.2, B(10) + 0.5) * (1 - er(t, B(11) + 0.4, B(11) + 1.1));
  gate.visible = gIn > 0.001;
  gate.scale.set(1, Math.max(0.0001, gIn), 1);
  const gateOk = win(t, at(10, 0.3), at(10, 0.5), 0.05, 0.1), gateNo = win(t, at(10, 0.68), at(10, 1.0) + 0.3, 0.05, 0.2);
  beamMat.color.setHex(0xcfd7d3).lerp(new THREE.Color(C.accent), gateOk).lerp(new THREE.Color(0x39423f), gateNo);
  setSprite(okBadge, gateOk > 0 ? backOut(clamp(gateOk)) : 0);
  setSprite(noBadge, gateNo > 0 ? backOut(clamp(gateNo)) : 0);
  setSprite(gateSign, gIn, gIn);
  const docA = pop(t, B(10) + 0.1, 0.4);
  const dx1 = er(t, at(10, 0.06), at(10, 0.3)), dx2 = er(t, at(10, 0.4), at(10, 0.56)), drop = eIn(ramp(t, at(10, 0.56), at(10, 0.66)));
  docItem.visible = docA > 0.001 && drop < 1;
  docItem.scale.setScalar(Math.max(0.0001, docA));
  docItem.position.set(lerp(-6.1, -4.2, dx1) + lerp(0, 3.15, dx2), 0.06 - drop * 1.0, 3.9);
  const kA = pop(t, at(10, 0.34), 0.4), kx = er(t, at(10, 0.44), at(10, 0.68)), kb = eOut(ramp(t, at(10, 0.7), at(10, 0.86)));
  keyItem.visible = kA > 0.001 && t < B(11) + 0.6;
  keyItem.scale.setScalar(Math.max(0.0001, kA * (1 - ramp(t, B(11), B(11) + 0.5))));
  keyItem.position.set(lerp(-6.3, -4.65, kx) - kb * 0.7, 0.06 + Math.sin(Math.PI * kb) * 0.35, 3.9 + kb * 0.85);
  keyItem.rotation.y = kb * 0.9;

  // 第 11 句：单独的房间、单独的账号
  const iIn = er(t, B(11) - 0.1, at(11, 0.25));
  island.visible = iIn > 0.001;
  island.position.y = lerp(-10, 0, iIn);
  const mv = er(t, at(11, 0.08), at(11, 0.5));
  stF.g.position.set(lerp(5, 13.3, mv), Math.sin(Math.PI * mv) * 1.4 + island.position.y * (mv >= 1 ? 1 : 0), lerp(-0.8, -1.1, mv));
  const wallUp = er(t, at(11, 0.45), at(11, 0.72));
  roomWalls.visible = wallUp > 0.001;
  roomWalls.scale.set(1, Math.max(0.0001, wallUp), 1);
  const lockK = er(t, at(11, 0.78), at(11, 0.9));
  shackles.forEach((s) => (s.position.y = 0.11 + 0.08 * (1 - lockK)));
  lockBadge.position.set(10.15, 2.95, 0.8);
  setSprite(lockBadge, pop(t, at(11, 0.88), 0.4) * (1 - ramp(t, cutT - 0.4, cutT)));
  setCable(islandCable, eOut(ramp(t, at(11, 0.62), at(11, 0.95))));
  smallLed.color.setHex(C.accent).multiplyScalar(0.6 + 0.4 * (Math.sin(t * 6) > 0 ? 1 : 0.5));

  // 第 12 句：手接过键盘、自己登录
  const fb = stF.bot;
  const aside = er(t, cutT + 0.05, cutT + 0.55);
  fb.g.position.x = lerp(-0.55, -1.75, aside);
  fb.g.rotation.y = lerp(0, -0.9, aside) * (1 - ramp(t, cutT + 1.6, cutT + 2.2) * 0.4);
  const useLogin = t > cutT - 0.05 && t < B(13);
  stF.scrMat.map = useLogin ? login : finScreenTex;
  if (useLogin) {
    const typing = ramp(t, cutT + 0.85, cutT + 2.0);
    drawLogin(Math.round(typing * 8), t > cutT + 2.15);
  }
  const hIn = eOut(ramp(t, cutT + 0.2, cutT + 0.85));
  hand.visible = t > cutT + 0.15 && t < B(13);
  const kbW = stF.g.localToWorld(new THREE.Vector3(-0.15, 0.85, 0.12));
  hand.position.set(kbW.x + 0.12 + (1 - hIn) * 0.7, kbW.y + 0.05 + (1 - hIn) * 0.3, kbW.z + 0.1 + (1 - hIn) * 0.8);
  hand.rotation.set(0.12, 0.45, 0);
  const tapOn = t > cutT + 0.85 && t < cutT + 2.0;
  fingers.forEach((f, i) => (f.position.y = -0.03 + (tapOn ? 0.03 * Math.max(0, Math.sin(t * 22 + i * 1.7)) : 0)));
}

function renderAt(t) {
  update(t);
  placeCamera(t);
  renderer.render(scene, camera);
  ctx.clearRect(0, 0, W, H);
  ctx.drawImage(renderer.domElement, 0, 0);
  drawQuote(t);
  drawNotLock(t);
  drawChat(t);
  drawRules(t);
}

window.DURATION = DUR;
window.FRAMES = Math.round(DUR * FPS);
window.renderFrame = (n) => renderAt(n / FPS);
window.renderTime = (t) => renderAt(t);
window.frameDataURL = (type = 'image/png', q = 1) => out.toDataURL(type, q);
renderAt(0);
window.READY = true;
