// Mobile menu toggle + active-link highlighting + preview-flag dismissal
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

  const header = document.querySelector('.site-header');
  const toggle = document.querySelector('.menu-toggle');
  if (toggle && header) {
    toggle.addEventListener('click', () => header.classList.toggle('is-open'));
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
