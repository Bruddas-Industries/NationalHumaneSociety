// Confetti for the Previous Winners page (preview only).
// Two bursts pop up from the bottom corners, arc over and drift down the
// screen, mixing rectangles, circles and paw prints in the brand colours. The
// canvas lets clicks through and removes itself when done. Skipped for
// visitors who ask for reduced motion.
//
// Performance: every shape/colour is drawn once into a small sprite up front,
// so each frame only stamps images (no path building); fewer pieces on small
// screens; resolution capped at 1.5x; and it waits for the page to finish its
// initial load (capped) so it isn't competing with photo decoding.
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const COLOURS = ['#fa5853', '#fbff00', '#181733', '#2b8979', '#f3a94b', '#3498af'];
  const SHAPES = ['rect', 'circle', 'paw'];
  const DURATION = 4200;     // ms before the remaining pieces fade out
  const MAX_WAIT = 1200;     // ms to wait for the page's load event at most
  const SPRITE = 40;         // sprite size in px (pieces are drawn scaled down)

  const rand = (min, max) => min + Math.random() * (max - min);

  // --- sprites: one small canvas per shape + colour ------------------------
  const drawShape = (c, shape, s) => {
    if (shape === 'rect') { c.fillRect(-s / 2, -s * 0.3, s, s * 0.6); return; }
    if (shape === 'circle') { c.beginPath(); c.arc(0, 0, s * 0.4, 0, Math.PI * 2); c.fill(); return; }
    c.beginPath(); // paw: main pad + four toes
    c.ellipse(0, s * 0.18, s * 0.34, s * 0.28, 0, 0, Math.PI * 2);
    [[-0.36, -0.12, 0.13], [-0.13, -0.34, 0.14], [0.13, -0.34, 0.14], [0.36, -0.12, 0.13]].forEach(([tx, ty, tr]) => {
      c.moveTo(tx * s + tr * s, ty * s);
      c.ellipse(tx * s, ty * s, tr * s, tr * s * 1.25, 0, 0, Math.PI * 2);
    });
    c.fill();
  };
  const sprites = {};
  const makeSprites = () => {
    SHAPES.forEach((shape) => COLOURS.forEach((colour) => {
      const sc = document.createElement('canvas');
      sc.width = sc.height = SPRITE;
      const c = sc.getContext('2d');
      c.translate(SPRITE / 2, SPRITE / 2);
      c.fillStyle = colour;
      drawShape(c, shape, SPRITE * 0.9);
      sprites[shape + colour] = sc;
    }));
  };

  // --- pieces --------------------------------------------------------------
  let canvas, ctx, w = 0, h = 0, dpr = 1;
  const resize = () => {
    dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    w = window.innerWidth;
    h = window.innerHeight;
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
  };

  const pieces = [];
  const piece = (dir, scale) => {
    const r = Math.random();
    const shape = r < 0.22 ? 'paw' : r < 0.6 ? 'rect' : 'circle';
    const speed = rand(11, 19) * Math.max(0.75, Math.min(1.15, h / 800));
    const angle = rand(55, 80) * Math.PI / 180; // up and inward
    return {
      sprite: sprites[shape + COLOURS[Math.floor(Math.random() * COLOURS.length)]],
      flat: shape !== 'paw', // paper shapes tumble; paws just spin
      x: dir > 0 ? rand(-10, w * 0.08) : rand(w * 0.92, w + 10),
      y: h + rand(0, 30),
      vx: Math.cos(angle) * speed * dir * rand(0.5, 1.1),
      vy: -Math.sin(angle) * speed,
      size: (shape === 'paw' ? rand(15, 21) : rand(8, 13)) * scale,
      rot: rand(0, Math.PI * 2),
      spin: rand(-0.2, 0.2),
      wobble: rand(0, Math.PI * 2),
      wobbleSpeed: rand(0.06, 0.14),
    };
  };

  // --- animation -----------------------------------------------------------
  let start = null, last = null;
  const frame = (now) => {
    if (start === null) { start = now; last = now; }
    const elapsed = now - start;
    const dt = Math.min(2.5, (now - last) / 16.67); // in 60fps frames
    last = now;

    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.globalAlpha = elapsed > DURATION ? Math.max(0, 1 - (elapsed - DURATION) / 900) : 1;

    let alive = 0;
    const drag = Math.pow(0.985, dt);
    for (let i = 0; i < pieces.length; i++) {
      const p = pieces[i];
      if (p.done) continue;
      p.vy = Math.min(p.vy + 0.32 * dt, 4.2); // gravity, then flutter down
      p.vx *= drag;
      p.x += (p.vx + Math.sin(p.wobble) * 0.6) * dt;
      p.y += p.vy * dt;
      p.rot += p.spin * dt;
      p.wobble += p.wobbleSpeed * dt;
      if (p.y > h + 40) { p.done = true; continue; }
      alive++;

      // rotate, squash (tumbling paper) and place in one transform
      const cos = Math.cos(p.rot), sin = Math.sin(p.rot);
      const sy = p.flat ? Math.cos(p.wobble) : 1;
      ctx.setTransform(cos * dpr, sin * dpr, -sin * sy * dpr, cos * sy * dpr, p.x * dpr, p.y * dpr);
      ctx.drawImage(p.sprite, -p.size / 2, -p.size / 2, p.size, p.size);
    }

    if (alive && ctx.globalAlpha > 0) requestAnimationFrame(frame);
    else { window.removeEventListener('resize', resize); canvas.remove(); }
  };

  const go = () => {
    makeSprites();
    canvas = document.createElement('canvas');
    canvas.setAttribute('aria-hidden', 'true');
    canvas.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:200';
    document.body.appendChild(canvas);
    ctx = canvas.getContext('2d');
    resize();
    window.addEventListener('resize', resize);
    const small = w < 700;
    const count = small ? 90 : 150;
    const scale = small ? 0.8 : 1;
    for (let i = 0; i < count; i++) pieces.push(piece(i % 2 ? 1 : -1, scale));
    requestAnimationFrame(frame);
  };

  // Start once the page has finished its initial load (photos decoded), but
  // never more than MAX_WAIT ms after the page appears.
  let started = false;
  const begin = () => { if (!started) { started = true; requestAnimationFrame(go); } };
  if (document.readyState === 'complete') begin();
  else {
    window.addEventListener('load', begin, { once: true });
    setTimeout(begin, MAX_WAIT);
  }
})();
