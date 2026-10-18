// Mobile menu toggle + active-link highlighting + preview-flag dismissal +
// transparent-header-over-video on the homepage
(function () {
  // Preview flag — dismiss on click of the X, persist for the session
  const flag = document.getElementById('previewFlag');
  if (flag) {
    if (sessionStorage.getItem('nhs-preview-flag-dismissed') === '1') {
      flag.classList.add('is-dismissed');
    }
    const closeBtn = flag.querySelector('.preview-flag-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        flag.classList.add('is-dismissed');
        try { sessionStorage.setItem('nhs-preview-flag-dismissed', '1'); } catch (_) {}
      });
    }
  }

  // Transparent-on-video header (homepage only).
  // Header starts transparent over the video hero, then transitions to solid
  // white once the user scrolls past the threshold.
  if (document.body.classList.contains('is-home')) {
    const header = document.querySelector('.site-header');
    if (header) {
      const THRESHOLD = 60;
      const updateHeader = () => {
        if (window.scrollY < THRESHOLD) header.classList.add('at-top');
        else header.classList.remove('at-top');
      };
      updateHeader();
      window.addEventListener('scroll', updateHeader, { passive: true });
    }
  }

  const header = document.querySelector('.site-header');
  const toggle = document.querySelector('.menu-toggle');
  if (toggle && header) {
    toggle.addEventListener('click', () => {
      header.classList.toggle('is-open');
      // When the mobile menu is open over the video hero, force the header
      // out of its transparent state so dropdown items remain readable.
      if (header.classList.contains('is-open')) header.classList.remove('at-top');
      else if (document.body.classList.contains('is-home') && window.scrollY < 60) {
        header.classList.add('at-top');
      }
    });
  }

  // Highlight current page in nav
  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link, .nav-dropdown a').forEach((a) => {
    const href = a.getAttribute('href');
    if (href === path) a.classList.add('is-active');
  });

  // Donate widget interactions (preview only).
  // Monthly and one-time share every preset except the largest, which carries
  // both values in data-monthly / data-one-time and swaps with the toggle.
  document.querySelectorAll('.donate-widget').forEach((widget) => {
    const cta = widget.querySelector('.donate-cta');
    const mode = () => {
      const active = widget.querySelector('.donate-toggle button.is-active');
      return (active && active.dataset.mode) || 'monthly';
    };
    const updateCta = () => {
      if (!cta) return;
      const btn = widget.querySelector('.amount-btn.is-active');
      const amount = btn ? btn.dataset.amount : null;
      const suffix = mode() === 'monthly' ? ' monthly' : '';
      cta.textContent = amount && amount !== 'other'
        ? `Donate $${amount}${suffix} →`
        : `Donate${suffix} →`;
    };
    widget.querySelectorAll('.amount-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        widget.querySelectorAll('.amount-btn').forEach((b) => b.classList.remove('is-active'));
        btn.classList.add('is-active');
        updateCta();
      });
    });
    widget.querySelectorAll('.donate-toggle button').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        widget.querySelectorAll('.donate-toggle button').forEach((b) => b.classList.remove('is-active'));
        btn.classList.add('is-active');
        const key = mode() === 'monthly' ? 'monthly' : 'oneTime';
        widget.querySelectorAll('.amount-btn[data-monthly]').forEach((b) => {
          b.dataset.amount = b.dataset[key];
          b.textContent = `$${b.dataset[key]}`;
        });
        updateCta();
      });
    });
  });

  // Educational video carousel: arrows page through the cards, and a card
  // plays its video in place (one at a time) instead of opening YouTube.
  document.querySelectorAll('[data-carousel]').forEach((carousel) => {
    const track = carousel.querySelector('.short-track');
    if (!track) return;
    const prev = carousel.querySelector('.carousel-btn[data-dir="-1"]');
    const next = carousel.querySelector('.carousel-btn[data-dir="1"]');
    const updateArrows = () => {
      const max = track.scrollWidth - track.clientWidth - 2;
      if (prev) prev.disabled = track.scrollLeft <= 2;
      if (next) next.disabled = track.scrollLeft >= max;
    };
    carousel.querySelectorAll('.carousel-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        track.scrollBy({ left: Number(btn.dataset.dir) * track.clientWidth });
      });
    });
    track.addEventListener('scroll', updateArrows, { passive: true });
    window.addEventListener('resize', updateArrows);
    updateArrows();

    let playing = null; // { player, card }: the card goes back when another video starts
    track.querySelectorAll('a.short-card').forEach((card) => {
      card.addEventListener('click', (e) => {
        e.preventDefault();
        if (playing) playing.player.replaceWith(playing.card);
        const player = document.createElement('div');
        player.className = 'short-card is-playing';
        const iframe = document.createElement('iframe');
        iframe.src = `https://www.youtube-nocookie.com/embed/${card.dataset.video}?autoplay=1&playsinline=1&rel=0`;
        iframe.title = card.querySelector('.short-title')?.textContent || 'Video';
        iframe.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
        iframe.allowFullscreen = true;
        // YouTube refuses to play embeds that arrive without a referrer (error 153).
        iframe.referrerPolicy = 'strict-origin-when-cross-origin';
        player.appendChild(iframe);
        card.replaceWith(player);
        playing = { player, card };
      });
    });
  });

  // Photo strips (prize cards, entry-page heroes): arrows and dots page
  // through the cars, wrapping round at the ends; swiping works through the
  // scroll container itself. With data-autoplay="ms" the strip also moves on
  // by itself, pausing while the pointer or keyboard focus is on it, and
  // never for visitors who ask for reduced motion.
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-gallery]').forEach((gallery) => {
    const track = gallery.querySelector('.prize-slides');
    const count = track ? track.children.length : 0;
    if (count < 2) return;
    const dots = [...gallery.querySelectorAll('.gallery-dots button')];
    const current = () => Math.round(track.scrollLeft / track.clientWidth);
    const go = (i) => track.scrollTo({ left: ((i + count) % count) * track.clientWidth });

    const delay = Number(gallery.dataset.autoplay) || 0;
    let timer = null;
    let paused = false;
    const restart = () => {
      if (!delay || reduceMotion) return;
      clearInterval(timer);
      timer = setInterval(() => {
        if (!paused && !document.hidden) go(current() + 1);
      }, delay);
    };
    gallery.addEventListener('mouseenter', () => { paused = true; });
    gallery.addEventListener('mouseleave', () => { paused = false; restart(); });
    gallery.addEventListener('focusin', () => { paused = true; });
    gallery.addEventListener('focusout', () => { paused = false; restart(); });
    track.addEventListener('touchstart', restart, { passive: true });

    const step = (i) => { go(i); restart(); };
    gallery.querySelector('.gallery-prev').addEventListener('click', () => step(current() - 1));
    gallery.querySelector('.gallery-next').addEventListener('click', () => step(current() + 1));
    dots.forEach((dot, i) => dot.addEventListener('click', () => step(i)));
    track.addEventListener('scroll', () => {
      const i = current();
      dots.forEach((dot, j) => dot.classList.toggle('is-active', i === j));
    }, { passive: true });
    restart();
  });

  // Prize pages: switch the ticket bundles between Sweepstakes and Raffle Plus
  document.querySelectorAll('[data-tier-switch]').forEach((box) => {
    const tabs = [...box.querySelectorAll('[data-tier]')];
    tabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        tabs.forEach((t) => t.setAttribute('aria-selected', String(t === tab)));
        box.querySelectorAll('[data-tier-panel]').forEach((panel) => {
          panel.hidden = panel.dataset.tierPanel !== tab.dataset.tier;
        });
      });
    });
  });

  // Sweepstakes / Raffle Plus entry forms (preview only): keep the summary
  // panel in step with the selected ticket bundle and prize.
  document.querySelectorAll('[data-entry]').forEach((form) => {
    const set = (key, text) => {
      const el = form.querySelector(`[data-sum="${key}"]`);
      if (el) el.textContent = text;
    };
    const prizeBoxes = [...form.querySelectorAll('input[type="checkbox"][name="prize"]')];
    const counter = form.querySelector('[data-prize-count]');
    // Each option's worth out of a full Raffle Plus prize of 2:
    // a car or $50,000 is 1, $100,000 is the whole prize.
    const weight = (box) => (box.dataset.kind === 'all' ? 2 : 1);
    const picked = () => prizeBoxes.filter((b) => b.checked);
    const total = () => picked().reduce((sum, b) => sum + weight(b), 0);

    // Raffle Plus: any two cars, or one car and $50,000, or $100,000 alone.
    prizeBoxes.forEach((box) => {
      box.addEventListener('change', () => {
        if (!box.checked) return;
        if (box.dataset.kind === 'all') {
          prizeBoxes.forEach((b) => { if (b !== box) b.checked = false; });
        } else {
          prizeBoxes.forEach((b) => { if (b.dataset.kind === 'all') b.checked = false; });
          if (total() > 2) {
            box.checked = false;
            if (counter) counter.textContent = 'Two prizes are already selected — unselect one to change it.';
            counter && counter.setAttribute('data-full', '1');
          }
        }
      });
    });

    const update = () => {
      const tickets = form.querySelector('input[name="tickets"]:checked');
      set('tickets', tickets ? tickets.dataset.label : 'Not selected yet');
      set('total', tickets ? `$${tickets.dataset.price}` : '—');
      const prizes = [...form.querySelectorAll('input[name="prize"]:checked')].map((i) => i.value);
      set('prize', prizes.length ? prizes.join(' + ') : 'Not selected yet');
      if (counter) {
        if (counter.getAttribute('data-full')) counter.removeAttribute('data-full');
        else if (total() === 2) counter.textContent = 'Selection complete.';
        else if (total() === 1) counter.textContent = 'One more to pick.';
        else counter.textContent = '';
      }
    };
    form.addEventListener('change', update);

    // Links from the prize pages arrive with ?tickets=3 or ?prize=Rivian%20R1T:
    // start the form with that bundle / car already chosen.
    const params = new URLSearchParams(location.search);
    const preset = (name, value) => {
      if (!value) return;
      const input = [...form.querySelectorAll(`input[name="${name}"]`)].find((i) => i.value === value);
      if (input) input.checked = true;
    };
    preset('tickets', params.get('tickets'));
    preset('prize', params.get('prize'));
    update();
  });
})();
