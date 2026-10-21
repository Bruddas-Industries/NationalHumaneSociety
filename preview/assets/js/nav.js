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
      // Freeze the page behind the open menu so swipes scroll the menu only.
      document.documentElement.classList.toggle('menu-open', header.classList.contains('is-open'));
      toggle.setAttribute('aria-expanded', String(header.classList.contains('is-open')));
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

  // Loading states for embedded videos and posts: the paw loader fades out
  // when the iframe has loaded; after 10 s without that, it offers a link.
  // Instagram's script swaps its blockquote for an iframe later, so watch for it.
  function watchEmbed(box) {
    const done = () => { box.classList.add('is-loaded'); box.classList.remove('is-slow'); };
    const hook = (frame) => {
      frame.addEventListener('load', done, { once: true });
    };
    const frame = box.querySelector('iframe');
    if (frame) hook(frame);
    else {
      const mo = new MutationObserver(() => {
        const f = box.querySelector('iframe');
        if (f) { mo.disconnect(); hook(f); }
      });
      mo.observe(box, { childList: true, subtree: true });
    }
    // Start the 10 s clock only once the embed is on screen: lazy iframes
    // further down the page don't begin loading until they're scrolled to.
    const startClock = () => setTimeout(() => {
      if (!box.classList.contains('is-loaded')) box.classList.add('is-slow');
    }, 10000);
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((entries) => {
        if (entries.some((e) => e.isIntersecting)) { io.disconnect(); startClock(); }
      });
      io.observe(box);
    } else startClock();
  }
  document.querySelectorAll('[data-embed]').forEach(watchEmbed);

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

    // Thumbnails: show the play button and title once the image is in
    track.querySelectorAll('a.short-card').forEach((card) => {
      const img = card.querySelector('img');
      const ready = () => card.classList.add('thumb-ready');
      if (!img || (img.complete && img.naturalWidth)) ready();
      else { img.addEventListener('load', ready, { once: true }); img.addEventListener('error', ready, { once: true }); }
    });

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
        const loader = card.querySelector('.embed-loader');
        if (loader) player.appendChild(loader.cloneNode(true));
        player.appendChild(iframe);
        card.replaceWith(player);
        watchEmbed(player);
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

  // FAQ cards: ease the answer open and closed instead of snapping. The
  // <details> element still works on its own if this script doesn't run.
  document.querySelectorAll('.faq-card').forEach((card) => {
    const summary = card.querySelector('summary');
    const answer = card.querySelector('.faq-a');
    if (!summary || !answer) return;
    // Animate from the current height to the target; reading offsetHeight
    // between the two forces the start value to apply, so the motion begins
    // on the first frame.
    const animate = (from, to, done) => {
      card.classList.remove('is-animating');
      answer.style.height = from + 'px';
      answer.style.opacity = to ? '0' : '1';
      void answer.offsetHeight;
      card.classList.add('is-animating');
      answer.style.height = to + 'px';
      answer.style.opacity = to ? '1' : '0';
      let ended = false;
      const end = () => {
        if (ended) return;
        ended = true;
        if (done) done();
        card.classList.remove('is-animating');
        answer.style.height = '';
        answer.style.opacity = '';
      };
      answer.addEventListener('transitionend', (ev) => { if (ev.propertyName === 'height') end(); }, { once: true });
      setTimeout(end, 400);
    };
    summary.addEventListener('click', (e) => {
      if (reduceMotion || card.classList.contains('is-animating')) return;
      e.preventDefault();
      if (card.open) {
        animate(answer.offsetHeight, 0, () => { card.open = false; });
      } else {
        card.open = true;
        animate(0, answer.scrollHeight);
      }
    });
  });

  // Educational Messages: filter the article cards by category and show
  // them a page at a time ("Show more").
  document.querySelectorAll('[data-post-filter]').forEach((box) => {
    const cards = [...box.querySelectorAll('[data-post-grid] .post-card')];
    const chips = [...box.querySelectorAll('.filter-chip')];
    const more = box.querySelector('[data-show-more]');
    const pageSize = Number(box.dataset.pageSize) || 12;
    let filter = 'all';
    let shown = pageSize;
    const render = () => {
      const matching = cards.filter((c) => filter === 'all' || c.dataset.category === filter);
      cards.forEach((c) => { c.hidden = true; });
      matching.slice(0, shown).forEach((c) => { c.hidden = false; });
      if (more) {
        const left = Math.max(0, matching.length - shown);
        more.hidden = left === 0;
        more.textContent = `Show more articles (${left} more)`;
      }
    };
    chips.forEach((chip) => chip.addEventListener('click', () => {
      filter = chip.dataset.filter;
      shown = pageSize;
      chips.forEach((c) => {
        c.classList.toggle('is-active', c === chip);
        c.setAttribute('aria-pressed', String(c === chip));
      });
      render();
    }));
    if (more) more.addEventListener('click', () => {
      const total = cards.filter((c) => filter === 'all' || c.dataset.category === filter).length;
      shown = Math.min(shown + pageSize, total);
      render();
    });
    render();
  });

  // Instagram posts (Videos & More): open Instagram's own embed in a pop-up,
  // so videos play without leaving the page. Esc, the close button or a click
  // outside closes it.
  const igPosts = document.querySelectorAll('a.ig-post[data-ig]');
  if (igPosts.length) {
    const modal = document.createElement('div');
    modal.className = 'ig-modal';
    modal.hidden = true;
    modal.innerHTML = '<div class="ig-modal-box" role="dialog" aria-modal="true" aria-label="Instagram post">' +
      '<button type="button" class="ig-modal-close" aria-label="Close">×</button><div class="ig-modal-frame" data-embed></div></div>';
    document.body.appendChild(modal);
    const frameBox = modal.querySelector('.ig-modal-frame');
    let lastFocus = null;
    const close = () => {
      modal.hidden = true;
      frameBox.innerHTML = '';
      frameBox.classList.remove('is-loaded', 'is-slow');
      document.documentElement.classList.remove('menu-open');
      if (lastFocus) lastFocus.focus();
    };
    igPosts.forEach((post) => post.addEventListener('click', (e) => {
      e.preventDefault();
      lastFocus = post;
      const loader = post.querySelector('.embed-loader');
      frameBox.innerHTML = '';
      if (loader) frameBox.appendChild(loader.cloneNode(true));
      const iframe = document.createElement('iframe');
      iframe.src = `https://www.instagram.com/${post.dataset.ig}/embed/captioned/`;
      iframe.title = 'Instagram post';
      iframe.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      iframe.allowFullscreen = true;
      frameBox.appendChild(iframe);
      watchEmbed(frameBox);
      modal.hidden = false;
      document.documentElement.classList.add('menu-open');
      modal.querySelector('.ig-modal-close').focus();
    }));
    modal.addEventListener('click', (e) => { if (e.target === modal || e.target.closest('.ig-modal-close')) close(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !modal.hidden) close(); });
  }

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
