"""
UX endpoints: language toggle, theme cookie, presence heartbeat, shot checklist.
"""
from __future__ import annotations

import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from X.common import Env, g_tab_list
from X.models import Scene
from X.ux import (
    THEME_COOKIE,
    THEME_COOKIE_MAX_AGE,
    format_presence_label,
    presence_heartbeat,
    project_has_multi_users,
    theme_from_request,
)

###############################################################################


@login_required
@require_POST
def set_language(request):
    """Session/cookie language switch for DE/EN chrome."""
    lang = (request.POST.get('language') or request.GET.get('language') or '').strip().lower()
    if lang.startswith('de'):
        lang = 'de'
    elif lang.startswith('en'):
        lang = 'en'
    else:
        lang = translation.get_language() or 'de'

    translation.activate(lang)
    request.session['django_language'] = lang
    next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER') or '/'
    response = HttpResponseRedirect(next_url)
    response.set_cookie('django_language', lang, max_age=THEME_COOKIE_MAX_AGE)
    return response


@login_required
@require_POST
def set_theme(request):
    theme = (request.POST.get('theme') or '').strip().lower()
    if theme not in ('dark', 'light'):
        theme = 'light'
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    response = HttpResponseRedirect(next_url)
    response.set_cookie(THEME_COOKIE, theme, max_age=THEME_COOKIE_MAX_AGE)
    return response


@login_required
@require_http_methods(['GET', 'POST'])
def presence(request):
    env = Env(request)
    if not env.project or not project_has_multi_users(env.project):
        return JsonResponse({'enabled': False, 'others': []})

    if request.method == 'POST':
        try:
            payload = json.loads(request.body.decode('utf-8') or '{}')
        except (TypeError, ValueError, UnicodeDecodeError):
            payload = {}
        label = payload.get('label') or ''
        scene_id = payload.get('scene_id') or env.scene_id or None
        path = payload.get('path') or request.META.get('HTTP_REFERER') or request.path
        scene = None
        if scene_id:
            try:
                scene = Scene.objects.get(pk=int(scene_id), project=env.project)
            except (Scene.DoesNotExist, TypeError, ValueError):
                scene = env.scene
        else:
            scene = env.scene
        if not label:
            label = format_presence_label(scene=scene)
        others = presence_heartbeat(
            env.project,
            request.user,
            label=label,
            scene_id=getattr(scene, 'id', None),
            path=path,
        )
    else:
        others = presence_heartbeat(
            env.project,
            request.user,
            label=format_presence_label(scene=env.scene),
            scene_id=env.scene_id or None,
            path=request.path,
        )

    return JsonResponse({
        'enabled': True,
        'others': [
            {
                'username': o.get('username'),
                'label': o.get('label'),
                'scene_id': o.get('scene_id'),
            }
            for o in others
        ],
    })


###############################################################################


@login_required
@require_GET
def shot_checklist(request):
    """Mobile-friendly on-set checklist driven by Scene.progress_shot."""
    env = Env(request)
    scenes = []
    if env.project_id and env.script_id:
        scenes = list(
            Scene.objects.filter(project=env.project_id, script=env.script_id).order_by('order')
        )

    return render(request, 'X/shot_checklist.html', {
        'title': _('Shot checklist'),
        'env': env,
        'tab_list': g_tab_list,
        'tab_active_id': 'H',
        'scenes': scenes,
        'ux_theme': theme_from_request(request),
        'presence_enabled': project_has_multi_users(env.project),
    })


@login_required
@require_POST
def shot_checklist_progress(request, scene_id):
    env = Env(request)
    try:
        scene = Scene.objects.get(pk=scene_id, project=env.project_id, script=env.script_id)
    except Scene.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'not_found'}, status=404)

    raw = request.POST.get('progress_shot')
    if raw is None and request.body:
        try:
            raw = json.loads(request.body.decode('utf-8')).get('progress_shot')
        except (TypeError, ValueError, UnicodeDecodeError):
            raw = None

    if raw is None:
        # cycle: 0 -> 50 -> 100 -> 0
        current = int(scene.progress_shot or 0)
        if current < 50:
            scene.progress_shot = 50
        elif current < 100:
            scene.progress_shot = 100
        else:
            scene.progress_shot = 0
    else:
        try:
            value = int(raw)
        except (TypeError, ValueError):
            return JsonResponse({'ok': False, 'error': 'bad_value'}, status=400)
        scene.progress_shot = max(0, min(100, value))

    scene.save(update_fields=['progress_shot'])
    return JsonResponse({
        'ok': True,
        'scene_id': scene.id,
        'progress_shot': scene.progress_shot,
        'done': scene.progress_shot >= 100,
    })
