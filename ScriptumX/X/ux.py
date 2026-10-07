"""
UX helpers for presence, theme cookie, and shot-checklist progress.
"""
from __future__ import annotations

import time
from typing import Any

from django.core.cache import cache
from django.utils.translation import gettext as _

PRESENCE_TTL = 45
PRESENCE_STALE = 35
THEME_COOKIE = 'sx_stage_theme'
THEME_COOKIE_MAX_AGE = 60 * 60 * 24 * 365


def project_has_multi_users(project) -> bool:
    if not project:
        return False
    # Prefer memberships (source of truth); fall back to legacy users M2M.
    try:
        if project.memberships.count() > 1:
            return True
    except Exception:
        pass
    return project.users.count() > 1


def presence_cache_key(project_id: int) -> str:
    return f'sx_presence:{project_id}'


def presence_heartbeat(project, user, *, label: str = '', scene_id=None, path: str = '') -> list[dict[str, Any]]:
    """Record this user and return other active users for the project."""
    if not project or not user or not user.is_authenticated:
        return []
    if not project_has_multi_users(project):
        return []

    key = presence_cache_key(project.id)
    now = time.time()
    bucket = cache.get(key) or {}

    bucket[str(user.id)] = {
        'user_id': user.id,
        'username': user.get_username(),
        'label': (label or '')[:120],
        'scene_id': scene_id,
        'path': (path or '')[:200],
        'ts': now,
    }

    active = {}
    others = []
    for uid, entry in bucket.items():
        if now - float(entry.get('ts', 0)) > PRESENCE_STALE:
            continue
        active[uid] = entry
        if int(entry.get('user_id', 0)) != user.id:
            others.append(entry)

    cache.set(key, active, PRESENCE_TTL)
    others.sort(key=lambda e: e.get('username') or '')
    return others


def format_presence_label(scene=None, tab: str = '') -> str:
    if scene is not None:
        short = (getattr(scene, 'short', '') or '').strip()
        name = (getattr(scene, 'name', '') or '').strip()
        if short:
            return _('editing Scene %(short)s') % {'short': short}
        if name:
            return _('editing %(name)s') % {'name': name[:40]}
        return _('editing a scene')
    if tab:
        return _('viewing %(tab)s') % {'tab': tab}
    return _('online')


def theme_from_request(request) -> str:
    raw = request.COOKIES.get(THEME_COOKIE, '')
    if raw == 'dark':
        return 'dark'
    return 'light'
