(function () {
  // ---- site search (client side, over /index.json) ----
  var form = document.getElementById('search-form');
  if (!form) return;
  var input = document.getElementById('search-input');
  var status = document.getElementById('search-status');
  var list = document.getElementById('search-results');
  var index = null;

  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function hl(s, q) { return esc(s).replace(new RegExp('(' + q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig'), '<mark>$1</mark>'); }

  function run(q) {
    q = (q || '').trim();
    list.innerHTML = '';
    if (!q) { status.textContent = ''; return; }
    var lq = q.toLowerCase();
    var hits = index.filter(function (it) {
      return (it.title + ' ' + it.gloss + ' ' + it.content + ' ' + (it.tags || []).join(' ')).toLowerCase().indexOf(lq) >= 0;
    }).sort(function (a, b) {
      var at = a.title.toLowerCase().indexOf(lq) >= 0 ? 0 : 1, bt = b.title.toLowerCase().indexOf(lq) >= 0 ? 0 : 1;
      return at - bt;
    });
    status.textContent = hits.length ? '找到 ' + hits.length + ' 个词' : '没有找到「' + q + '」';
    hits.forEach(function (it) {
      var i = it.content.toLowerCase().indexOf(lq), snip = '';
      if (i >= 0) snip = (i > 60 ? '…' : '') + it.content.substr(Math.max(0, i - 60), 160) + '…';
      var li = document.createElement('li');
      li.innerHTML = '<a href="' + it.url + '"><b>' + hl(it.title, q) + '</b></a> <span class="gloss">' + hl(it.gloss, q) + '</span>' +
        (snip ? '<div class="snippet">' + hl(snip, q) + '</div>' : '');
      list.appendChild(li);
    });
  }

  function load(cb) {
    if (index) return cb();
    status.textContent = '加载索引…';
    fetch(form.getAttribute('data-index')).then(function (r) { return r.json(); }).then(function (d) {
      var ta = document.createElement('textarea');
      index = d.map(function (it) { ta.innerHTML = it.content; it.content = ta.value; ta.innerHTML = ta.value; it.content = ta.value; return it; });
      cb();
    });
  }

  form.addEventListener('submit', function (e) { e.preventDefault(); load(function () { run(input.value); }); });
  input.addEventListener('input', function () { if (index) run(input.value); });

  var q = new URLSearchParams(location.search).get('q');
  if (q) { input.value = q; load(function () { run(q); }); }
})();
