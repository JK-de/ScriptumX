"""Project membership, role presets, and central can() helper."""

from __future__ import annotations

import re
from typing import Optional

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404

TAB_KEYS = (
    'project',
    'script',
    'scene',
    'shot',
    'role',
    'person',
    'time',
    'location',
    'gadget',
    'audio',
    'sfx',
    'scheduler',
    'plan',
    'reports',
)

# Navbar tab id → permission key
TAB_ID_TO_KEY = {
    'P': 'project',
    'C': 'script',
    'S': 'scene',
    'H': 'shot',
    'R': 'role',
    'L': 'location',
    'T': 'time',
    'F': 'person',
    'G': 'gadget',
    'X': 'sfx',
    'A': 'audio',
    'B': 'plan',
}

ROLE_ACTOR = 'actor'
ROLE_WRITER = 'writer'
ROLE_CREW = 'crew'
ROLE_DIRECTOR = 'director'
ROLE_PRODUCER = 'producer'

ROLE_CHOICES = (
    (ROLE_ACTOR, 'Actor'),
    (ROLE_WRITER, 'Writer'),
    (ROLE_CREW, 'Crew'),
    (ROLE_DIRECTOR, 'Director'),
    (ROLE_PRODUCER, 'Producer'),
)

# Presets producers may assign (below producer).
PRODUCER_ASSIGNABLE_ROLES = (ROLE_ACTOR, ROLE_WRITER, ROLE_CREW)

ROLE_RANK = {
    ROLE_ACTOR: 10,
    ROLE_WRITER: 20,
    ROLE_CREW: 25,
    ROLE_DIRECTOR: 30,
    ROLE_PRODUCER: 40,
}


def _flags(**pairs):
    """Build a full permissions dict; unspecified tabs are False/False."""
    out = {tab: {'read': False, 'edit': False} for tab in TAB_KEYS}
    for tab, (read, edit) in pairs.items():
        out[tab] = {'read': bool(read), 'edit': bool(edit)}
    return out


def _all_tabs(read=True, edit=True, person_edit=None):
    flags = {tab: {'read': read, 'edit': edit} for tab in TAB_KEYS}
    if person_edit is not None:
        flags['person'] = {'read': read, 'edit': bool(person_edit)}
    return flags


ROLE_PRESETS = {
    ROLE_ACTOR: _flags(
        script=(True, False),
        scene=(True, False),
        reports=(True, False),  # PDF when Script read is on
    ),
    ROLE_WRITER: _flags(
        script=(True, True),
        scene=(True, True),
        role=(True, False),
        reports=(True, False),
    ),
    ROLE_CREW: _flags(
        shot=(True, True),
        location=(True, True),
        time=(True, True),
        gadget=(True, True),
        audio=(True, True),
        sfx=(True, True),
        script=(True, False),
        scene=(True, False),
        reports=(True, False),
    ),
    ROLE_DIRECTOR: _all_tabs(read=True, edit=True, person_edit=False),
    ROLE_PRODUCER: _all_tabs(read=True, edit=True, person_edit=True),
}


def empty_permissions():
    return {tab: {'read': False, 'edit': False} for tab in TAB_KEYS}


def permissions_for_role(role: str) -> dict:
    base = ROLE_PRESETS.get(role) or empty_permissions()
    # Deep copy
    return {tab: dict(flags) for tab, flags in base.items()}


def normalize_permissions(raw) -> dict:
    out = empty_permissions()
    if not isinstance(raw, dict):
        return out
    for tab in TAB_KEYS:
        src = raw.get(tab) or {}
        if isinstance(src, dict):
            out[tab] = {
                'read': bool(src.get('read')),
                'edit': bool(src.get('edit')),
            }
    return out


def get_membership(user, project):
    if not user or not getattr(user, 'is_authenticated', False) or not project:
        return None
    from X.models import ProjectMembership
    try:
        return ProjectMembership.objects.get(project=project, user=user)
    except ProjectMembership.DoesNotExist:
        return None


def user_is_site_admin(user) -> bool:
    return bool(user and getattr(user, 'is_authenticated', False) and user.is_superuser)


def projects_for_user(user):
    """Projects visible to user (membership or site admin)."""
    from X.models import Project
    if not user or not getattr(user, 'is_authenticated', False):
        return Project.objects.none()
    if user_is_site_admin(user):
        return Project.objects.all()
    return Project.objects.filter(memberships__user=user).distinct()


def can(user, project, tab: str, write: bool = False) -> bool:
    """Central access check used by Env and views."""
    if tab not in TAB_KEYS:
        return False
    if not project:
        return False
    if user_is_site_admin(user):
        return True
    # Share-link guests: Env sets read_only; handled separately via can_share
    membership = get_membership(user, project)
    if not membership:
        # Legacy fallback while migrating / if sync lagged
        if project.owner_id == getattr(user, 'id', None):
            flags = permissions_for_role(ROLE_PRODUCER)
        elif user and project.users.filter(pk=user.id).exists():
            flags = permissions_for_role(ROLE_CREW)
        elif user and project.guests.filter(pk=user.id).exists():
            flags = permissions_for_role(ROLE_ACTOR)
        else:
            return False
    else:
        flags = membership.effective_permissions()
    cell = flags.get(tab) or {}
    if write:
        return bool(cell.get('edit'))
    return bool(cell.get('read') or cell.get('edit'))


def can_invite(user, project) -> bool:
    if user_is_site_admin(user):
        return True
    membership = get_membership(user, project)
    if not membership:
        return bool(project and project.owner_id == getattr(user, 'id', None))
    return bool(membership.can_invite or membership.role == ROLE_PRODUCER)


def can_export_backup(user, project) -> bool:
    """Full project backup requires project edit or owner (not actors)."""
    if user_is_site_admin(user):
        return True
    if project and project.owner_id == getattr(user, 'id', None):
        return True
    return can(user, project, 'project', write=True)


def can_create_share(user, project, tab: str) -> bool:
    """Share-link creation requires matching read right on the report tab."""
    return can(user, project, tab, write=False)


def apply_preset_to_membership(membership, role: str, overrides: Optional[dict] = None):
    membership.role = role
    membership.permissions = permissions_for_role(role)
    if overrides:
        merged = normalize_permissions(membership.permissions)
        for tab, flags in normalize_permissions(overrides).items():
            if flags['read'] or flags['edit']:
                merged[tab] = flags
            # Allow explicit override of False only when key present in overrides
            if tab in (overrides or {}):
                merged[tab] = {
                    'read': bool((overrides[tab] or {}).get('read')),
                    'edit': bool((overrides[tab] or {}).get('edit')),
                }
        membership.permissions = merged
    membership.can_invite = role == ROLE_PRODUCER
    membership.save()
    sync_legacy_m2m(membership.project)
    return membership


def ensure_membership(project, user, role: str, overrides=None):
    from X.models import ProjectMembership
    membership, _created = ProjectMembership.objects.get_or_create(
        project=project,
        user=user,
        defaults={
            'role': role,
            'permissions': permissions_for_role(role),
            'can_invite': role == ROLE_PRODUCER,
        },
    )
    apply_preset_to_membership(membership, role, overrides)
    return membership


def sync_legacy_m2m(project):
    """Keep Project.owner / users / guests in sync with memberships."""
    from X.models import ProjectMembership
    memberships = list(
        ProjectMembership.objects.filter(project=project).select_related('user')
    )
    if not memberships:
        return

    producers = [m for m in memberships if m.role == ROLE_PRODUCER]
    if producers:
        # Prefer current owner if still a producer; else first producer.
        owner_ids = {m.user_id for m in producers}
        if project.owner_id not in owner_ids:
            project.owner = producers[0].user
            project.save(update_fields=['owner'])

    crew_like = {
        m.user_id
        for m in memberships
        if m.role in (ROLE_CREW, ROLE_WRITER, ROLE_DIRECTOR, ROLE_PRODUCER)
    }
    actors = {m.user_id for m in memberships if m.role == ROLE_ACTOR}
    # Owner always in users for legacy UX helpers
    if project.owner_id:
        crew_like.add(project.owner_id)

    User = get_user_model()
    project.users.set(User.objects.filter(pk__in=crew_like))
    project.guests.set(User.objects.filter(pk__in=actors))


def deactivate_user(user):
    """Admin deactivate: strip memberships and set inactive."""
    from X.models import ProjectMembership
    ProjectMembership.objects.filter(user=user).delete()
    user.is_active = False
    user.save(update_fields=['is_active'])


def assignable_roles_for(actor_user, project):
    """Roles the acting user may grant on this project."""
    if user_is_site_admin(actor_user):
        return [r[0] for r in ROLE_CHOICES]
    if can_invite(actor_user, project):
        membership = get_membership(actor_user, project)
        if membership and membership.role == ROLE_PRODUCER:
            return list(PRODUCER_ASSIGNABLE_ROLES)
        if user_is_site_admin(actor_user):
            return [r[0] for r in ROLE_CHOICES]
        return list(PRODUCER_ASSIGNABLE_ROLES)
    return []


# --- Path → tab mapping for middleware enforcement ---

_PATH_TAB_RULES = (
    (re.compile(r'^/person'), 'person'),
    (re.compile(r'^/p/\d+/s/\d+/person'), 'person'),
    (re.compile(r'^/planner'), 'plan'),
    (re.compile(r'^/p/\d+/s/\d+/planner'), 'plan'),
    (re.compile(r'^/scheduler'), 'scheduler'),
    (re.compile(r'^/p/\d+/s/\d+/scheduler'), 'scheduler'),
    (re.compile(r'^/script'), 'script'),
    (re.compile(r'^/p/\d+/s/\d+/script'), 'script'),
    (re.compile(r'^/scene'), 'scene'),
    (re.compile(r'^/p/\d+/s/\d+/scene'), 'scene'),
    (re.compile(r'^/shot'), 'shot'),
    (re.compile(r'^/p/\d+/s/\d+/shot'), 'shot'),
    (re.compile(r'^/role'), 'role'),
    (re.compile(r'^/p/\d+/s/\d+/role'), 'role'),
    (re.compile(r'^/location'), 'location'),
    (re.compile(r'^/p/\d+/s/\d+/location'), 'location'),
    (re.compile(r'^/time'), 'time'),
    (re.compile(r'^/p/\d+/s/\d+/time'), 'time'),
    (re.compile(r'^/gadget'), 'gadget'),
    (re.compile(r'^/p/\d+/s/\d+/gadget'), 'gadget'),
    (re.compile(r'^/audio'), 'audio'),
    (re.compile(r'^/p/\d+/s/\d+/audio'), 'audio'),
    (re.compile(r'^/sfx'), 'sfx'),
    (re.compile(r'^/p/\d+/s/\d+/sfx'), 'sfx'),
    (re.compile(r'^/project'), 'project'),
    # Script PDF: Script read
    (re.compile(r'^/report/S/'), 'script'),
    (re.compile(r'^/p/\d+/s/\d+/report/S/'), 'script'),
    # Person reports
    (re.compile(r'^/report/L/simple_person'), 'person'),
    (re.compile(r'^/report/L/grouped_person'), 'person'),
    (re.compile(r'^/report/M/scene_person'), 'person'),
    (re.compile(r'^/p/\d+/s/\d+/report/L/simple_person'), 'person'),
    (re.compile(r'^/p/\d+/s/\d+/report/L/grouped_person'), 'person'),
    (re.compile(r'^/p/\d+/s/\d+/report/M/scene_person'), 'person'),
    # Other reports → reports tab (or matching entity)
    (re.compile(r'^/report/L/simple_role'), 'role'),
    (re.compile(r'^/report/L/grouped_role'), 'role'),
    (re.compile(r'^/report/M/scene_role'), 'role'),
    (re.compile(r'^/report/L/simple_time'), 'time'),
    (re.compile(r'^/report/L/grouped_time'), 'time'),
    (re.compile(r'^/report/M/scene_time'), 'time'),
    (re.compile(r'^/report/L/simple_location'), 'location'),
    (re.compile(r'^/report/L/grouped_location'), 'location'),
    (re.compile(r'^/report/M/scene_location'), 'location'),
    (re.compile(r'^/report/L/simple_gadget'), 'gadget'),
    (re.compile(r'^/report/L/grouped_gadget'), 'gadget'),
    (re.compile(r'^/report/M/scene_gadget'), 'gadget'),
    (re.compile(r'^/report/L/simple_sfx'), 'sfx'),
    (re.compile(r'^/report/L/grouped_sfx'), 'sfx'),
    (re.compile(r'^/report/M/scene_sfx'), 'sfx'),
    (re.compile(r'^/report/L/simple_audio'), 'audio'),
    (re.compile(r'^/report/L/grouped_audio'), 'audio'),
    (re.compile(r'^/report/M/scene_audio'), 'audio'),
    (re.compile(r'^/report/L/simple_scene'), 'scene'),
    (re.compile(r'^/report/C/'), 'script'),
    (re.compile(r'^/report/'), 'reports'),
    (re.compile(r'^/p/\d+/s/\d+/report/'), 'reports'),
)


def tab_for_path(path: str) -> Optional[str]:
    path = path.split('?')[0]
    for pattern, tab in _PATH_TAB_RULES:
        if pattern.search(path):
            return tab
    return None


def deny_access(prefer_404: bool = False):
    if prefer_404:
        raise Http404()
    raise PermissionDenied()
