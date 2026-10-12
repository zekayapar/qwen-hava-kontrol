<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>Zeka Kule — Hava Trafik Kontrolü</title>
<style>
  :root{
    --bg:#0a1420; --bg2:#0c1a28; --panel:#0f2130; --panel2:#12283a;
    --line:#1d3a4d; --line2:#274a60;
    --ink:#dceaf2; --dim:#8aa6b6; --faint:#5f7c8c;
    --amber:#f4b942; --amber2:#ffcf6b;
    --green:#57d99a; --red:#ff5d6c; --cyan:#57c7e6; --blue:#5b9bd5;
    --shadow:0 10px 30px rgba(0,0,0,.45);
    --mono:ui-monospace,"SF Mono","Cascadia Code","JetBrains Mono",Menlo,Consolas,monospace;
    --sans:"Segoe UI",system-ui,-apple-system,Roboto,Helvetica,Arial,sans-serif;
  }
  *{box-sizing:border-box}
  html,body{margin:0;height:100%}
  body{
    background:
      radial-gradient(1200px 700px at 70% -10%, #123047 0%, transparent 60%),
      radial-gradient(900px 600px at 0% 110%, #0e2a3a 0%, transparent 55%),
      var(--bg);
    color:var(--ink); font-family:var(--sans);
    -webkit-font-smoothing:antialiased; overflow-x:hidden;
  }
  .app{max-width:1440px;margin:0 auto;padding:14px 16px 26px}

  /* ---------- header ---------- */
  .top{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:12px}
  .brand{display:flex;align-items:center;gap:12px;min-width:0}
  .logo{width:44px;height:44px;flex:0 0 auto;filter:drop-shadow(0 0 8px rgba(87,199,230,.4))}
  .brand h1{font-size:clamp(20px,3.4vw,30px);margin:0;letter-spacing:.14em;font-weight:800;line-height:1}
  .brand h1 b{color:var(--amber)}
  .brand .sub{font-size:11px;letter-spacing:.28em;color:var(--dim);text-transform:uppercase;margin-top:4px}
  .clock{margin-left:auto;display:flex;align-items:center;gap:14px}
  .clock .time{font-family:var(--mono);font-size:22px;font-weight:700;color:var(--cyan);letter-spacing:.06em}
  .clock .lbl{font-size:10px;letter-spacing:.24em;color:var(--faint);text-transform:uppercase}
  .live{display:flex;align-items:center;gap:7px;font-size:11px;letter-spacing:.18em;color:var(--dim);text-transform:uppercase}
  .live .dot{width:9px;height:9px;border-radius:50%;background:var(--faint)}
  .live.on .dot{background:var(--green);box-shadow:0 0 10px var(--green);animation:pulse 1.6s infinite}
  .live.paused .dot{background:var(--amber)}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}

  /* ---------- layout ---------- */
  .layout{display:grid;grid-template-columns:minmax(0,1fr) 348px;gap:14px;align-items:start}
  .stage{position:relative;min-width:0}
  .canvas-wrap{
    position:relative;width:100%;aspect-ratio:1000/700;border-radius:14px;overflow:hidden;
    border:1px solid var(--line2);box-shadow:var(--shadow),inset 0 0 60px rgba(0,0,0,.5);
    background:#06121c;
  }
  canvas{display:block;width:100%;height:100%;touch-action:none;cursor:crosshair;outline:none}
  canvas:focus-visible{box-shadow:inset 0 0 0 3px var(--amber)}

  /* ---------- overlays ---------- */
  .overlay{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:18px;
    background:radial-gradient(120% 120% at 50% 30%, rgba(6,18,28,.55), rgba(4,12,20,.9));
    backdrop-filter:blur(2px);z-index:5}
  .overlay.hidden{display:none}
  .card{width:min(560px,100%);max-height:100%;overflow:auto;background:linear-gradient(180deg,var(--panel2),var(--panel));
    border:1px solid var(--line2);border-radius:16px;padding:22px 24px;box-shadow:var(--shadow)}
  .card h2{margin:0 0 4px;font-size:26px;letter-spacing:.02em}
  .card h2 b{color:var(--amber)}
  .card .lead{color:var(--dim);font-size:14px;margin:0 0 16px;line-height:1.5}
  .howto{display:grid;gap:10px;margin:0 0 18px}
  .howto li{display:flex;gap:12px;align-items:flex-start;list-style:none;font-size:13.5px;line-height:1.45;color:var(--ink)}
  .howto li .n{flex:0 0 auto;width:26px;height:26px;border-radius:8px;background:rgba(87,199,230,.14);
    border:1px solid var(--line2);color:var(--cyan);display:grid;place-items:center;font-family:var(--mono);font-weight:700;font-size:13px}
  .howto li b{color:var(--amber2)}
  .setup{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:18px}
  .field{display:flex;flex-direction:column;gap:6px}
  .field label{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--dim)}
  .field input,.field select{
    background:#0a1a26;border:1px solid var(--line2);color:var(--ink);border-radius:9px;padding:10px 12px;
    font-family:var(--mono);font-size:14px;outline:none;transition:border-color .15s,box-shadow .15s}
  .field input:focus,.field select:focus{border-color:var(--amber);box-shadow:0 0 0 3px rgba(244,185,66,.18)}
  .field .hint{font-size:11px;color:var(--faint)}
  .btnrow{display:flex;flex-wrap:wrap;gap:10px}
  .btn{
    font-family:var(--sans);font-size:14px;font-weight:600;letter-spacing:.02em;cursor:pointer;
    border-radius:10px;padding:11px 16px;border:1px solid var(--line2);background:var(--panel2);color:var(--ink);
    transition:transform .12s,background .15s,border-color .15s,box-shadow .15s;display:inline-flex;align-items:center;gap:8px}
  .btn:hover{transform:translateY(-1px);border-color:var(--cyan);background:#16324a}
  .btn:active{transform:translateY(0)}
  .btn:focus-visible{outline:none;box-shadow:0 0 0 3px rgba(87,199,230,.4)}
  .btn.primary{background:linear-gradient(180deg,var(--amber2),var(--amber));color:#20160a;border-color:var(--amber);
    box-shadow:0 6px 18px rgba(244,185,66,.28)}
  .btn.primary:hover{box-shadow:0 8px 24px rgba(244,185,66,.4)}
  .btn.danger{border-color:rgba(255,93,108,.5);color:var(--red)}
  .btn.danger:hover{background:rgba(255,93,108,.12);border-color:var(--red)}
  .btn.ghost{background:transparent}
  .btn.sm{padding:8px 12px;font-size:12.5px}
  .btn:disabled{opacity:.4;cursor:not-allowed;transform:none}

  /* tutorial */
  .tut{display:flex;gap:8px;margin-bottom:16px}
  .tut .step{flex:1;background:#0a1a26;border:1px solid var(--line2);border-radius:10px;padding:10px 12px;font-size:12px;line-height:1.4}
  .tut .step .k{font-family:var(--mono);font-weight:700;color:var(--amber);display:block;margin-bottom:3px;font-size:12px}
  .tut .step.done{border-color:var(--green);background:rgba(87,217,154,.08)}
  .tut .step.done .k{color:var(--green)}

  /* game over */
  .over-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:14px 0 18px}
  .over-stats .s{background:#0a1a26;border:1px solid var(--line2);border-radius:10px;padding:12px;text-align:center}
  .over-stats .s .v{font-family:var(--mono);font-size:24px;font-weight:700}
  .over-stats .s .l{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);margin-top:4px}

  /* ---------- panel ---------- */
  .panel{display:flex;flex-direction:column;gap:12px;position:sticky;top:12px}
  .card2{background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--line2);
    border-radius:14px;padding:14px 15px;box-shadow:var(--shadow)}
  .card2 h3{margin:0 0 12px;font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--dim);
    display:flex;align-items:center;gap:8px}
  .card2 h3::before{content:"";width:8px;height:8px;border-radius:2px;background:var(--amber);box-shadow:0 0 8px var(--amber)}

  .stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
  .stat{background:#0a1a26;border:1px solid var(--line2);border-radius:10px;padding:9px 10px}
  .stat .v{font-family:var(--mono);font-size:20px;font-weight:700;line-height:1}
  .stat .l{font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--dim);margin-top:5px}
  .stat.big{grid-column:span 3}
  .stat.big .v{font-size:30px;color:var(--amber)}
  .stat.good .v{color:var(--green)} .stat.bad .v{color:var(--red)}

  .seg{display:flex;gap:6px;flex-wrap:wrap}
  .seg button{flex:1;min-width:44px;background:#0a1a26;border:1px solid var(--line2);color:var(--dim);
    border-radius:9px;padding:9px 8px;font-family:var(--mono);font-size:13px;font-weight:700;cursor:pointer;transition:.15s}
  .seg button:hover{color:var(--ink);border-color:var(--cyan)}
  .seg button.on{background:linear-gradient(180deg,var(--amber2),var(--amber));color:#20160a;border-color:var(--amber)}
  .seg button:focus-visible{outline:none;box-shadow:0 0 0 3px rgba(87,199,230,.4)}

  .actions{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
  .actions .btn{justify-content:center;padding:10px 6px;font-size:12.5px}

  .legend{display:flex;flex-direction:column;gap:9px}
  .legend .row{display:flex;align-items:center;gap:10px;font-size:13px}
  .legend .sw{width:26px;height:26px;flex:0 0 auto;display:grid;place-items:center}
  .legend .row small{color:var(--faint);margin-left:auto;font-family:var(--mono);font-size:11px}

  .sel{display:flex;flex-direction:column;gap:10px}
  .sel .empty{color:var(--faint);font-size:13px;text-align:center;padding:8px 0}
  .sel .head{display:flex;align-items:center;gap:10px}
  .sel .head .badge{font-family:var(--mono);font-weight:700;font-size:15px;padding:4px 10px;border-radius:8px;
    background:#0a1a26;border:1px solid var(--line2)}
  .sel .head .tname{font-size:14px;font-weight:600}
  .sel .grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
  .sel .kv{background:#0a1a26;border:1px solid var(--line2);border-radius:9px;padding:8px 10px}
  .sel .kv .l{font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--dim)}
  .sel .kv .v{font-family:var(--mono);font-size:15px;font-weight:700;margin-top:3px}
  .fuelbar{height:8px;border-radius:5px;background:#0a1a26;overflow:hidden;border:1px solid var(--line2);margin-top:6px}
  .fuelbar i{display:block;height:100%;background:linear-gradient(90deg,var(--green),var(--amber));transition:width .3s}
  .fuelbar.low i{background:linear-gradient(90deg,var(--amber),var(--red))}
  .sel .btnrow{margin-top:2px}

  .list{display:flex;flex-direction:column;gap:6px;max-height:150px;overflow:auto}
  .list .item{display:flex;align-items:center;gap:8px;font-size:12.5px;background:#0a1a26;border:1px solid var(--line2);
    border-radius:8px;padding:7px 9px;cursor:pointer;transition:.12s}
  .list .item:hover{border-color:var(--cyan);transform:translateX(2px)}
  .list .item .id{font-family:var(--mono);font-weight:700;color:var(--cyan)}
  .list .item .meta{margin-left:auto;font-family:var(--mono);font-size:11px;color:var(--dim)}
  .list .item.warn{border-color:rgba(255,93,108,.5);background:rgba(255,93,108,.08)}
  .list .item.warn .id{color:var(--red)}
  .list .empty{color:var(--faint);font-size:12px;text-align:center;padding:6px}

  .warns{display:flex;flex-direction:column;gap:6px;max-height:120px;overflow:auto}
  .warns .w{font-size:12px;color:var(--red);background:rgba(255,93,108,.08);border:1px solid rgba(255,93,108,.35);
    border-radius:8px;padding:6px 9px;font-family:var(--mono)}
  .warns .empty{color:var(--faint);font-size:12px;text-align:center;padding:6px}

  .events{display:flex;flex-direction:column;gap:5px;max-height:150px;overflow:auto}
  .events .e{font-size:12px;line-height:1.35;display:flex;gap:8px}
  .events .e .t{font-family:var(--mono);color:var(--faint);flex:0 0 auto;font-size:11px}
  .events .e .tag{flex:0 0 auto;font-size:10px;font-weight:700;letter-spacing:.06em;padding:1px 6px;border-radius:5px;text-transform:uppercase}
  .tag.ini{background:rgba(87,217,154,.15);color:var(--green)}
  .tag.kayip{background:rgba(255,93,108,.15);color:var(--red)}
  .tag.carp{background:rgba(255,93,108,.25);color:var(--red)}
  .tag.hava{background:rgba(87,199,230,.15);color:var(--cyan)}
  .tag.oyun{background:rgba(244,185,66,.15);color:var(--amber)}
  .events .empty{color:var(--faint);font-size:12px;text-align:center;padding:6px}

  .status{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:20;
    background:var(--panel2);border:1px solid var(--line2);border-radius:10px;padding:10px 16px;font-size:13px;
    box-shadow:var(--shadow);opacity:0;pointer-events:none;transition:opacity .2s;max-width:90vw;text-align:center}
  .status.show{opacity:1}
  .status.err{border-color:var(--red);color:var(--red)}
  .status.ok{border-color:var(--green);color:var(--green)}

  .foot{margin-top:14px;font-size:11px;color:var(--faint);text-align:center;letter-spacing:.04em}
  .foot kbd{font-family:var(--mono);background:#0a1a26;border:1px solid var(--line2);border-radius:5px;padding:1px 6px;color:var(--dim)}

  @media (max-width:900px){
    .layout{grid-template-columns:1fr}
    .panel{position:static}
    .clock{margin-left:0}
  }
  @media (prefers-reduced-motion:reduce){
    *{animation-duration:.001s!important;transition-duration:.001s!important}
  }
</style>
</head>
<body>
<div class="app">
  <header class="top">
    <div class="brand">
      <svg class="logo" viewBox="0 0 48 48" aria-hidden="true">
        <circle cx="24" cy="24" r="22" fill="none" stroke="#274a60" stroke-width="2"/>
        <circle cx="24" cy="24" r="14" fill="none" stroke="#274a60" stroke-width="1.5"/>
        <circle cx="24" cy="24" r="6" fill="none" stroke="#274a60" stroke-width="1.5"/>
        <line x1="24" y1="24" x2="44" y2="10" stroke="#57c7e6" stroke-width="2"/>
        <circle cx="24" cy="24" r="3" fill="#f4b942"/>
        <circle cx="34" cy="15" r="2.4" fill="#57d99a"/>
      </svg>
      <div>
        <h1>Zeka <b>Kule</b></h1>
        <div class="sub">Hava Trafik Kontrolü</div>
      </div>
    </div>
    <div class="clock">
      <div class="live" id="live"><span class="dot"></span><span id="liveTxt">Hazır</span></div>
      <div style="text-align:right">
        <div class="time" id="clock">00:00</div>
        <div class="lbl">Simülasyon</div>
      </div>
    </div>
  </header>

  <div class="layout">
    <!-- STAGE -->
    <div class="stage">
      <div class="canvas-wrap">
        <canvas id="radar" width="1000" height="700" role="img"
          aria-label="Radar ekranı. Uçakları seçmek için üzerine tıklayın, rota çizmek için basılı tutup sürükleyin."></canvas>

        <!-- START -->
        <div class="overlay" id="startOverlay">
          <div class="card">
            <h2>Zeka <b>Kule</b></h2>
            <p class="lead">Gökyüzünü yönet: uçakları güvenli rotalara yönlendir, çarpışmaları önle, inişleri tamamla. 3 çarpışma oyunun sonudur.</p>

            <div class="tut" id="tut">
              <div class="step" data-step="1"><span class="k">1 · Seç</span>Uçağa tıkla, sağdaki panelden detayını gör.</div>
              <div class="step" data-step="2"><span class="k">2 · Çiz</span>Basılı tutup sürükle, rotayı serbestçe çiz.</div>
              <div class="step" data-step="3"><span class="k">3 · İniş</span>Uçağı doğru yönde uygun piste götür.</div>
            </div>

            <ul class="howto">
              <li><span class="n">A</span><span><b>Seç:</b> Bir uçağa tıkla. Çağrı adı, tür, hız, yakıt ve rota bilgisi sağda görünür.</span></li>
              <li><span class="n">B</span><span><b>Rota çiz:</b> Uçağa basılı tutup sürükle. Bırakınca rota uygulanır (en fazla 100 nokta).</span></li>
              <li><span class="n">C</span><span><b>İniş:</b> Uçağı <b>doğru yönde</b> (pist okuna karşı) uygun piste yaklaştır. Pist türü ve durumu önemli.</span></li>
              <li><span class="n">D</span><span><b>Dikkat:</b> Kırmızı halka = ayrım ihlali. Yakıt bitince uçak kaybedilir. Fırtına pistleri kapatır.</span></li>
            </ul>

            <div class="setup">
              <div class="field">
                <label for="seed">Seed</label>
                <input id="seed" type="number" value="42" min="0" step="1">
                <span class="hint">Aynı seed → aynı oyun</span>
              </div>
              <div class="field">
                <label for="diff">Zorluk</label>
                <select id="diff">
                  <option value="normal">Normal</option>
                  <option value="zor">Zor</option>
                </select>
                <span class="hint">Zor = daha sık uçak</span>
              </div>
            </div>

            <div class="btnrow">
              <button class="btn primary" id="startBtn">▶ Başla</button>
              <button class="btn" id="loadStartBtn">Yükle</button>
              <button class="btn ghost" id="exportStartBtn">Dışa Aktar</button>
              <button class="btn ghost" id="importStartBtn">İçe Aktar</button>
            </div>
          </div>
        </div>

        <!-- PAUSE -->
        <div class="overlay hidden" id="pauseOverlay">
          <div class="card" style="text-align:center">
            <h2>Duraklatıldı</h2>
            <p class="lead">Simülasyon beklemede. Devam etmek için aşağıdan seç.</p>
            <div class="btnrow" style="justify-content:center">
              <button class="btn primary" id="resumeBtn">▶ Devam Et</button>
              <button class="btn" id="restartBtn">↻ Yeniden Başlat</button>
              <button class="btn ghost" id="saveBtn">💾 Kaydet</button>
              <button class="btn ghost" id="loadBtn">Yükle</button>
            </div>
          </div>
        </div>

        <!-- GAME OVER -->
        <div class="overlay hidden" id="overOverlay">
          <div class="card" style="text-align:center">
            <h2>Oyun <b>Bitti</b></h2>
            <p class="lead">3 çarpışma gerçekleşti. Kule görevi sona erdi.</p>
            <div class="over-stats">
              <div class="s"><div class="v" id="ovScore">0</div><div class="l">Skor</div></div>
              <div class="s"><div class="v" id="ovLand">0</div><div class="l">İniş</div></div>
              <div class="s"><div class="v" id="ovLost">0</div><div class="l">Kayıp</div></div>
              <div class="s"><div class="v" id="ovTime">0</div><div class="l">Süre</div></div>
            </div>
            <div class="btnrow" style="justify-content:center">
              <button class="btn primary" id="overRestart">↻ Yeniden Başlat</button>
              <button class="btn ghost" id="overExport">Dışa Aktar</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- PANEL -->
    <aside class="panel">
      <div class="card2">
        <h3>Skor &amp; Durum</h3>
        <div class="stats">
          <div class="stat big"><div class="v" id="sScore">0</div><div class="l">Skor</div></div>
          <div class="stat good"><div class="v" id="sLand">0</div><div class="l">İniş</div></div>
          <div class="stat bad"><div class="v" id="sLost">0</div><div class="l">Kayıp</div></div>
          <div class="stat"><div class="v" id="sInc">0</div><div class="l">Olay</div></div>
          <div class="stat"><div class="v" id="sTime">00:00</div><div class="l">Zaman</div></div>
          <div class="stat"><div class="v" id="sActive">0</div><div class="l">Aktif Uçak</div></div>
        </div>
      </div>

      <div class="card2">
        <h3>Hava &amp; Pistler</h3>
        <div class="stats" style="grid-template-columns:1fr 1fr">
          <div class="stat"><div class="v" id="wState">Açık</div><div class="l">Hava Durumu</div></div>
          <div class="stat"><div class="v" id="wWind">0</div><div class="l">Rüzgâr</div></div>
          <div class="stat" id="rw1"><div class="v">—</div><div class="l">Pist 1</div></div>
          <div class="stat" id="rw2"><div class="v">—</div><div class="l">Pist 2</div></div>
        </div>
      </div>

      <div class="card2">
        <h3>Kontroller</h3>
        <div class="seg" id="speedSeg" role="group" aria-label="Oyun hızı">
          <button data-speed="1" class="on">1×</button>
          <button data-speed="2">2×</button>
          <button data-speed="4">4×</button>
        </div>
        <div class="actions" style="margin-top:10px">
          <button class="btn" id="pauseBtn">⏸ Duraklat</button>
          <button class="btn" id="restartBtn2">↻ Yeniden</button>
          <button class="btn" id="saveBtn2">💾 Kaydet</button>
          <button class="btn" id="loadBtn2">Yükle</button>
          <button class="btn" id="exportBtn">Dışa</button>
          <button class="btn" id="importBtn">İçe</button>
        </div>
      </div>

      <div class="card2">
        <h3>Uçak Türleri</h3>
        <div class="legend">
          <div class="row"><span class="sw"><svg width="26" height="26" viewBox="0 0 26 26"><path d="M13 3 L16 13 L13 11 L10 13 Z" fill="#57d99a"/></svg></span> Hafif <small>60 birim/sn</small></div>
          <div class="row"><span class="sw"><svg width="26" height="26" viewBox="0 0 26 26"><path d="M13 3 L17 13 L13 15 L9 13 Z" fill="#f4b942"/></svg></span> Orta <small>45 birim/sn</small></div>
          <div class="row"><span class="sw"><svg width="26" height="26" viewBox="0 0 26 26"><path d="M13 2 L18 13 L13 16 L8 13 Z" fill="#ff5d6c"/></svg></span> Ağır <small>30 birim/sn</small></div>
        </div>
      </div>

      <div class="card2">
        <h3>Seçili Uçak</h3>
        <div class="sel" id="selPanel"></div>
      </div>

      <div class="card2">
        <h3>Aktif Uçaklar</h3>
        <div class="list" id="planeList"></div>
      </div>

      <div class="card2">
        <h3>Ayrım Uyarıları</h3>
        <div class="warns" id="warnList"></div>
      </div>

      <div class="card2">
        <h3>Son Olaylar</h3>
        <div class="events" id="eventList"></div>
      </div>
    </aside>
  </div>

  <div class="foot">
    Kısayollar: <kbd>Boşluk</kbd>/<kbd>P</kbd> duraklat · <kbd>1</kbd><kbd>2</kbd><kbd>4</kbd> hız · <kbd>R</kbd> yeniden · <kbd>Esc</kbd> seçimi bırak
  </div>
</div>

<div class="status" id="status" role="status" aria-live="polite"></div>
<input type="file" id="fileInput" accept="application/json,.json" hidden>

<script type="module">
import { createGame, addPlane, setRoute, tick, serialize, deserialize } from './engine.js';

/* ============================ constants ============================ */
const W = 1000, H = 700;
const SAVE_KEY = 'qwen-kule-save-v1';
const TYPE = {
  light:  { name:'Hafif', color:'#57d99a', size:1.0 },
  medium: { name:'Orta',  color:'#f4b942', size:1.15 },
  heavy:  { name:'Ağır',  color:'#ff5d6c', size:1.35 }
};
const RW_COLOR = { open:'#57d99a', busy:'#f4b942', closed:'#ff5d6c' };
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ============================ state ============================ */
let game = createGame(42, 'normal');
let started = false;      // tick yalnızca started && !paused && !over
let speed = 1;
let selectedId = null;
let drawing = false;
let drawPts = [];
let lastTime = 0;
let uiAccum = 0;
let rafId = null;
let statusTimer = null;

/* ============================