/**
 * Keyboard-first navigation for Script / Scene lists.
 * j/k — previous/next list item
 * a   — new Action after selected (scene editor)
 * d   — new Dialog after selected (scene editor)
 * ?   — toggle shortcut hint
 */
(function (window, document) {
  'use strict';

  function isTypingTarget(el) {
    if (!el) return false;
    var tag = (el.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea' || tag === 'select') return true;
    if (el.isContentEditable) return true;
    return false;
  }

  function listItems() {
    return Array.prototype.slice.call(
      document.querySelectorAll('#app_container a.list-group-item[href]')
    );
  }

  function selectedIndex(items) {
    var selected = document.getElementById('selected_scope');
    if (!selected) return -1;
    for (var i = 0; i < items.length; i++) {
      if (items[i] === selected || items[i].contains(selected)) return i;
    }
    return -1;
  }

  function go(delta) {
    var items = listItems();
    if (!items.length) return;
    var idx = selectedIndex(items);
    var next = idx < 0 ? (delta > 0 ? 0 : items.length - 1) : idx + delta;
    if (next < 0 || next >= items.length) return;
    var href = items[next].getAttribute('href');
    if (href) window.location.href = href;
  }

  function insertAfter(type) {
    var selected = document.getElementById('selected_scope');
    if (!selected) return;
    var href = selected.getAttribute('href') || '';
    var match = href.match(/\/scene\/(\d+)/);
    if (!match) return;
    window.location.href = '/scene/new/' + type + '/' + match[1] + '/1';
  }

  function ensureHint() {
    var hint = document.getElementById('ux-kb-hint');
    if (hint) return hint;
    hint = document.createElement('div');
    hint.id = 'ux-kb-hint';
    hint.className = 'ux-kb-hint';
    hint.setAttribute('role', 'status');
    hint.hidden = true;
    hint.innerHTML =
      '<strong>Keyboard</strong> · <kbd>j</kbd>/<kbd>k</kbd> nav · ' +
      '<kbd>a</kbd> action · <kbd>d</kbd> dialog · <kbd>?</kbd> hide';
    document.body.appendChild(hint);
    return hint;
  }

  function toggleHint() {
    var hint = ensureHint();
    hint.hidden = !hint.hidden;
  }

  document.addEventListener('keydown', function (ev) {
    if (ev.defaultPrevented || ev.metaKey || ev.ctrlKey || ev.altKey) return;
    if (isTypingTarget(ev.target)) return;

    var key = ev.key;
    if (key === 'j' || key === 'J') {
      ev.preventDefault();
      go(1);
    } else if (key === 'k' || key === 'K') {
      ev.preventDefault();
      go(-1);
    } else if (key === 'a' || key === 'A') {
      if (document.body.getAttribute('data-ux-page') === 'scene') {
        ev.preventDefault();
        insertAfter('A');
      }
    } else if (key === 'd' || key === 'D') {
      if (document.body.getAttribute('data-ux-page') === 'scene') {
        ev.preventDefault();
        insertAfter('D');
      }
    } else if (key === '?' || (ev.shiftKey && key === '/')) {
      ev.preventDefault();
      toggleHint();
    }
  });
})(window, document);
