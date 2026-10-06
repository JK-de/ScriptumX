/* ScriptumX editor safety: autosave indicator + conflict warning */
(function ($) {
  'use strict';

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = $.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function setStatus($el, text, cls) {
    if (!$el.length) return;
    $el.removeClass('text-muted text-success text-danger text-warning').addClass(cls || 'text-muted');
    $el.text(text);
  }

  function initEditorSafety(options) {
    var $form = $(options.formSelector);
    if (!$form.length || !options.autosaveUrl) return;

    var $status = $(options.statusSelector);
    var $expected = $form.find('input[name="expected_updated_at"]');
    var $conflict = $(options.conflictSelector);
    var $force = $form.find('input[name="force_save"]');
    var timer = null;
    var dirty = false;
    var saving = false;

    setStatus($status, 'Ready', 'text-muted');

    $form.on('input change', 'input, textarea, select', function () {
      dirty = true;
      setStatus($status, 'Unsaved changes…', 'text-warning');
      if (timer) clearTimeout(timer);
      timer = setTimeout(doAutosave, options.delayMs || 1500);
    });

    function doAutosave() {
      if (!dirty || saving) return;
      saving = true;
      setStatus($status, 'Saving…', 'text-muted');

      var data = $form.serialize();
      $.ajax({
        url: options.autosaveUrl,
        method: 'POST',
        data: data,
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
      }).done(function (resp) {
        dirty = false;
        if (resp && resp.updated_at) {
          $expected.val(resp.updated_at);
        }
        $conflict.hide().text('');
        $force.prop('checked', false);
        setStatus($status, 'Saved', 'text-success');
      }).fail(function (xhr) {
        if (xhr.status === 409) {
          var msg = (xhr.responseJSON && xhr.responseJSON.message) || 'Conflict detected';
          $conflict.show().text(msg);
          setStatus($status, 'Conflict', 'text-danger');
          if (xhr.responseJSON && xhr.responseJSON.updated_at) {
            // keep expected_updated_at stale so manual force is explicit
          }
        } else {
          setStatus($status, 'Autosave failed', 'text-danger');
        }
      }).always(function () {
        saving = false;
      });
    }

    // Expose for tests / manual trigger
    window.ScriptumXEditorSafety = window.ScriptumXEditorSafety || {};
    window.ScriptumXEditorSafety.saveNow = doAutosave;
  }

  window.ScriptumXEditorSafety = {
    init: initEditorSafety,
  };
})(jQuery);
