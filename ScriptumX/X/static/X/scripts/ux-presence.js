/**
 * Multi-user presence heartbeat (only when server enables it).
 */
(function (window, document) {
  'use strict';

  function csrfToken() {
    var el = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (el) return el.value;
    var match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
  }

  function render(others) {
    var host = document.getElementById('ux-presence');
    if (!host) return;
    if (!others || !others.length) {
      host.hidden = true;
      host.innerHTML = '';
      return;
    }
    host.hidden = false;
    host.innerHTML = others
      .map(function (o) {
        var label = o.label || 'online';
        return (
          '<span class="ux-presence-pill" title="' +
          (o.username || '') +
          '">' +
          '<i class="fa fa-circle"></i> ' +
          (o.username || '?') +
          ' · ' +
          label +
          '</span>'
        );
      })
      .join(' ');
  }

  function beat() {
    var cfg = window.ScriptumXPresence || {};
    if (!cfg.enabled || !cfg.url) return;
    var body = JSON.stringify({
      label: cfg.label || '',
      scene_id: cfg.sceneId || null,
      path: window.location.pathname,
    });
    if (!window.fetch) return;
    fetch(cfg.url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken(),
      },
      body: body,
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (!data || !data.enabled) {
          render([]);
          return;
        }
        render(data.others || []);
      })
      .catch(function () { /* ignore */ });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var cfg = window.ScriptumXPresence || {};
    if (!cfg.enabled) return;
    beat();
    window.setInterval(beat, 15000);
  });
})(window, document);
