/**
 * Mobile shot checklist — tap rows to cycle progress_shot.
 */
(function (window, document) {
  'use strict';

  function csrfToken() {
    var el = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (el) return el.value;
    var match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
  }

  function updateRow(row, progress) {
    row.setAttribute('data-progress', String(progress));
    row.classList.toggle('is-done', progress >= 100);
    row.classList.toggle('is-partial', progress > 0 && progress < 100);
    var bar = row.querySelector('.ux-check-bar-fill');
    if (bar) bar.style.width = progress + '%';
    var pct = row.querySelector('.ux-check-pct');
    if (pct) pct.textContent = progress + '%';
    var mark = row.querySelector('.ux-check-mark');
    if (mark) {
      mark.innerHTML =
        progress >= 100
          ? '<i class="fa fa-check-square-o"></i>'
          : progress > 0
            ? '<i class="fa fa-minus-square-o"></i>'
            : '<i class="fa fa-square-o"></i>';
    }
  }

  function postProgress(row) {
    var url = row.getAttribute('data-progress-url');
    if (!url || !window.fetch) return;
    row.classList.add('is-busy');
    fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken(),
      },
      body: '{}',
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (data && data.ok) updateRow(row, data.progress_shot);
      })
      .finally(function () {
        row.classList.remove('is-busy');
      });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var list = document.getElementById('ux-shot-checklist');
    if (!list) return;
    list.addEventListener('click', function (ev) {
      var row = ev.target.closest('.ux-check-row');
      if (!row || !list.contains(row)) return;
      ev.preventDefault();
      postProgress(row);
    });
  });
})(window, document);
