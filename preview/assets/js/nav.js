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
    update();
  });
})();
