export function createGame(seed = 42, difficulty = 'normal') {
  const rng = mulberry32(seed);
  const g = {
    version: 1, time: 0, paused: false, over: false,
    planes: [], runways: [], score: 0, landed: 0, lost: 0, incidents: 0,
    warnings: [], events: [], seed: seed, rngState: rng.s,
    spawnTimer: 5, weather: { wind: 0, storm: false, stormTimer: 0 },
    idCounter: 0, difficulty: difficulty
  };
  g.runways = [
    { id: 'RW1', name: 'Pist 1', x: 200, y: 350, heading: 0, accepts: ['light', 'medium'], busy: 0, closed: false, closeTimer: 0 },
    { id: 'RW2', name: 'Pist 2', x: 800, y: 350, heading: Math.PI, accepts: ['medium', 'heavy'], busy: 0, closed: false, closeTimer: 0 }
  ];
  logEvent(g, 'başlangıç', 'Oyun başladı');
  return g;
}

function mulberry32(a) {
  return {
    s: a >>> 0,
    next() {
      this.s = (this.s + 0x6D2B79F5) | 0;
      let t = Math.imul(this.s ^ (this.s >>> 15), 1 | this.s);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    }
  };
}

function logEvent(g, type, text) {
  g.events.push({ time: g.time, type, text });
  if (g.events.length > 50) g.events.shift();
}

function dist(a, b) {
  const dx = a.x - b.x, dy = a.y - b.y;
  return Math.sqrt(dx * dx + dy * dy);
}

function headingDiff(a, b) {
  let d = a - b;
  while (d > Math.PI) d -= 2 * Math.PI;
  while (d < -Math.PI) d += 2 * Math.PI;
  return Math.abs(d);
}

function clamp(v, min, max) {
  return v < min ? min : v > max ? max : v;
}

function speedFor(type) {
  return type === 'light' ? 60 : type === 'medium' ? 45 : 30;
}

function fuelFor(type) {
  return type === 'light' ? 120 : type === 'medium' ? 150 : 180;
}

export function addPlane(g, options) {
  const type = options && options.type !== undefined ? options.type : 'light';
  if (!['light', 'medium', 'heavy'].includes(type)) throw new Error('Geçersiz uçak türü');
  const x = options && options.x !== undefined ? options.x : 0;
  const y = options && options.y !== undefined ? options.y : 0;
  if (typeof x !== 'number' || !isFinite(x) || typeof y !== 'number' || !isFinite(y)) throw new Error('Geçersiz koordinat');
  const heading = options && options.heading !== undefined ? options.heading : 0;
  if (typeof heading !== 'number' || !isFinite(heading)) throw new Error('Geçersiz yön');
  const fuel = options && options.fuel !== undefined ? options.fuel : fuelFor(type);
  if (typeof fuel !== 'number' || !isFinite(fuel) || fuel < 0) throw new Error('Geçersiz yakıt');
  g.idCounter++;
  const p = { id: g.idCounter, type, x, y, heading, speed: speedFor(type), fuel, route: [] };
  g.planes.push(p);
  return p;
}

export function setRoute(g, id, points) {
  const p = g.planes.find(pl => pl.id === id);
  if (!p) return false;
  if (!Array.isArray(points)) return false;
  if (points.length > 100) return false;
  for (const pt of points) {
    if (typeof pt !== 'object' || pt === null) return false;
    if (typeof pt.x !== 'number' || !isFinite(pt.x) || typeof pt.y !== 'number' || !isFinite(pt.y)) return false;
  }
  p.route = points.map(pt => ({ x: clamp(pt.x, 0, 1000), y: clamp(pt.y, 0, 700) }));
  return true;
}

export function tick(g, dt) {
  if (g.paused || g.over) return;
  if (typeof dt !== 'number' || !isFinite(dt) || dt < 0) return;
  if (dt === 0) return;
  dt = Math.min(dt, 0.1);
  g.time += dt;

  // Weather
  if (g.time > 60) {
    const rng = mulberry32(g.rngState);
    const r = rng.next();
    g.rngState = rng.s;
    if (r < 0.02 && !g.weather.storm) {
      g.weather.storm = true;
      g.weather.stormTimer = 15 + rng.next() * 15;
      g.weather.wind = 20 + rng.next() * 30;
      logEvent(g, 'hava', 'Fırtına başladı');
      for (const rw of g.runways) {
        if (!rw.closed) {
          rw.closed = true;
          rw.closeTimer = 10 + rng.next() * 10;
        }
      }
    } else if (g.weather.storm) {
      g.weather.stormTimer -= dt;
      if (g.weather.stormTimer <= 0) {
        g.weather.storm = false;
        g.weather.wind = 0;
        logEvent(g, 'hava', 'Fırtına bitti');
        for (const rw of g.runways) {
          if (rw.closed) {
            rw.closed = false;
            rw.closeTimer = 0;
          }
        }
      }
    }
  }

  // Runway timers
  for (const rw of g.runways) {
    if (rw.busy > 0) rw.busy = Math.max(0, rw.busy - dt);
    if (rw.closed && rw.closeTimer > 0) {
      rw.closeTimer -= dt;
      if (rw.closeTimer <= 0) {
        rw.closed = false;
        rw.closeTimer = 0;
      }
    }
  }

  // Spawn
  g.spawnTimer -= dt;
  if (g.spawnTimer <= 0) {
    const rng = mulberry32(g.rngState);
    g.rngState = rng.s;
    const types = ['light', 'medium', 'heavy'];
    const type = types[Math.floor(rng.next() * types.length)];
    const side = Math.floor(rng.next() * 4);
    let x, y, heading;
    if (side === 0) { x = 0; y = rng.next() * 700; heading = 0; }
    else if (side === 1) { x = 1000; y = rng.next() * 700; heading = Math.PI; }
    else if (side === 2) { x = rng.next() * 1000; y = 0; heading = Math.PI / 2; }
    else { x = rng.next() * 1000; y = 700; heading = -Math.PI / 2; }
    // Check separation
    let ok = true;
    for (const p of g.planes) {
      if (dist({ x, y }, p) < 50) { ok = false; break; }
    }
    if (ok) {
      g.idCounter++;
      const p = { id: g.idCounter, type, x, y, heading, speed: speedFor(type), fuel: fuelFor(type), route: [] };
      g.planes.push(p);
    }
    const base = g.difficulty === 'zor' ? 3 : 5;
    const decay = Math.max(1, base - g.time / 100);
    g.spawnTimer = decay + rng.next() * 2;
  }

  // Move planes
  const removed = new Set();
  for (const p of g.planes) {
    if (removed.has(p.id)) continue;
    p.fuel -= dt;
    if (p.fuel <= 0) {
      p.fuel = 0;
      removed.add(p.id);
      g.lost++;
      g.score -= 10;
      logEvent(g, 'kayıp', `Uçak ${p.id} yakıt bitti`);
      continue;
    }
    let target = null;
    if (p.route.length > 0) {
      target = p.route[0];
    } else {
      target = { x: p.x + Math.cos(p.heading) * 100, y: p.y + Math.sin(p.heading) * 100 };
    }
    const dx = target.x - p.x, dy = target.y - p.y;
    const d = Math.sqrt(dx * dx + dy * dy);
    if (d > 0.001) {
      const desired = Math.atan2(dy, dx);
      let diff = desired - p.heading;
      while (diff > Math.PI) diff -= 2 * Math.PI;
      while (diff < -Math.PI) diff += 2 * Math.PI;
      p.heading += diff;
      const move = p.speed * dt;
      if (move >= d) {
        p.x = target.x;
        p.y = target.y;
        if (p.route.length > 0) p.route.shift();
      } else {
        p.x += (dx / d) * move;
        p.y += (dy / d) * move;
      }
    }
    if (p.x < 0 || p.x > 1000 || p.y < 0 || p.y > 700) {
      removed.add(p.id);
      g.lost++;
      g.score -= 10;
      logEvent(g, 'kayıp', `Uçak ${p.id} alan dışına çıktı`);
    }
  }
  g.planes = g.planes.filter(p => !removed.has(p.id));

  // Collision detection
  const active = g.planes;
  const colliding = new Set();
  for (let i = 0; i < active.length; i++) {
    for (let j = i + 1; j < active.length; j++) {
      const a = active[i], b = active[j];
      if (dist(a, b) < 12) {
        colliding.add(a.id);
        colliding.add(b.id);
      }
    }
  }
  if (colliding.size > 0) {
    const ids = [...colliding];
    const removed2 = new Set(ids);
    g.planes = g.planes.filter(p => !removed2.has(p.id));
    g.incidents++;
    g.lost += 2;
    g.score -= 50;
    logEvent(g, 'çarpışma', `Çarpışma: ${ids.join(', ')}`);
    if (g.incidents >= 3) {
      g.over = true;
      logEvent(g, 'oyun', 'Oyun bitti: 3 çarpışma');
    }
  }

  // Landing
  const landedThisTick = new Set();
  for (const p of g.planes) {
    for (const rw of g.runways) {
      if (landedThisTick.has(rw.id)) continue;
      if (rw.closed || rw.busy > 0) continue;
      if (!rw.accepts.includes(p.type)) continue;
      if (dist(p, rw) >= 18) continue;
      if (headingDiff(p.heading, rw.heading) >= 0.35) continue;
      p.x = rw.x;
      p.y = rw.y;
      p.heading = rw.heading;
      landedThisTick.add(rw.id);
      rw.busy = 3;
      g.landed++;
      g.score += 20;
      logEvent(g, 'iniş', `Uçak ${p.id} ${rw.name} iniş yaptı`);
      break;
    }
  }
  if (landedThisTick.size > 0) {
    const landedIds = new Set();
    for (const p of g.planes) {
      for (const rw of g.runways) {
        if (landedThisTick.has(rw.id) && dist(p, rw) < 1 && headingDiff(p.heading, rw.heading) < 0.01) {
          landedIds.add(p.id);
          break;
        }
      }
    }
    g.planes = g.planes.filter(p => !landedIds.has(p.id));
  }

  // Warnings
  g.warnings = [];
  const act = g.planes;
  for (let i = 0; i < act.length; i++) {
    for (let j = i + 1; j < act.length; j++) {
      const a = act[i], b = act[j];
      const d = dist(a, b);
      if (d < 35) {
        g.warnings.push({ a: a.id, b: b.id, dist: d });
      }
    }
  }
}

export function serialize(g) {
  return JSON.stringify(g);
}

export function deserialize(text) {
  let obj;
  try {
    obj = JSON.parse(text);
  } catch (e) {
    throw new Error('Geçersiz JSON');
  }
  if (typeof obj !== 'object' || obj === null) throw new Error('Geçersiz veri');
  if (obj.version !== 1) throw new Error('Geçersiz sürüm');
  if (typeof obj.time !== 'number' || !isFinite(obj.time)) throw new Error('Geçersiz zaman');
  if (typeof obj.paused !== 'boolean') throw new Error('Geçersiz paused');
  if (typeof obj.over !== 'boolean') throw new Error('Geçersiz over');
  if (!Array.isArray(obj.planes)) throw new Error('Geçersiz planes');
  if (!Array.isArray(obj.runways)) throw new Error('Geçersiz runways');
  if (typeof obj.score !== 'number' || !isFinite(obj.score)) throw new Error('Geçersiz score');
  if (typeof obj.landed !== 'number' || !isFinite(obj.landed)) throw new Error('Geçersiz landed');
  if (typeof obj.lost !== 'number' || !isFinite(obj.lost)) throw new Error('Geçersiz lost');
  if (typeof obj.incidents !== 'number' || !isFinite(obj.incidents)) throw new Error('Geçersiz incidents');
  if (!Array.isArray(obj.warnings)) throw new Error('Geçersiz warnings');
  if (!Array.isArray(obj.events)) throw new Error('Geçersiz events');
  if (typeof obj.seed !== 'number' || !isFinite(obj.seed)) throw new Error('Geçersiz seed');
  if (typeof obj.rngState !== 'number' || !isFinite(obj.rngState)) throw new Error('Geçersiz rngState');
  if (typeof obj.spawnTimer !== 'number' || !isFinite(obj.spawnTimer)) throw new Error('Geçersiz spawnTimer');
  if (typeof obj.idCounter !== 'number' || !isFinite(obj.idCounter)) throw new Error('Geçersiz idCounter');
  if (typeof obj.difficulty !== 'string') throw new Error('Geçersiz difficulty');
  if (!obj.weather || typeof obj.weather !== 'object') throw new Error('Geçersiz weather');
  if (typeof obj.weather.wind !== 'number' || !isFinite(obj.weather.wind)) throw new Error('Geçersiz wind');
  if (typeof obj.weather.storm !== 'boolean') throw new Error('Geçersiz storm');
  if (typeof obj.weather.stormTimer !== 'number' || !isFinite(obj.weather.stormTimer)) throw new Error('Geçersiz stormTimer');

  for (const p of obj.planes) {
    if (typeof p !== 'object' || p === null) throw new Error('Geçersiz uçak');
    if (typeof p.id !== 'number' || !isFinite(p.id)) throw new Error('Geçersiz uçak id');
    if (!['light', 'medium', 'heavy'].includes(p.type)) throw new Error('Geçersiz uçak türü');
    if (typeof p.x !== 'number' || !isFinite(p.x)) throw new Error('Geçersiz x');
    if (typeof p.y !== 'number' || !isFinite(p.y)) throw new Error('Geçersiz y');
    if (typeof p.heading !== 'number' || !isFinite(p.heading)) throw new Error('Geçersiz heading');
    if (typeof p.speed !== 'number' || !isFinite(p.speed)) throw new Error('Geçersiz speed');
    if (typeof p.fuel !== 'number' || !isFinite(p.fuel)) throw new Error('Geçersiz fuel');
    if (!Array.isArray(p.route)) throw new Error('Geçersiz route');
    if (p.route.length > 100) throw new Error('Route çok uzun');
    for (const pt of p.route) {
      if (typeof pt !== 'object' || pt === null) throw new Error('Geçersiz rota noktası');
      if (typeof pt.x !== 'number' || !isFinite(pt.x)) throw new Error('Geçersiz rota x');
      if (typeof pt.y !== 'number' || !isFinite(pt.y)) throw new Error('Geçersiz rota y');
    }
  }

  for (const rw of obj.runways) {
    if (typeof rw !== 'object' || rw === null) throw new Error('Geçersiz pist');
    if (typeof rw.id !== 'string') throw new Error('Geçersiz pist id');
    if (typeof rw.name !== 'string') throw new Error('Geçersiz pist name');
    if (typeof rw.x !== 'number' || !isFinite(rw.x)) throw new Error('Geçersiz pist x');
    if (typeof rw.y !== 'number' || !isFinite(rw.y)) throw new Error('Geçersiz pist y');
    if (typeof rw.heading !== 'number' || !isFinite(rw.heading)) throw new Error('Geçersiz pist heading');
    if (!Array.isArray(rw.accepts)) throw new Error('Geçersiz accepts');
    for (const t of rw.accepts) {
      if (!['light', 'medium', 'heavy'].includes(t)) throw new Error('Geçersiz accepts türü');
    }
    if (typeof rw.busy !== 'number' || !isFinite(rw.busy)) throw new Error('Geçersiz busy');
    if (typeof rw.closed !== 'boolean') throw new Error('Geçersiz closed');
    if (typeof rw.closeTimer !== 'number' || !isFinite(rw.closeTimer)) throw new Error('Geçersiz closeTimer');
  }

  for (const w of obj.warnings) {
    if (typeof w !== 'object' || w === null) throw new Error('Geçersiz warning');
    if (typeof w.a !== 'number' || !isFinite(w.a)) throw new Error('Geçersiz warning a');
    if (typeof w.b !== 'number' || !isFinite(w.b)) throw new Error('Geçersiz warning b');
    if (typeof w.dist !== 'number' || !isFinite(w.dist)) throw new Error('Geçersiz warning dist');
  }

  for (const e of obj.events) {
    if (typeof e !== 'object' || e === null) throw new Error('Geçersiz event');
    if (typeof e.time !== 'number' || !isFinite(e.time)) throw new Error('Geçersiz event time');
    if (typeof e.type !== 'string') throw new Error('Geçersiz event type');
    if (typeof e.text !== 'string') throw new Error('Geçersiz event text');
  }

  if (obj.events.length > 50) obj.events = obj.events.slice(-50);

  return obj;
}
