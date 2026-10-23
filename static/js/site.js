(function () {
  var root = document.documentElement;
  var meta = document.querySelector('meta[name="theme-color"]');

  var toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      root.setAttribute('data-theme', next);
      if (meta) meta.content = next === 'light' ? '#f6f8fb' : '#0b0f14';
      try { localStorage.setItem('theme', next); } catch (e) {}
    });
  }

  var header = document.getElementById('site-header');
  var navToggle = document.getElementById('nav-toggle');
  if (header && navToggle) {
    function setOpen(open) {
      header.setAttribute('data-nav-open', open ? 'true' : 'false');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    navToggle.addEventListener('click', function () {
      setOpen(header.getAttribute('data-nav-open') !== 'true');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
  }
})();
