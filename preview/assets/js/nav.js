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

  // Donate widget interactions (preview only)
  document.querySelectorAll('.donate-widget').forEach((widget) => {
    widget.querySelectorAll('.amount-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        widget.querySelectorAll('.amount-btn').forEach((b) => b.classList.remove('is-active'));
        btn.classList.add('is-active');
      });
    });
    widget.querySelectorAll('.donate-toggle button').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        widget.querySelectorAll('.donate-toggle button').forEach((b) => b.classList.remove('is-active'));
        btn.classList.add('is-active');
      });
    });
  });
})();
