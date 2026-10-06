/**
 * Optional dark “stage” theme toggle (cookie + body class).
 */
(function (window, document) {
  'use strict';

  var COOKIE = 'sx_stage_theme';

  function readCookie() {
    var parts = (';.cookie || '').split(';');
    for (var i = 0; i < parts.length; i++) {
      var p = parts[i].replace(/^\s+|\s+$/g, '');
      if (p.indexOf(COOKIE + '=') === 0) return p.substring(COOKIE.length + 1);
    }
    return 'light';
  }

  function apply(theme) {
    var dark = theme === 'dark';
    document.documentElement.classList.toggle('ux-stage-dark', dark);
    document.body.classList.toggle('ux-stage-dark', dark);
    var btn = document.getElementById('ux-theme-toggle');
    if (btn) {
      btn.setAttribute('aria-pressed', dark ? 'true' : 'false');
      btn.title = dark ? btn.getAttribute('data-label-light') : btn.getAttribute('data-label-dark');
      var icon = btn.querySelector('i');
      if (icon) {
        icon.className = dark ? 'fa fa-sun-o' : 'fa fa-moon-o';
      }
    }
  }

  function setTheme(theme) {
    apply(theme);
    var maxAge = 60 * 60 * 24 * 365;
    document.cookie = COOKIE + '=' + theme + ';path=/;max-age=' + maxAge + ';SameSite=Lax';
    var form = document.getElementById('ux-theme-form');
    if (form) {
      var input = form.querySelector('input[name="theme"]');
      if (input) input.value = theme;
      // fire-and-forget server sync; navigation not required
      try {
        var fd = new FormData(form);
        if (window.fetch) {
          fetch(form.action, { method: 'POST', body: fd, credentials: 'same-origin' });
        }
      } catch (e) { /* ignore */ }
    }
  }

  function toggle() {
    setTheme(readCookie() === 'dark' ? 'light' : 'dark');
  }

  document.addEventListener('DOMContentLoaded', function () {
    apply(readCookie());
    var btn = document.getElementById('ux-theme-toggle');
    if (btn) {
      btn.addEventListener('click', function (ev) {
        ev.preventDefault();
        toggle();
      });
    }
  });

  window.ScriptumXTheme = { apply: apply, setTheme: setTheme, toggle: toggle };
})(window, document);
