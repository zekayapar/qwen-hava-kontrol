```js
import { createGame, setRoute, tick, serialize, deserialize } from './engine.js';

const $ = id => document.getElementById(id);
const cv = $('radar'), ctx = cv.getContext('2d');
const W = 1000, H = 700, DPR = Math.min(2, window.devicePixelRatio || 1);
const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const SAVE_KEY = 'qwen-kule-save-v1';
const TYPE = { light: { c: '#5fe08a', n: 'Hafif' }, medium: { c: '#ffb020', n: 'Orta' }, heavy: { c: '#ff5a4d', n: 'Ağır' } };
const CALL = ['TK','AF','LH','DL','BA','EK','TH','SK','RJ','KL'];

let g = null, playing = false, sel = null, speed = 1, last = 0, uiAcc = 0, raf = 0;
let drag = null, dragPts = [], dragMoved = false;
let err = '';

function fit() {
  const r = cv.getBoundingClientRect();
  cv.width = Math.max(1, Math.round(r.width * DPR));
  cv.height = Math.max(1, Math.round(r.height * DPR));
}
function toLocal(e) {
  const r = cv.getBoundingClientRect();
  return { x: (e.clientX - r.left) / r.width * W, y: (e.clientY - r.top) / r.height * H };
}
function dist(a, b) { return Math.hypot(a.x - b.x, a.y - b.y); }
function nearest(p, pts) { let m = 1e9, i = 0; for (let k = 0; k < pts.length; k++) { const d = dist(p, pts[k]); if (d < m) { m = d; i = k; } } return i; }
function headingTo(a, b) { return Math.atan2(b.y - a.y, b.x - a.x); }
function fmt(t) { const m = Math.floor(t / 60), s = Math.floor(t % 60); return m + ':' + String(s).padStart(2, '0'); }

function setErr(m) { err = m; $('status').textContent = m || 'Hazır'; $('status').classList.toggle('err', !!m); }

function startGame(seed, diff) {
  g = createGame(seed, diff);
  g.paused = true; sel = null; speed = 1;
  $('speedSelect').value = '1';
  $('startOverlay').hidden = true; $('endOverlay').hidden = true;
  playing = true; last = 0; uiAcc = 0;
  setErr(''); updateUI();
}

function restart() {
  startGame(parseInt($('seedInput').value, 10) || 0, $('difficulty').value);
}

function doSave() {
  try { localStorage.setItem(SAVE_KEY, serialize(g)); setErr('Kaydedildi.'); }
  catch (e) { setErr('Kaydetme hatası: ' + e.message); }
}
function doLoad() {
  try {
    const raw = localStorage.getItem(SAVE_KEY); if (!raw) { setErr('Kayıt yok.'); return; }
    const s = deserialize(raw);
    if (!s || !s.planes || !s.runways) throw new Error('geçersiz veri');
    g = s; g.paused = true; sel = null; playing = true; last = 0; uiAcc = 0;
    $('startOverlay').hidden = true; $('endOverlay').hidden = true;
    setErr('Yüklendi (duraklatıldı).'); updateUI();
  } catch (e) { setErr('Yükleme hatası: ' + e.message); }
}
function doExport() {
  try {
    const blob = new Blob([serialize(g)], { type: 'application/json' });
    const url = URL.createObjectURL(blob), a = document.createElement('a');
    a.href = url; a.download = 'zeka-kule.json'; a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000); setErr('Dışa aktarıldı.');
  } catch (e) { setErr('Dışa aktarma hatası: ' + e.message); }
}
function doImport() { $('fileInput').click(); }
function onFile(e) {
  const f = e.target.files[0]; e.target.value = '';
  if (!f) return;
  if (f.size > 100 * 1024) { setErr('Dosya çok büyük (max 100KB).'); return; }
  const rd = new FileReader();
  rd.onload = () => {
    try {
      const s = deserialize(String(rd.result));
      if (!s || !s.planes || !s.runways) throw new Error('geçersiz veri');
      g = s; g.paused = true; sel = null; playing = true; last = 0; uiAcc = 0;
      $('startOverlay').hidden = true; $('endOverlay').hidden = true;
      setErr('İçe aktarıldı (duraklatıldı).'); updateUI();
    } catch (ex) { setErr('İçe aktarma hatası: ' + ex.message); }
  };
  rd.onerror = () => setErr('Dosya okunamadı.');
  rd.readAsText(f);
}

function togglePause() {
  if (!playing) return;
  g.paused = !g.paused;
  $('pauseBtn').textContent = g.paused ? '▶ Devam Et' : '⏸ Duraklat';
  updateUI();
}

function approach() {
  if (!g || !sel) return;
  const p = g.planes.find(x => x.id === sel); if (!p) return;
  const rw = g.runways.find(r => r.accepts.includes(p.type) && !r.closed);
  if (!rw) { setErr('Uygun açık pist yok.'); return; }
  const h = rw.heading, cx = Math.cos(h), cy = Math.sin(h);
  const pts = [{ x: rw.x - 60 * cx, y: rw.y - 60 * cy }, { x: rw.x, y: rw.y }, { x: rw.x + 60 * cx, y: rw.y + 60 * cy }];
  if (setRoute(g, p.id, pts)) { setErr('Yaklaşma rotası çizildi.'); updateUI(); }
  else setErr('Rota çizilemedi.');
}

function selectPlane(id) { sel = id; updateUI(); }

function onPointerDown(e) {
  if (!playing || g.paused || g.over) return;
  const p = toLocal(e);
  let best = null, bd = 26;
  for (const pl of g.planes) { const d = dist(p, pl); if (d < bd) { bd = d; best = pl; } }
  if (best) {
    sel = best.id;
    drag = { id: best.id }; dragPts = [{ x: p.x, y: p.y }]; dragMoved = false;
    try { cv.setPointerCapture(e.pointerId); } catch (_) {}
    updateUI();
  }
}
function onPointerMove(e) {
  if (!drag) return;
  const p = toLocal(e);
  if (dist(p, dragPts[0]) > 4) dragMoved = true;
  if (dragPts.length < 100) dragPts.push({ x: p.x, y: p.y });
}
function onPointerUp(e) {
  if (!drag) return;
  try { cv.releasePointerCapture(e.pointerId); } catch (_) {}
  if (dragMoved && dragPts.length > 1) {
    const pts = dragPts.filter((pt, i) => i === 0 || dist(pt, dragPts[i - 1]) > 6);
    if (setRoute(g, drag.id, pts)) setErr('Rota çizildi (' + pts.length + ' nokta).');
    else setErr('Rota çizilemedi.');
  }
  drag = null; dragPts = []; updateUI();
}
function onPointerCancel(e) {
  try { cv.releasePointerCapture(e.pointerId); } catch (_) {}
  drag = null; dragPts = [];
}

function onKey(e) {
  const t = e.target;
  if (t && (t.tagName === 'INPUT' || t.tagName === 'SELECT' || t.tagName === 'TEXTAREA')) return;
  if (!playing) return;
  const k = e.key;
  if (k === 'p' || k === 'P') { e.preventDefault(); togglePause(); }
  else if (k === 'r' || k === 'R') { e.preventDefault(); restart(); }
  else if (k === '1') { speed = 1; $('speedSelect').value = '1'; }
  else if (k === '2') { speed = 2; $('speedSelect').value = '2'; }
  else if (k === '4') { speed = 4; $('speedSelect').value = '4'; }
  else if (k === 'Escape') { if (sel) { setRoute(g, sel, []); setErr('Rota temizlendi.'); updateUI(); } }
  else if (k === 'Enter') { e.preventDefault(); approach(); }
}

function loop(ts) {
  raf = requestAnimationFrame(loop);
  if (!last) last = ts;
  let dt = (ts - last) / 1000; last = ts;
  if (dt > 0.1) dt = 0.1;
  if (playing && g && !g.paused && !g.over) {
    const steps = speed;
    for (let i = 0; i < steps; i++) tick(g, dt);
    uiAcc += dt;
    if (uiAcc >= 0.25) { uiAcc = 0; updateUI(); }
    if (g.over) { playing = false; showEnd(); }
  }
  render();
}

function showEnd() {
  $('endSummary').textContent =
    'Skor: ' + g.score + ' · İniş: ' + g.landed + ' · Kayıp: ' + g.lost + ' · Olay: ' + g.incidents + ' · Süre: ' + fmt(g.time);
  $('endOverlay').hidden = false;
  $('pauseBtn').textContent = '⏸ Duraklat';
}

function updateUI() {
  if (!g) return;
  const st = $('stats');
  st.innerHTML = '';
  const items = [['Skor', g.score], ['İniş', g.landed], ['Kayıp', g.lost], ['Olay', g.incidents], ['Süre', fmt(g.time)], ['Uçak', g.planes.length]];
  for (const [l, v] of items) {
    const d = document.createElement('div'); d.className = 'stat';
    const b = document.createElement('b'); b.textContent = v;
    const s = document.createElement('span'); s.textContent = l;
    d.appendChild(b); d.appendChild(s); st.appendChild(d);
  }
  $('weather').textContent = 'Rüzgar ' + Math.round(g.weather.wind) + '°' + (g.weather.storm ? ' · ⛈ FIRTINA' : ' · Açık');
  const rw = $('runways'); rw.innerHTML = '';
  for (const r of g.runways) {
    const li = document.createElement('li');
    li.textContent = r.name + ' · ' + (r.closed ? 'KAPALI' : (r.busySeconds > 0 ? 'MEŞGUL ' + Math.ceil(r.busySeconds) + 's' : 'AÇIK')) + ' · ' + r.accepts.map(t => TYPE[t].n).join('/');
    rw.appendChild(li);
  }
  const pl = $('planes'); pl.innerHTML = '';
  for (const p of g.planes) {
    const li = document.createElement('li');
    if (p.id === sel) li.className = 'sel';
    const a = document.createElement('span'); a.textContent = 'Uçak' + p.id + ' ' + TYPE[p.type].n;
    const b = document.createElement('span'); b.textContent = Math.round(p.fuel) + '%';
    li.appendChild(a); li.appendChild(b);
    li.addEventListener('click', () => selectPlane(p.id));
    pl.appendChild(li);
  }
  const selBox = $('selected'); selBox.innerHTML = '';
  const p = g.planes.find(x => x.id === sel);
  if (p) {
    const rows = [['Çağrı', CALL[p.id % CALL.length] + p.id], ['Tür', TYPE[p.type].n], ['Hız', Math.round(p.speed)], ['Yakıt', Math.round(p.fuel) + '%'], ['Rota', p.route.length + ' nokta']];
    for (const [k, v] of rows) {
      const d = document.createElement('div');
      const kk = document.createElement('span'); kk.className = 'k'; kk.textContent = k + ': ';
      const vv = document.createElement('span'); vv.textContent = v;
      d.appendChild(kk); d.appendChild(vv); selBox.appendChild(d);
    }
  } else {
    const s = document.createElement('span'); s.className = 'k'; s.textContent = 'Uçak seçilmedi.'; selBox.appendChild(s);
  }
  const wr = $('warnings'); wr.innerHTML = '';
  for (const w of g.warnings) {
    const li = document.createElement('li');
    if (w.dist < 40) li.className = 'bad';
    li.textContent = 'Uçak' + w.a + ' ↔ Uçak' + w.b + ' · ' + Math.round(w.dist) + ' birim';
    wr.appendChild(li);
  }
  const ev = $('events'); ev.innerHTML = '';
  const evs = g.events.slice(-6).reverse();
  for (const e of evs) {
    const li = document.createElement('li');
    li.textContent = fmt(e.time) + ' · ' + e.text;
    ev.appendChild(li);
  }
  $('clearRouteBtn').disabled = !sel;
  $('approachBtn').disabled = !sel;
  if (g.paused && !g.over) $('pauseBtn').textContent = '▶ Devam Et';
  else if (!g.over) $('pauseBtn').textContent = '⏸ Duraklat';
}

function drawRunway(r) {
  const h = r.heading, cx = Math.cos(h), cy = Math.sin(h);
  const len = 120, w = 14;
  ctx.save();
  ctx.translate(r.x, r.y); ctx.rotate(h);
  ctx.fillStyle = r.closed ? '#3a2020' : '#12303a';
  ctx.fillRect(-len / 2, -w / 2, len, w);
  ctx.strokeStyle = r.closed ? '#ff5a4d' : '#37e0e8'; ctx.lineWidth = 1.5;
  ctx.strokeRect(-len / 2, -w / 2, len, w);
  ctx.fillStyle = '#d7f0f4';
  for (let i = -3; i <= 3; i++) ctx.fillRect(i * 14 - 1, -w / 2 + 2, 2, w - 4);
  ctx.restore();
  // approach arrows (approach from -heading side)
  ctx.save();
  ctx.strokeStyle = r.closed ? '#ff5a4d' : 'rgba(55,224,232,.7)';
  ctx.fillStyle = ctx.strokeStyle; ctx.lineWidth = 2;
  for (let i = 1; i <= 3; i++) {
    const d = 40 + i * 30;
    const ax = r.x - d * cx, ay = r.y - d * cy;
    ctx.beginPath();
    ctx.moveTo(ax - 10 * cx, ay - 10 * cy);
    ctx.lineTo(ax + 6 * cx, ay + 6 * cy);
    ctx.lineTo(ax - 4 * cx + 6 * cy, ay - 4 * cy - 6 * cx);
    ctx.lineTo(ax - 4 * cx - 6 * cy, ay - 4 * cy + 6 * cx);
    ctx.closePath(); ctx.fill();
  }
  ctx.restore();
  ctx.fillStyle = '#7fa6b0'; ctx.font = '11px sans-serif'; ctx.textAlign = 'center';
  ctx.fillText(r.name, r.x, r.y - 22);
}

function drawPlane(p) {
  const c = TYPE[p.type].c;
  ctx.save();
  ctx.translate(p.x, p.y); ctx.rotate(p.heading);
  ctx.fillStyle = c; ctx.strokeStyle = c; ctx.lineWidth = 1.5;
  const s = p.type === 'heavy' ? 1.4 : p.type === 'medium' ? 1.15 : 0.9;
  ctx.scale(s, s);
  if (p.type === 'light') {
    ctx.beginPath(); ctx.moveTo(10, 0); ctx.lineTo(-8, -6); ctx.lineTo(-4, 0); ctx.lineTo(-8, 6); ctx.closePath(); ctx.fill();
  } else if (p.type === 'medium') {
    ctx.beginPath(); ctx.moveTo(12, 0); ctx.lineTo(-6, -8); ctx.lineTo(-10, 0); ctx.lineTo(-6, 8); ctx.closePath(); ctx.fill();
    ctx.fillRect(-2, -1, 8, 2);
  } else {
    ctx.beginPath(); ctx.moveTo(14, 0); ctx.lineTo(-4, -10); ctx.lineTo(-12, -4); ctx.lineTo(-12, 4); ctx.lineTo(-4, 10); ctx.closePath(); ctx.fill();
    ctx.fillRect(-4, -2, 10, 4);
  }
  ctx.restore();
  // fuel bar
  const fw = 24, fh = 3, fx = p.x - fw / 2, fy = p.y - 16;
  ctx.fillStyle = '#081a21'; ctx.fillRect(fx, fy, fw, fh);
  ctx.fillStyle = p.fuel < 25 ? '#ff5a4d' : p.fuel < 50 ? '#ffb020' : '#5fe08a';
  ctx.fillRect(fx, fy, fw * (p.fuel / 100), fh);
  // callsign
  ctx.fillStyle = '#d7f0f4'; ctx.font = '10px sans-serif'; ctx.textAlign = 'center';
  ctx.fillText(CALL[p.id % CALL.length] + p.id, p.x, p.y + 22);
  // selection
  if (p.id === sel) {
    ctx.strokeStyle = '#37e0e8'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.arc(p.x, p.y, 18, 0, Math.PI * 2); ctx.stroke();
  }
}

function drawRoute(p) {
  if (p.route.length < 2) return;
  ctx.save();
  ctx.strokeStyle = 'rgba(55,224,232,.5)'; ctx.lineWidth = 1.5; ctx.setLineDash([6, 5]);
  ctx.beginPath(); ctx.moveTo(p.x, p.y);
  for (const pt of p.route) ctx.lineTo(pt.x, pt.y);
  ctx.stroke(); ctx.setLineDash([]);
  ctx.restore();
}

function render() {
  ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
  ctx.clearRect(0, 0, W, H);
  // grid
  ctx.strokeStyle = 'rgba(28,74,88,.25)'; ctx.lineWidth = 1;
  for (let x = 0; x <= W; x += 50) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); }
  for (let y = 0; y <= H; y += 50) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }
  // sea / city decor
  ctx.fillStyle = 'rgba(10,40,55,.4)';
  ctx.fillRect(0, H - 120, W, 120);
  if (!RM) {
    ctx.fillStyle = 'rgba(20,60,75,.3)';
    for (let i = 0; i < 8; i++) ctx.fillRect(60 + i * 120, 60 + (i % 3) * 40, 40, 30);
  }
  if (!g) return;
  for (const r of g.runways) drawRunway(r);
  for (const p of g.planes) drawRoute(p);
  for (const p of g.planes) drawPlane(p);
  // separation lines
  for (const w of g.warnings) {
    const a = g.planes.find(x => x.id === w.a), b = g.planes.find(x => x.id === w.b);
    if (a && b) {
      ctx.strokeStyle = w.dist < 40 ? '#ff5a4d' : '#ffb020'; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
    }
  }
  // drag preview
  if (drag && dragPts.length > 1) {
    ctx.strokeStyle = '#37e0e8'; ctx.lineWidth = 2; ctx.setLineDash([4, 4]);
    ctx.beginPath(); ctx.moveTo(dragPts[0].x, dragPts[0].y);
    for (const pt of dragPts) ctx.lineTo(pt.x, pt.y);
    ctx.stroke(); ctx.setLineDash([]);
  }
  // pause banner
  if (g.paused && !g.over) {
    ctx.fillStyle = 'rgba(4,14,20,.5)'; ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#37e0e8'; ctx.font = 'bold 32px sans-serif'; ctx.textAlign = 'center';
    ctx.fillText('DURAKLATILDI', W / 2, H / 2);
    ctx.font = '14px sans-serif'; ctx.fillStyle = '#7fa6b0';
    ctx.fillText('Devam etmek için ▶ Devam Et', W / 2, H / 2 + 30);
  }
}

// wire events
$('startBtn').addEventListener('click', () => restart());
$('startLoadBtn').addEventListener('click', doLoad);
$('againBtn').addEventListener('click', () => restart());
$('restartBtn').addEventListener('click', restart);
$('pauseBtn').addEventListener('click', togglePause);
$('saveBtn').addEventListener('click', doSave);
$('loadBtn').addEventListener('click', doLoad);
$('exportBtn').addEventListener('click', doExport);
$('importBtn').addEventListener('click', doImport);
$('fileInput').addEventListener('change', onFile);
$('speedSelect').addEventListener('change', e => speed = parseInt(e.target.value, 10));
$('clearRouteBtn').addEventListener('click', () => { if (sel) { setRoute(g, sel, []); setErr('Rota temizlendi.'); updateUI(); } });
$('approachBtn').addEventListener('click', approach);

cv.addEventListener('pointerdown', onPointerDown);
cv.addEventListener('pointermove', onPointerMove);
cv.addEventListener('pointerup', onPointerUp);
cv.addEventListener('pointercancel', onPointerCancel);
cv.addEventListener('blur', onPointerCancel);

window.addEventListener('keydown', onKey);
window.addEventListener('resize', fit);
document.addEventListener('visibilitychange', () => {
  if (document.hidden && playing && g && !g.paused) { g.paused = true; $('pauseBtn').textContent = '▶ Devam Et'; updateUI(); }
});
window.addEventListener('blur', () => {
  if (playing && g && !g.paused) { g.paused = true; $('pauseBtn').textContent = '▶ Devam Et'; updateUI(); }
});

// init
fit();
g = createGame(42, 'normal');
g.paused = true;
updateUI();
raf = requestAnimationFrame(loop);
```