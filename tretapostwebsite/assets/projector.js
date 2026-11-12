/* TretaPost — motor do projetor
   Grão de película, light leak vivo, faixa óptica de áudio, flicker no logo e som de projetor.
   Uso: <div class="projector" data-projector></div> e elementos .wordmark na página. */
(() => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const root = document.documentElement;
  const host = document.querySelector("[data-projector]");
  if (!host) return;

  /* ---------- montagem das camadas ---------- */
  const base = host.dataset.assets || "assets/";
  host.innerHTML = `
    <video class="projector__bg" autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="auto" poster="${base}poster.jpg" aria-hidden="true">
      <source src="${base}bg-hevc.mp4" type='video/mp4; codecs="hvc1"'>
      <source src="${base}bg-avc.mp4" type="video/mp4">
    </video>
    <div class="projector__leak"></div>
    <canvas class="projector__strip" aria-hidden="true"></canvas>
    <canvas class="projector__grain" aria-hidden="true"></canvas>
    <div class="projector__vignette"></div>`;
  const video = host.querySelector("video");
  const leak = host.querySelector(".projector__leak");
  const grain = host.querySelector(".projector__grain");
  const strip = host.querySelector(".projector__strip");
  // sem autoplay (modo Pouca Energia no iPhone, economia de dados ou movimento reduzido), o vídeo vira a imagem estática:
  // nunca aparece o botão de play do sistema
  const fallback = () => {
    if (!video.isConnected) return;
    const img = document.createElement("img");
    img.className = "projector__bg"; img.alt = ""; img.src = `${base}poster.jpg`;
    video.replaceWith(img);
  };
  if (reduce) fallback();
  else {
    const p = video.play?.();
    if (p && p.catch) p.catch(fallback);
    video.addEventListener("suspend", () => { if (video.paused && video.readyState < 3) setTimeout(() => video.paused && fallback(), 1200); });
  }

  /* ---------- estado compartilhado ---------- */
  let boost = 0, boostTarget = 0;   // intensidade do vazamento
  let lastY = scrollY, velocity = 0; // velocidade de scroll (px/frame suavizada)
  let hovering = false;
  let analyser = null, wave = null, analyserL = null, analyserR = null, waveL = null, waveR = null, freq = null, specL = null, specR = null;

  /* ---------- grão: tile de ruído reposicionado a 24 qps ---------- */
  const gctx = grain.getContext("2d");
  const tiles = [];
  const TILE = 180;
  for (let n = 0; n < 6; n++) {
    const c = document.createElement("canvas"); c.width = c.height = TILE;
    const x = c.getContext("2d"), img = x.createImageData(TILE, TILE);
    for (let i = 0; i < img.data.length; i += 4) {
      const v = Math.random() * 255;
      img.data[i] = img.data[i + 1] = img.data[i + 2] = v;
      img.data[i + 3] = 255;
    }
    x.putImageData(img, 0, 0);
    tiles.push(c);
  }
  function sizeGrain() {
    const s = Math.min(devicePixelRatio || 1, 1.5);
    grain.width = Math.ceil(innerWidth * s / 1.6);   // grão um pouco maior que o pixel, como película
    grain.height = Math.ceil(innerHeight * s / 1.6);
    strip.width = 32 * Math.min(devicePixelRatio || 1, 2);
    strip.height = Math.ceil(innerHeight * Math.min(devicePixelRatio || 1, 2));
    drawGrain();
  }
  function drawGrain() {
    const t = tiles[(Math.random() * tiles.length) | 0];
    const p = gctx.createPattern(t, "repeat");
    gctx.save();
    gctx.translate(-Math.random() * TILE, -Math.random() * TILE);
    gctx.fillStyle = p;
    gctx.fillRect(0, 0, grain.width + TILE, grain.height + TILE);
    gctx.restore();
  }

  /* ---------- faixa óptica: área variável, rola como filme passando no gate ---------- */
  const sctx = strip.getContext("2d");
  let stripOffset = 0;
  const seedWave = (y) => {
    // envelope de "fala/música" falso: soma de senos com rajadas
    const a = Math.sin(y * .021) * .5 + Math.sin(y * .0073 + 1.3) * .35 + Math.sin(y * .11) * .15;
    const burst = Math.max(0, Math.sin(y * .0041)) ** 3;
    return Math.min(1, Math.abs(a) * .55 + burst * .6 + .06);
  };
  // três pistas: canal esquerdo, canal direito (área variável, espelhadas) e uma pista fina central que pulsa com o grave
  let bass = 0;
  // espectro como o analisador do Fadel (Pro-Q): escala log 30 Hz–16 kHz, inclinação de 4,5 dB/oitava, curva suavizada.
  // na faixa vertical: graves embaixo, agudos em cima.
  const F0 = 30, F1 = 16000;
  function specAmp(arr, frac) {
    const sr = ctx.sampleRate, bins = arr.length, hz = sr / 2 / bins;
    const f = F0 * Math.pow(F1 / F0, frac);
    const lo = Math.max(1, Math.floor(f * Math.pow(2, -1 / 12) / hz)), hi = Math.max(lo, Math.ceil(f * Math.pow(2, 1 / 12) / hz));
    let sum = 0, n = 0;
    for (let i = lo; i <= hi && i < bins; i++) { sum += Math.pow(10, arr[i] / 10); n++; }
    const db = 10 * Math.log10(sum / Math.max(1, n) + 1e-12) + 4.5 * Math.log2(f / 1000);
    return Math.pow(Math.min(1, Math.max(0, (db + 112) / 58)), 1.4);
  }
  function trackAmp(arr, y, step, fallbackShift) {
    if (arr && soundOn) {
      const i = Math.floor(((y + stripOffset * .25) / step) % arr.length + arr.length) % arr.length;
      return Math.min(1, Math.abs(arr[i] - 128) / 46 + .05);
    }
    return seedWave(y + stripOffset + fallbackShift);
  }
  function drawStrip() {
    // uma faixa só, com camadas sobrepostas no mesmo eixo (levemente desalinhadas, como cópia de filme)
    const w = strip.width, h = strip.height, u = w / 32, cx = 16 * u;
    sctx.clearRect(0, 0, w, h);
    sctx.globalCompositeOperation = "lighter";
    const step = 2 * u;
    const layers = [
      { dx: -1.2 * u, max: 7 * u, arr: specL, shift: 0,  rgb: [70, 190, 215], a: .26, k: .5 },
      { dx: 1.2 * u,  max: 6 * u, arr: specR, shift: 37, rgb: [255, 92, 40],  a: .24, k: .55 },
    ];
    const live = soundOn && specL;
    if (live) {
      // curva contínua por pista, suavizada entre linhas vizinhas
      for (const L of layers) {
        const rows = Math.ceil(h / step), vals = new Float32Array(rows);
        for (let r = 0; r < rows; r++) vals[r] = specAmp(L.arr, 1 - (r * step) / h);
        for (let pass = 0; pass < 2; pass++) for (let r = 1; r < rows - 1; r++) vals[r] = (vals[r - 1] + vals[r] * 2 + vals[r + 1]) / 4;
        L.vals = vals;
      }
    }
    for (let y = 0, r = 0; y < h; y += step, r++) {
      for (const L of layers) {
        const amp = live ? L.vals[r] : trackAmp(null, y, step, L.shift), half = amp * L.max;
        sctx.fillStyle = `rgba(${L.rgb[0]},${L.rgb[1]},${L.rgb[2]},${L.a + amp * L.k})`;
        sctx.fillRect(cx + L.dx - half, y, half * 2, step * .7);
      }
    }
    // núcleo: linha clara no centro que acende com o grave
    const pulse = soundOn ? bass : .25 + Math.sin(stripOffset * .01) * .1;
    const core = .9 * u + pulse * 1.6 * u;
    sctx.fillStyle = `rgba(255, 236, 214, ${.16 + pulse * .6})`;
    sctx.fillRect(cx - core / 2, 0, core, h);
    sctx.globalCompositeOperation = "source-over";
  }

  /* ---------- light leak: deriva orgânica ---------- */
  function driftLeak(t) {
    const s = t / 1000;
    leak.style.setProperty("--lx1", `${-4 + Math.sin(s * .31) * 6 + Math.sin(s * .73) * 3}%`);
    leak.style.setProperty("--ly1", `${38 + Math.sin(s * .19) * 18}%`);
    leak.style.setProperty("--lx2", `${104 + Math.sin(s * .27 + 2) * 6}%`);
    leak.style.setProperty("--ly2", `${62 + Math.sin(s * .23 + 1) * 20}%`);
  }

  /* ---------- flicker de projetor: só no elemento com data-flicker (o logo grande) ---------- */
  let active = null;
  function flicker() {
    document.querySelectorAll("[data-flicker]").forEach((el) => {
      if (el !== active) { el.style.setProperty("--flick", 1); el.style.setProperty("--weave-x", "0px"); el.style.setProperty("--weave-y", "0px"); return; }
      const dip = Math.random() < .12 ? .55 + Math.random() * .25 : .9 + Math.random() * .1;
      el.style.setProperty("--flick", dip.toFixed(3));
      el.style.setProperty("--weave-x", `${(Math.random() - .5) * 1.6}px`);   // gate weave
      el.style.setProperty("--weave-y", `${(Math.random() - .5) * 2.4}px`);
    });
  }
  document.querySelectorAll("[data-flicker]").forEach((el) => {
    const on = () => { hovering = true; active = el; boostTarget = 1; };
    const off = () => { hovering = false; active = null; boostTarget = 0; };
    el.addEventListener("pointerenter", on);
    el.addEventListener("pointerleave", off);
    el.addEventListener("touchstart", () => { on(); clearTimeout(el._t); el._t = setTimeout(off, 1400); }, { passive: true });
  });

  /* ---------- loop a 24 qps (cadência de cinema) ---------- */
  let last = 0;
  function frame(t) {
    requestAnimationFrame(frame);
    if (t - last < 1000 / 24) return;
    last = t;
    const dy = scrollY - lastY; lastY = scrollY;
    velocity += (Math.abs(dy) - velocity) * .25;
    const scrollBoost = Math.min(1, velocity / 60) * .6;
    boost += (Math.max(boostTarget, scrollBoost) - boost) * .18;
    root.style.setProperty("--leak-boost", boost.toFixed(3));
    stripOffset += 14 + dy * 1.2;          // o filme corre sempre; o scroll acelera
    if (analyser && soundOn) {
      analyserL.getFloatFrequencyData(specL); analyserR.getFloatFrequencyData(specR);
      analyser.getByteFrequencyData(freq);
      let e = 0; for (let i = 1; i < 12; i++) e += freq[i]; e /= 11 * 255;
      bass += (e - bass) * .35;
    }
    drawGrain(); drawStrip(); driftLeak(t); flicker();
  }

  sizeGrain();
  addEventListener("resize", sizeGrain);
  if (reduce) { drawStrip(); } else { requestAnimationFrame(frame); }

  /* ---------- som: trilha (data-track) ou, sem trilha, ruído de projetor. Sempre iniciado por clique ---------- */
  const track = host.dataset.track ? base + host.dataset.track : null;
  let ctx = null, master = null, music = null;
  function buildSound() {
    ctx = new (window.AudioContext || window.webkitAudioContext)();
    master = ctx.createGain(); master.gain.value = 0;
    analyser = ctx.createAnalyser(); analyser.fftSize = 1024; analyser.smoothingTimeConstant = .6;
    wave = new Uint8Array(analyser.fftSize); freq = new Uint8Array(analyser.frequencyBinCount);
    const split = ctx.createChannelSplitter(2);
    analyserL = ctx.createAnalyser(); analyserR = ctx.createAnalyser(); analyserL.fftSize = analyserR.fftSize = 1024;
    waveL = new Uint8Array(1024); waveR = new Uint8Array(1024);
    analyserL.fftSize = analyserR.fftSize = 4096; analyserL.smoothingTimeConstant = analyserR.smoothingTimeConstant = .82;
    specL = new Float32Array(2048); specR = new Float32Array(2048);
    master.connect(split); split.connect(analyserL, 0); split.connect(analyserR, 1);
    if (track) {
      // a faixa óptica desenha a onda da própria música
      music = new Audio(track); music.loop = true; music.crossOrigin = "anonymous"; music.preload = "auto";
      const src = ctx.createMediaElementSource(music);
      src.connect(master);
    } else {
      const len = ctx.sampleRate * 2, buf = ctx.createBuffer(1, len, ctx.sampleRate), d = buf.getChannelData(0);
      let b0 = 0, b1 = 0, b2 = 0;
      for (let i = 0; i < len; i++) { const w = Math.random() * 2 - 1; b0 = .997 * b0 + w * .029; b1 = .985 * b1 + w * .032; b2 = .95 * b2 + w * .048; d[i] = (b0 + b1 + b2) * .25; }
      const noise = ctx.createBufferSource(); noise.buffer = buf; noise.loop = true;
      const bp = ctx.createBiquadFilter(); bp.type = "bandpass"; bp.frequency.value = 1400; bp.Q.value = .6;
      const hiss = ctx.createGain(); hiss.gain.value = .5;
      const clack = ctx.createOscillator(); clack.type = "square"; clack.frequency.value = 24;
      const clackGain = ctx.createGain(); clackGain.gain.value = .05;
      const lp = ctx.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.value = 320;
      noise.connect(bp).connect(hiss).connect(master);
      clack.connect(lp).connect(clackGain).connect(master);
      noise.start(); clack.start();
    }
    master.connect(analyser); master.connect(ctx.destination);
  }
  var soundOn = false;
  document.querySelectorAll("[data-sound]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        if (!ctx) buildSound();
        soundOn = !soundOn;
        if (ctx.state === "suspended") await ctx.resume();
        if (music && soundOn) await music.play();
        master.gain.cancelScheduledValues(ctx.currentTime);
        master.gain.setTargetAtTime(soundOn ? (music ? .9 : .16) : 0, ctx.currentTime, soundOn ? .35 : .25);
        if (music && !soundOn) setTimeout(() => { if (!soundOn) music.pause(); }, 900);
        document.querySelectorAll("[data-sound]").forEach((b) => {
          b.setAttribute("aria-pressed", String(soundOn));
          b.setAttribute("aria-label", soundOn ? "Desligar o som" : "Ligar o som");
        });
      } catch (e) { soundOn = false; }
    });
  });
  // a faixa só reage enquanto o som está ligado
  const realWave = () => soundOn && analyser;

  /* expõe utilidades para as páginas */
  window.Projector = { reduce };
})();
