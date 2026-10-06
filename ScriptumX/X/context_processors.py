"""Template context for UX chrome (theme, presence, language)."""
from django.conf import settings
from django.utils import translation

from X.common import Env
from X.ux import project_has_multi_users, theme_from_request


def ux_chrome(request):
    theme = theme_from_request(request)
    presence_enabled = False
    scene_id = None
    presence_label = ''
    try:
        if getattr(request, 'user', None) and request.user.is_authenticated:
            env = Env(request)
            presence_enabled = project_has_multi_users(env.project)
            scene_id = env.scene_id or None
            if env.scene:
                short = (env.scene.short or '').strip()
                presence_label = short or (env.scene.name or '')[:40]
    except Exception:
        # Never break page render for chrome prefs
        pass

    return {
        'ux_theme': theme,
        'presence_enabled': presence_enabled,
        'presence_scene_id': scene_id,
        'presence_label': presence_label,
        'ux_languages': getattr(settings, 'LANGUAGES', (('de', 'Deutsch'), ('en', 'English'))),
        'ux_language': translation.get_language() or settings.LANGUAGE_CODE,
    }
