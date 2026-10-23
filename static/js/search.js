(function () {
  var input = document.getElementById('search-input');
  if (!input) return;

  var list = document.getElementById('search-results');
  var status = document.getElementById('search-status');
  var indexPromise = null;
  var timer = null;

  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch(input.dataset.index).then(function (r) { return r.json(); });
    }
    return indexPromise;
  }

  function escapeRegExp(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

  function count(haystack, term) {
    var n = 0, i = haystack.indexOf(term);
    while (i !== -1 && n < 5) { n++; i = haystack.indexOf(term, i + term.length); }
    return n;
  }

  function score(entry, terms) {
    var title = entry.title.toLowerCase();
    var tags = entry.tags.join(' ').toLowerCase();
    var excerpt = entry.excerpt.toLowerCase();
    var body = entry.body.toLowerCase();
    var total = 0;
    for (var i = 0; i < terms.length; i++) {
      var t = terms[i];
      var s = (title.indexOf(t) !== -1 ? 10 : 0) + (tags.indexOf(t) !== -1 ? 6 : 0) +
              (excerpt.indexOf(t) !== -1 ? 3 : 0) + count(body, t);
      if (s === 0) return 0;
      total += s;
    }
    return total;
  }

  function snippet(entry, terms) {
    var lower = entry.body.toLowerCase();
    var at = -1;
    for (var i = 0; i < terms.length && at === -1; i++) at = lower.indexOf(terms[i]);
    if (at === -1) return entry.excerpt;
    var start = Math.max(0, at - 60);
    var end = Math.min(entry.body.length, at + 140);
    return (start > 0 ? '...' : '') + entry.body.slice(start, end) + (end < entry.body.length ? '...' : '');
  }

  // Builds text and <mark> nodes via the DOM, so post content is never parsed as HTML.
  function appendHighlighted(el, text, re) {
    var parts = text.split(re);
    for (var i = 0; i < parts.length; i++) {
      if (!parts[i]) continue;
      if (i % 2 === 1) {
        var m = document.createElement('mark');
        m.textContent = parts[i];
        el.appendChild(m);
      } else {
        el.appendChild(document.createTextNode(parts[i]));
      }
    }
  }

  function render(entries, terms) {
    list.textContent = '';
    var re = new RegExp('(' + terms.map(escapeRegExp).join('|') + ')', 'gi');
    entries.forEach(function (entry) {
      var li = document.createElement('li');
      li.className = 'result';

      var h = document.createElement('h3');
      var a = document.createElement('a');
      a.href = entry.url;
      appendHighlighted(a, entry.title, re);
      h.appendChild(a);
      li.appendChild(h);

      if (entry.tags.length) {
        var tg = document.createElement('p');
        tg.className = 'meta';
        tg.textContent = entry.tags.map(function (t) { return '#' + t; }).join(' ');
        li.appendChild(tg);
      }

      var p = document.createElement('p');
      appendHighlighted(p, snippet(entry, terms), re);
      li.appendChild(p);
      list.appendChild(li);
    });
  }

  function run() {
    var query = input.value.trim();
    var terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    if (history.replaceState) {
      history.replaceState(null, '', query ? '?q=' + encodeURIComponent(query) : location.pathname);
    }
    if (!terms.length) {
      list.textContent = '';
      status.textContent = '';
      return;
    }
    loadIndex().then(function (index) {
      var hits = index
        .map(function (entry) { return { entry: entry, score: score(entry, terms) }; })
        .filter(function (h) { return h.score > 0; })
        .sort(function (a, b) { return b.score - a.score || (a.entry.date < b.entry.date ? 1 : -1); })
        .map(function (h) { return h.entry; });
      render(hits, terms);
      status.textContent = hits.length
        ? hits.length + (hits.length === 1 ? ' result' : ' results')
        : 'No posts match "' + query + '".';
    }).catch(function () {
      status.textContent = 'Could not load the search index.';
    });
  }

  input.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(run, 120);
  });
  input.form.addEventListener('submit', function (e) { e.preventDefault(); run(); });

  var initial = new URLSearchParams(location.search).get('q');
  if (initial) { input.value = initial; run(); }
})();
