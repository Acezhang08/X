import * as THREE from 'three';

// ---------- 参数 ----------
const W = 1920, H = 1080, FPS = 30, DURATION = 18;
const N = 5, PITCH = 10, BLOCK = 7, ROAD = 3, SLAB = 70;
const ORIGIN = -(N - 1) / 2 * PITCH;
const ROADLEN = N * PITCH + ROAD;
const roadLine = (k) => ORIGIN + (k - 0.5) * PITCH; // k = 0..N，道路中心线

const mulberry = (a) => () => {
  a |= 0; a = (a + 0x6d2b79f5) | 0;
  let t = Math.imul(a ^ (a >>> 15), 1 | a);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};
const pick = (R, arr) => arr[Math.floor(R() * arr.length)];

// ---------- 城市数据（左右共用同一份） ----------
function buildCityData() {
  const R = mulberry(20261009);
  const blocks = [], buildings = [];
  for (let i = 0; i < N; i++) {
    for (let j = 0; j < N; j++) {
      const cx = ORIGIN + i * PITCH, cz = ORIGIN + j * PITCH;
      let kind = 'houses';
      if (i === 2 && j === 2) kind = 'tower';
      else if (i === 3 && j === 1) kind = 'ferris';
      else if (i === 1 && j === 3) kind = 'pond';
      else if (R() < 0.12) kind = 'park';
      blocks.push({ i, j, cx, cz, kind });
      if (kind === 'tower') {
        buildings.push({ cx, cz, w: 5, d: 5, h: 12, tower: true, seed: 1 });
        continue;
      }
      if (kind !== 'houses') continue;
      const nx = R() < 0.55 ? 2 : 1, nz = R() < 0.55 ? 2 : 1;
      const gap = 0.4, lw = (6 - gap * (nx - 1)) / nx, ld = (6 - gap * (nz - 1)) / nz;
      const dist = Math.hypot(i - 2, j - 2);
      for (let a = 0; a < nx; a++) {
        for (let b = 0; b < nz; b++) {
          if (nx * nz > 1 && R() < 0.08) continue; // 空地
          const h = 2.2 + Math.max(0, 3.4 - dist) * 2.0 * (0.4 + R()) + R() * 2.2;
          buildings.push({
            cx: cx - 3 + lw / 2 + a * (lw + gap), cz: cz - 3 + ld / 2 + b * (ld + gap),
            w: lw, d: ld, h,
            gable: h < 8 && R() < 0.6, color: Math.floor(R() * 7), seed: Math.floor(R() * 1e9),
            ac: R() < 0.4, tank: R() < 0.2, chimney: R() < 0.3,
          });
        }
      }
    }
  }
  return { blocks, buildings };
}

// ---------- 左：免费版（雾、灰、低分辨率、只有方块） ----------
function buildLow(data) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xa9a9a6);
  scene.fog = new THREE.Fog(0xa9a9a6, 36, 150);
  scene.add(new THREE.HemisphereLight(0xdcdcd8, 0x77776f, 1.7));
  const sun = new THREE.DirectionalLight(0xffffff, 0.9);
  sun.position.set(-30, 40, 25);
  scene.add(sun);
  const gray = (l) => new THREE.MeshLambertMaterial({ color: new THREE.Color().setHSL(0, 0, l) });
  const top = new THREE.Mesh(new THREE.BoxGeometry(SLAB, 1, SLAB), gray(0.56));
  top.position.y = -0.5;
  scene.add(top);
  const earth = new THREE.Mesh(new THREE.CylinderGeometry(SLAB * 0.7071, 40, 4, 4, 1), gray(0.42));
  earth.rotation.y = Math.PI / 4;
  earth.position.y = -3;
  scene.add(earth);
  data.buildings.forEach((b, k) => {
    const h = b.tower ? 17 : b.h;
    const m = new THREE.Mesh(new THREE.BoxGeometry(b.w, h, b.d), gray(0.47 + ((k * 37) % 10) * 0.012));
    m.position.set(b.cx, h / 2, b.cz);
    scene.add(m);
  });
  return { scene, update() {} };
}

// ---------- 右：精细版 ----------
const WALL_COLORS = ['#e8d5b0', '#d9a98a', '#b9c4a5', '#f0e2c8', '#c98b6b', '#e6c07b', '#a9bcb4'];
const LIT = ['#ffc766', '#ffb347', '#ffe3a0'];

function windowTextures(cols, rows, seed) {
  const cw = 24, ch = 30;
  const mk = () => { const c = document.createElement('canvas'); c.width = cols * cw; c.height = rows * ch; return c; };
  const cm = mk(), ce = mk(), a = cm.getContext('2d'), b = ce.getContext('2d');
  a.fillStyle = '#fff'; a.fillRect(0, 0, cm.width, cm.height);
  b.fillStyle = '#000'; b.fillRect(0, 0, ce.width, ce.height);
  const R = mulberry(seed);
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const shop = r === rows - 1;
      const x = c * cw + (shop ? 3 : 5), y = r * ch + (shop ? 9 : 6), w = shop ? 18 : 14, h = shop ? 17 : 17;
      a.fillStyle = '#3a2e29'; a.fillRect(x, y, w, h);
      if (R() < (shop ? 0.8 : 0.42)) { b.fillStyle = pick(R, LIT); b.fillRect(x, y, w, h); }
    }
  }
  const t1 = new THREE.CanvasTexture(cm), t2 = new THREE.CanvasTexture(ce);
  [t1, t2].forEach((t) => { t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; });
  return [t1, t2];
}

function wallMat(color, width, height, seed) {
  const cols = Math.max(1, Math.round(width / 1.1)), rows = Math.max(1, Math.round(height / 1.4));
  const [map, em] = windowTextures(cols, rows, seed);
  return new THREE.MeshStandardMaterial({
    color, map, emissive: 0xffffff, emissiveMap: em, emissiveIntensity: 1.3, roughness: 0.9,
  });
}

function gableGeometry(w, d, rh, alongX) {
  const hw = w / 2, hd = d / 2;
  const A = [-hw, 0, -hd], B = [hw, 0, -hd], C = [hw, 0, hd], D = [-hw, 0, hd];
  const r1 = alongX ? [-hw, rh, 0] : [0, rh, -hd], r2 = alongX ? [hw, rh, 0] : [0, rh, hd];
  const tris = alongX
    ? [A, B, r2, A, r2, r1, D, r1, r2, D, r2, C, A, r1, D, B, C, r2]
    : [A, r1, r2, A, r2, D, B, C, r2, B, r2, r1, A, B, r1, D, r2, C];
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(tris.flat(), 3));
  g.computeVertexNormals();
  return g;
}

function buildHigh(data) {
  const scene = new THREE.Scene();
  const anim = [];
  const R = mulberry(555);

  // 天空：暖橙到奶油的渐变 + 太阳方向的光晕（不用紫蓝）
  const sunDir = new THREE.Vector3(-30, 22, 25).normalize();
  const sky = new THREE.Mesh(
    new THREE.SphereGeometry(500, 24, 16),
    new THREE.ShaderMaterial({
      side: THREE.BackSide, depthWrite: false, fog: false,
      uniforms: { sunDir: { value: sunDir } },
      vertexShader: 'varying vec3 vD; void main(){ vD = normalize(position); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.0); }',
      fragmentShader: `varying vec3 vD; uniform vec3 sunDir;
        void main(){
          float y = vD.y;
          vec3 hor = vec3(1.0,0.84,0.62), up = vec3(0.93,0.55,0.34), low = vec3(0.98,0.70,0.46);
          vec3 c = y > 0.0 ? mix(hor, up, pow(y, 0.6)) : mix(hor, low, pow(-y, 0.5));
          c += vec3(1.0,0.75,0.45) * pow(max(dot(vD, sunDir), 0.0), 6.0) * 0.5;
          gl_FragColor = vec4(c, 1.0); }`,
    })
  );
  scene.add(sky);
  scene.fog = new THREE.Fog(0xffd7a3, 110, 330);
  scene.add(new THREE.HemisphereLight(0xfff0d8, 0x8a9a68, 1.9));
  const sun = new THREE.DirectionalLight(0xffc088, 3.2);
  sun.position.copy(sunDir).multiplyScalar(80);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -45, right: 45, top: 45, bottom: -45, near: 10, far: 200 });
  sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.05;
  scene.add(sun);

  const std = (color, extra = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.9, flatShading: true, ...extra });
  const add = (geo, mat, x, y, z, shadow = true) => {
    const m = new THREE.Mesh(geo, mat);
    m.position.set(x, y, z); m.castShadow = shadow; m.receiveShadow = true;
    scene.add(m); return m;
  };

  // 地面
  add(new THREE.BoxGeometry(SLAB, 1, SLAB), std('#86a463'), 0, -0.5, 0, false);
  const earth = add(new THREE.CylinderGeometry(SLAB * 0.7071, 40, 4, 4, 1), std('#7a5a3e'), 0, -3, 0, false);
  earth.rotation.y = Math.PI / 4;

  // 路
  const roadMat = std('#4d4843');
  for (let k = 0; k <= N; k++) {
    add(new THREE.BoxGeometry(ROADLEN, 0.06, ROAD), roadMat, 0, 0.03, roadLine(k), false);
    add(new THREE.BoxGeometry(ROAD, 0.06, ROADLEN), roadMat, roadLine(k), 0.03, 0, false);
  }
  // 车道虚线（实例化）
  const dashes = [];
  for (let k = 0; k <= N; k++) {
    for (let s = -ROADLEN / 2 + 1.5; s < ROADLEN / 2 - 1; s += 2.5) {
      const nearCross = [...Array(N + 1).keys()].some((q) => Math.abs(s - roadLine(q)) < 2.2);
      if (nearCross) continue;
      dashes.push([s, roadLine(k), 0], [roadLine(k), s, 1]);
    }
  }
  const dashMesh = new THREE.InstancedMesh(new THREE.BoxGeometry(1.1, 0.02, 0.12), std('#e9d8a0'), dashes.length);
  const dm = new THREE.Object3D();
  dashes.forEach(([x, z, v], n) => {
    dm.position.set(x, 0.07, z); dm.rotation.y = v ? Math.PI / 2 : 0; dm.updateMatrix();
    dashMesh.setMatrixAt(n, dm.matrix);
  });
  dashMesh.receiveShadow = true;
  scene.add(dashMesh);

  // 街区底座 / 公园
  const walk = std('#d8cdb8'), grass = std('#8cab62');
  for (const b of data.blocks) {
    if (b.kind === 'houses' || b.kind === 'tower') add(new THREE.BoxGeometry(BLOCK, 0.2, BLOCK), walk, b.cx, 0.1, b.cz, false);
    else add(new THREE.BoxGeometry(BLOCK, 0.25, BLOCK), grass, b.cx, 0.125, b.cz, false);
    if (b.kind === 'pond') {
      const w = add(new THREE.CylinderGeometry(2.3, 2.3, 0.1, 8), std('#6aa6a0', { roughness: 0.25, flatShading: true }), b.cx, 0.27, b.cz, false);
      anim.push((t) => { w.material.emissive.setRGB(0.05 + 0.03 * Math.sin(t * 2), 0.09 + 0.03 * Math.sin(t * 2), 0.08); });
    }
  }

  // 房子
  const roofColors = ['#c4623f', '#9a6650', '#85807a'], flatRoof = std('#b3a99b');
  const smokers = [];
  for (const b of data.buildings) {
    if (b.tower) { buildTower(b); continue; }
    const mx = wallMat(WALL_COLORS[b.color], b.d, b.h, b.seed), mz = wallMat(WALL_COLORS[b.color], b.w, b.h, b.seed + 1);
    const box = new THREE.Mesh(new THREE.BoxGeometry(b.w, b.h, b.d), [mx, mx, flatRoof, flatRoof, mz, mz]);
    box.position.set(b.cx, b.h / 2, b.cz); box.castShadow = box.receiveShadow = true;
    scene.add(box);
    if (b.gable) {
      const rh = Math.min(b.w, b.d) * 0.45;
      const roof = add(gableGeometry(b.w * 1.08, b.d * 1.08, rh, b.w >= b.d), std(roofColors[b.seed % 3]), b.cx, b.h, b.cz);
      if (b.chimney) {
        add(new THREE.BoxGeometry(0.4, 1.2, 0.4), std('#7a6a5e'), b.cx + b.w * 0.25, b.h + rh * 0.6, b.cz);
        smokers.push([b.cx + b.w * 0.25, b.h + rh * 0.6 + 1.2, b.cz]);
      }
    } else {
      if (b.ac) add(new THREE.BoxGeometry(0.9, 0.5, 0.7), std('#b9b2a6'), b.cx - b.w * 0.2, b.h + 0.25, b.cz + b.d * 0.15);
      if (b.tank) {
        add(new THREE.CylinderGeometry(0.4, 0.4, 0.8, 7), std('#9a7d5a'), b.cx + b.w * 0.2, b.h + 0.4, b.cz - b.d * 0.15);
      }
    }
  }
  function buildTower(b) {
    const tiers = [[5, 12, 5], [3.6, 5, 3.6], [2.2, 3, 2.2]];
    let y = 0;
    tiers.forEach(([w, h, d], n) => {
      const mx = wallMat('#e6d3ae', d, h, b.seed + n), mz = wallMat('#e6d3ae', w, h, b.seed + n + 9);
      const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), [mx, mx, flatRoof, flatRoof, mz, mz]);
      m.position.set(b.cx, y + h / 2, b.cz); m.castShadow = m.receiveShadow = true;
      scene.add(m); y += h;
    });
    add(new THREE.ConeGeometry(1.2, 3, 4), std('#b5532f'), b.cx, y + 1.5, b.cz).rotation.y = Math.PI / 4;
    add(new THREE.CylinderGeometry(0.04, 0.04, 1.4, 4), std('#444'), b.cx, y + 3.7, b.cz, false);
    const beacon = add(new THREE.SphereGeometry(0.18, 8, 6), new THREE.MeshBasicMaterial({ color: 0xff3b2a }), b.cx, y + 4.4, b.cz, false);
    anim.push((t) => { beacon.material.color.setRGB(1, 0.23, 0.16).multiplyScalar(0.25 + 0.75 * (Math.sin(t * 5) > 0.2 ? 1 : 0)); });
  }

  // 摩天轮
  const fb = data.blocks.find((q) => q.kind === 'ferris');
  const wheel = new THREE.Group();
  wheel.position.set(fb.cx, 4.4, fb.cz);
  const wr = 3.3, frame = std('#e9e1d0');
  const ring = new THREE.Mesh(new THREE.TorusGeometry(wr, 0.1, 4, 18), frame);
  wheel.add(ring);
  const cabinColors = ['#d94f3d', '#e8b53a', '#3f7f6b', '#c87b3a'];
  const cabins = [];
  for (let n = 0; n < 10; n++) {
    const a = (n / 10) * Math.PI * 2;
    const spoke = new THREE.Mesh(new THREE.BoxGeometry(wr, 0.06, 0.06), frame);
    spoke.position.set(Math.cos(a) * wr / 2, Math.sin(a) * wr / 2, 0); spoke.rotation.z = a;
    wheel.add(spoke);
    const pivot = new THREE.Group(); // 挂点：随轮转，自身反向转，吊舱始终朝下
    pivot.position.set(Math.cos(a) * wr, Math.sin(a) * wr, 0);
    const cab = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.5, 0.6), std(cabinColors[n % 4]));
    cab.position.y = -0.35;
    pivot.add(cab); wheel.add(pivot); cabins.push(pivot);
  }
  wheel.traverse((m) => { m.castShadow = true; });
  scene.add(wheel);
  for (const s of [-1, 1]) {
    const leg = add(new THREE.BoxGeometry(0.18, 5, 0.18), frame, fb.cx + s * 0.9, 2.1, fb.cz + 0.35 * 0, true);
    leg.rotation.z = -s * 0.28; leg.position.x = fb.cx + s * 1.0;
  }
  anim.push((t) => {
    wheel.rotation.z = -t * 0.25;
    cabins.forEach((p) => { p.rotation.z = t * 0.25; });
  });

  // 树（实例化）
  const trees = [];
  for (const b of data.blocks) {
    if (b.kind === 'park' || b.kind === 'ferris' || b.kind === 'pond') {
      const n = b.kind === 'park' ? 8 : 5;
      for (let q = 0; q < n; q++) {
        const x = b.cx + (R() - 0.5) * 6, z = b.cz + (R() - 0.5) * 6;
        if (b.kind === 'pond' && Math.hypot(x - b.cx, z - b.cz) < 2.8) continue;
        if (b.kind === 'ferris' && Math.abs(x - b.cx) < 2.2 && Math.abs(z - b.cz) < 1.5) continue;
        trees.push({ x, z, y: 0.25, s: 0.8 + R() * 0.7, pine: R() < 0.35 });
      }
    } else if (b.kind === 'houses') {
      for (let e = -3; e <= 3; e += 2) {
        if (R() < 0.18) trees.push({ x: b.cx + e, z: b.cz + (R() < 0.5 ? -3.3 : 3.3), y: 0.2, s: 0.55, pine: false });
        if (R() < 0.18) trees.push({ x: b.cx + (R() < 0.5 ? -3.3 : 3.3), z: b.cz + e, y: 0.2, s: 0.55, pine: false });
      }
    }
  }
  for (let q = 0; q < 36; q++) { // 外圈
    const a = R() * Math.PI * 2, r = 28.5 + R() * 5;
    const x = Math.cos(a) * r * 1.0, z = Math.sin(a) * r * 1.0;
    if (Math.abs(x) > 33 || Math.abs(z) > 33) continue;
    trees.push({ x, z, y: 0, s: 0.9 + R() * 0.9, pine: R() < 0.5 });
  }
  const treeColors = ['#5f8b4a', '#7ba05b', '#4c7a46', '#d28a3a', '#6b9a52'];
  const trunkM = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.1, 0.15, 1, 5), std('#6b4a32'), trees.length);
  const roundM = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(0.85, 0), std('#fff'), trees.length);
  const pineM = new THREE.InstancedMesh(new THREE.ConeGeometry(0.8, 2.1, 6), std('#fff'), trees.length);
  [trunkM, roundM, pineM].forEach((m) => { m.castShadow = true; m.receiveShadow = true; scene.add(m); });
  const o = new THREE.Object3D(), hide = new THREE.Matrix4().makeScale(0, 0, 0);
  trees.forEach((t, n) => {
    t.phase = R() * 6.28;
    const col = new THREE.Color(t.pine ? '#3f6e48' : treeColors[Math.floor(R() * treeColors.length)]);
    (t.pine ? pineM : roundM).setColorAt(n, col);
    o.position.set(t.x, t.y + 0.5 * t.s, t.z); o.rotation.set(0, 0, 0); o.scale.set(t.s, t.s, t.s); o.updateMatrix();
    trunkM.setMatrixAt(n, o.matrix);
  });
  anim.push((time) => {
    trees.forEach((t, n) => {
      o.position.set(t.x, t.y + (t.pine ? 1.5 : 1.35) * t.s, t.z);
      o.rotation.set(0, t.phase, Math.sin(time * 1.4 + t.phase) * 0.05);
      o.scale.set(t.s, t.s, t.s); o.updateMatrix();
      if (t.pine) { pineM.setMatrixAt(n, o.matrix); roundM.setMatrixAt(n, hide); }
      else { roundM.setMatrixAt(n, o.matrix); pineM.setMatrixAt(n, hide); }
    });
    roundM.instanceMatrix.needsUpdate = pineM.instanceMatrix.needsUpdate = true;
  });

  // 远景小山
  for (const [sx, sz, r, h] of [[-31.5, -31.5, 3.8, 3.4], [31.5, -31.5, 3.2, 2.6], [-31.5, 31.5, 3.4, 3], [31.5, 31.5, 3.9, 3.6]]) {
    add(new THREE.ConeGeometry(r, h, 6), std('#7d9a58'), sx, h / 2, sz);
  }

  // 路灯 + 光晕
  const glowTex = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 64;
    const g = c.getContext('2d'), gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr.addColorStop(0, 'rgba(255,214,140,1)'); gr.addColorStop(0.3, 'rgba(255,190,100,0.45)'); gr.addColorStop(1, 'rgba(255,170,80,0)');
    g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
    return new THREE.CanvasTexture(c);
  })();
  const lampHead = new THREE.MeshBasicMaterial({ color: 0xffe2a0 });
  for (let a = 0; a <= N; a++) {
    for (let b = 0; b <= N; b++) {
      if ((a + b) % 2) continue;
      const x = roadLine(a) + 1.9, z = roadLine(b) + 1.9;
      add(new THREE.CylinderGeometry(0.05, 0.07, 2.2, 5), std('#3a3631'), x, 1.1, z);
      add(new THREE.SphereGeometry(0.16, 6, 5), lampHead, x, 2.3, z, false);
      const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, fog: false, transparent: true, opacity: 0.85 }));
      sp.scale.set(2.6, 2.6, 1); sp.position.set(x, 2.3, z);
      scene.add(sp);
    }
  }

  // 车
  const cars = [];
  for (let k = 0; k <= N; k++) {
    for (const lane of [-0.7, 0.7]) {
      for (let q = 0; q < 2; q++) {
        cars.push({ axis: 0, line: roadLine(k), lane, dir: lane > 0 ? 1 : -1, speed: 2.6 + R() * 2, ph: R() * ROADLEN, col: Math.floor(R() * 6) });
        if (R() < 0.7) cars.push({ axis: 1, line: roadLine(k), lane, dir: lane > 0 ? -1 : 1, speed: 2.6 + R() * 2, ph: R() * ROADLEN, col: Math.floor(R() * 6) });
      }
    }
  }
  const carColors = ['#d94f3d', '#e8b53a', '#f2efe6', '#3f7f6b', '#c87b3a', '#2e2e2e'];
  const bodyM = new THREE.InstancedMesh(new THREE.BoxGeometry(1.5, 0.45, 0.75), std('#fff'), cars.length);
  const cabM = new THREE.InstancedMesh(new THREE.BoxGeometry(0.8, 0.35, 0.65), std('#2d2926'), cars.length);
  [bodyM, cabM].forEach((m) => { m.castShadow = true; scene.add(m); });
  cars.forEach((c, n) => bodyM.setColorAt(n, new THREE.Color(carColors[c.col])));
  const co = new THREE.Object3D();
  anim.push((t) => {
    cars.forEach((c, n) => {
      const s = (((c.ph + c.speed * t) % ROADLEN) + ROADLEN) % ROADLEN;
      const along = c.dir * (s - ROADLEN / 2);
      const edge = Math.min(s, ROADLEN - s), sc = Math.min(1, edge / 2); // 路尽头缩小消失，避免突然弹出
      const x = c.axis === 0 ? along : c.line + c.lane, z = c.axis === 0 ? c.line + c.lane : along;
      co.rotation.set(0, (c.axis === 0 ? 0 : Math.PI / 2) + (c.dir > 0 ? 0 : Math.PI), 0);
      co.scale.setScalar(sc);
      co.position.set(x, 0.3 * sc, z); co.updateMatrix(); bodyM.setMatrixAt(n, co.matrix);
      co.translateY(0.4); cabM.setMatrixAt(n, (co.updateMatrix(), co.matrix));
    });
    bodyM.instanceMatrix.needsUpdate = cabM.instanceMatrix.needsUpdate = true;
  });

  // 烟
  const puffMat = new THREE.MeshBasicMaterial({ color: 0xf3ece0, transparent: true, depthWrite: false });
  const puffs = [];
  smokers.slice(0, 6).forEach(([x, y, z], s) => {
    for (let q = 0; q < 4; q++) {
      const m = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 0), puffMat.clone());
      scene.add(m); puffs.push({ m, x, y, z, q, s });
    }
  });
  anim.push((t) => {
    puffs.forEach(({ m, x, y, z, q, s }) => {
      const age = (t * 0.45 + q / 4 + s * 0.13) % 1;
      m.position.set(x + age * 1.2, y + age * 3, z); m.scale.setScalar(0.2 + age * 0.55);
      m.material.opacity = (1 - age) * 0.7;
    });
  });

  // 鸟
  const wingGeo = new THREE.BufferGeometry();
  wingGeo.setAttribute('position', new THREE.Float32BufferAttribute([0, 0, 0, -0.5, 0, 0.12, -0.15, 0, -0.25], 3));
  wingGeo.computeVertexNormals();
  const birdMat = new THREE.MeshBasicMaterial({ color: 0x3a302a, side: THREE.DoubleSide });
  const birds = [];
  for (let q = 0; q < 8; q++) {
    const g = new THREE.Group(), l = new THREE.Mesh(wingGeo, birdMat), r = new THREE.Mesh(wingGeo, birdMat);
    r.scale.x = -1; g.add(l, r); scene.add(g);
    birds.push({ g, l, r, rad: 15 + R() * 8, ph: R() * 6.28, hy: 14 + R() * 5, sp: 0.22 + R() * 0.08 });
  }
  anim.push((t) => {
    birds.forEach((b) => {
      const a = b.ph + t * b.sp;
      b.g.position.set(Math.cos(a) * b.rad, b.hy + Math.sin(t * 0.7 + b.ph), Math.sin(a) * b.rad);
      b.g.rotation.y = -a;
      const f = Math.sin(t * 9 + b.ph) * 0.6;
      b.l.rotation.z = f; b.r.rotation.z = -f;
    });
  });

  // 云：绕着浮岛缓慢漂
  const clouds = new THREE.Group();
  const cloudMat = new THREE.MeshStandardMaterial({ color: '#fff1dc', emissive: '#ffd9a8', emissiveIntensity: 0.35, roughness: 1, flatShading: true });
  for (let q = 0; q < 9; q++) {
    const c = new THREE.Group(), a = (q / 9) * Math.PI * 2 + R(), rad = 52 + R() * 22;
    for (let p = 0; p < 3; p++) {
      const m = new THREE.Mesh(new THREE.IcosahedronGeometry(2.4 + R() * 1.4, 0), cloudMat);
      m.scale.set(1.6, 0.7, 1); m.position.set(p * 3 - 3, R() * 0.8, R() * 1.5);
      c.add(m);
    }
    c.position.set(Math.cos(a) * rad, -2 + R() * 8, Math.sin(a) * rad); c.rotation.y = -a;
    clouds.add(c);
  }
  scene.add(clouds);
  anim.push((t) => { clouds.rotation.y = t * 0.012; });

  return { scene, update(t) { anim.forEach((f) => f(t)); } };
}

// ---------- 合成 ----------
const data = buildCityData();
const low = buildLow(data);
const high = buildHigh(data);

const renderer = new THREE.WebGLRenderer({ antialias: false, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(W, H);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

const LOW_W = 480, LOW_H = 540; // 左边只渲染 1/4 像素再放大 → 糊
const rtLow = new THREE.WebGLRenderTarget(LOW_W, LOW_H, { type: THREE.HalfFloatType, samples: 0 });
const rtHigh = new THREE.WebGLRenderTarget(W / 2, H, { type: THREE.HalfFloatType, samples: 4 });

const cam = new THREE.PerspectiveCamera(36, (W / 2) / H, 1, 600);

const quadScene = new THREE.Scene();
const quadCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
const mix = new THREE.ShaderMaterial({
  uniforms: { tL: { value: rtLow.texture }, tR: { value: rtHigh.texture }, uFade: { value: 1 }, uTime: { value: 0 } },
  vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }',
  fragmentShader: `varying vec2 vUv; uniform sampler2D tL, tR; uniform float uFade, uTime;
    void main(){
      vec2 uv = vUv; vec4 c;
      if (uv.x < 0.5) {
        c = texture2D(tL, vec2(uv.x * 2.0, uv.y));
        float g = dot(c.rgb, vec3(0.299, 0.587, 0.114));
        c.rgb = mix(vec3(g), c.rgb, 0.3);
        float n = fract(sin(dot(uv * vec2(1920.0, 1080.0) + uTime * 37.0, vec2(12.9898, 78.233))) * 43758.5453);
        c.rgb += (n - 0.5) * 0.04;
      } else {
        c = texture2D(tR, vec2((uv.x - 0.5) * 2.0, uv.y));
        c.rgb *= 1.0 - 0.18 * pow(length(uv - vec2(0.75, 0.5)) * 1.3, 2.0);
      }
      float line = smoothstep(2.5, 1.5, abs(uv.x - 0.5) * 1920.0);
      c.rgb = mix(c.rgb, vec3(0.05, 0.045, 0.04), line);
      c.rgb *= uFade;
      gl_FragColor = vec4(c.rgb, 1.0);
      #include <colorspace_fragment>
    }`,
});
const quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), mix);
quadScene.add(quad);

function renderAt(t) {
  const u = t / DURATION, e = u * u * (3 - 2 * u) * 0.35 + u * 0.65;
  const ang = THREE.MathUtils.degToRad(-40 + 85 * e);
  const el = THREE.MathUtils.degToRad(29 + 3 * Math.sin(u * Math.PI)), r = 86;
  cam.position.set(Math.sin(ang) * Math.cos(el) * r, Math.sin(el) * r + 2, Math.cos(ang) * Math.cos(el) * r);
  cam.lookAt(0, 3, 0);

  low.scene.fog.far = 150 - 35 * u; // 左边：雾随时间越来越浓（“正在变差”）
  high.update(t);

  renderer.setRenderTarget(rtLow); renderer.render(low.scene, cam);
  renderer.setRenderTarget(rtHigh); renderer.render(high.scene, cam);
  renderer.setRenderTarget(null);
  const s = (x) => Math.min(1, Math.max(0, x)), f = (x) => x * x * (3 - 2 * x);
  mix.uniforms.uFade.value = f(s(t / 0.7)) * f(s((DURATION - t) / 0.7));
  mix.uniforms.uTime.value = t;
  renderer.render(quadScene, quadCam);
}

window.CFG = { W, H, FPS, DURATION, FRAMES: FPS * DURATION };
window.renderFrame = (n) => renderAt(n / FPS);
window.frameDataURL = (type = 'image/png', q = 1) => renderer.domElement.toDataURL(type, q);
window.READY = true;
