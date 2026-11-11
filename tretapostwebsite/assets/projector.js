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
  let analyser = null, wave = null;

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
    strip.width = 18 * Math.min(devicePixelRatio || 1, 2);
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
  function drawStrip() {
    const w = strip.width, h = strip.height, cx = w / 2;
    sctx.clearRect(0, 0, w, h);
    const step = 2 * (w / 18);
    for (let y = 0; y < h; y += step) {
      let amp;
      if (wave) {
        const i = Math.floor(((y + stripOffset) / step) % wave.length + wave.length) % wave.length;
        amp = Math.min(1, Math.abs(wave[i] - 128) / 60 + .05);
      } else {
        amp = seedWave(y + stripOffset);
      }
      const half = amp * (w * .46);
      const hue = (y + stripOffset) * .02;
      // mistura ciano / laranja / magenta como na faixa original
      const mix = (Math.sin(hue) + 1) / 2;
      const r = Math.round(99 + mix * 156), g = Math.round(199 - mix * 110), b = Math.round(212 - mix * 120);
      sctx.fillStyle = `rgba(${r},${g},${b},${.35 + amp * .5})`;
      sctx.fillRect(cx - half, y, half * 2, step * .7);
    }
    // linha central da pista
    sctx.fillStyle = "rgba(99,199,212,.35)";
    sctx.fillRect(cx - .5, 0, 1, h);
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
    if (analyser) { analyser.getByteTimeDomainData(wave); }
    drawGrain(); drawStrip(); driftLeak(t); flicker();
  }

  sizeGrain();
  addEventListener("resize", sizeGrain);
  if (reduce) { drawStrip(); } else { requestAnimationFrame(frame); }

  /* ---------- som de projetor (opcional, sempre iniciado por clique) ---------- */
  let ctx = null, master = null;
  function buildSound() {
    ctx = new (window.AudioContext || window.webkitAudioContext)();
    master = ctx.createGain(); master.gain.value = 0;
    // chiado do motor: ruído rosa filtrado
    const len = ctx.sampleRate * 2, buf = ctx.createBuffer(1, len, ctx.sampleRate), d = buf.getChannelData(0);
    let b0 = 0, b1 = 0, b2 = 0;
    for (let i = 0; i < len; i++) { const w = Math.random() * 2 - 1; b0 = .997 * b0 + w * .029; b1 = .985 * b1 + w * .032; b2 = .95 * b2 + w * .048; d[i] = (b0 + b1 + b2) * .25; }
    const noise = ctx.createBufferSource(); noise.buffer = buf; noise.loop = true;
    const bp = ctx.createBiquadFilter(); bp.type = "bandpass"; bp.frequency.value = 1400; bp.Q.value = .6;
    const hiss = ctx.createGain(); hiss.gain.value = .5;
    // claque do obturador: 24 batidas por segundo moduladas
    const clack = ctx.createOscillator(); clack.type = "square"; clack.frequency.value = 24;
    const clackGain = ctx.createGain(); clackGain.gain.value = .05;
    const lp = ctx.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.value = 320;
    noise.connect(bp).connect(hiss).connect(master);
    clack.connect(lp).connect(clackGain).connect(master);
    analyser = ctx.createAnalyser(); analyser.fftSize = 512; wave = new Uint8Array(analyser.fftSize);
    master.connect(analyser); master.connect(ctx.destination);
    noise.start(); clack.start();
  }
  document.querySelectorAll("[data-sound]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        if (!ctx) buildSound();
        const on = btn.getAttribute("aria-pressed") !== "true";
        if (ctx.state === "suspended") await ctx.resume();
        master.gain.setTargetAtTime(on ? .16 : 0, ctx.currentTime, .25);
        document.querySelectorAll("[data-sound]").forEach((b) => {
          b.setAttribute("aria-pressed", String(on));
          b.setAttribute("aria-label", on ? "Desligar o som" : "Ligar o som");
        });
        if (!on) { setTimeout(() => { analyser = null; wave = null; }, 600); }
        else if (!analyser) { analyser = ctx.createAnalyser(); analyser.fftSize = 512; wave = new Uint8Array(512); master.connect(analyser); }
      } catch (e) { btn.disabled = true; }
    });
  });

  /* expõe utilidades para as páginas */
  window.Projector = { reduce };
})();
