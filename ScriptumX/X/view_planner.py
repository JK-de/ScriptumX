"""
Production planner views (F9–F12).
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from X.common import Env, bind_scope_to_request, get_tab_list
from X.planner import (
    build_cast_availability,
    build_dood,
    build_location_groups,
    build_progress_dashboard,
    build_stripboard,
)

PLANNER_NAV = (
    {'id': 'hub', 'name': 'Overview', 'href': '/planner/', 'url_name': 'planner'},
    {'id': 'stripboard', 'name': 'Stripboard', 'href': '/planner/stripboard/', 'url_name': 'plannerStripboard'},
    {'id': 'dood', 'name': 'Day out of days', 'href': '/planner/dood/', 'url_name': 'plannerDood'},
    {'id': 'cast', 'name': 'Cast conflicts', 'href': '/planner/cast/', 'url_name': 'plannerCast'},
    {'id': 'locations', 'name': 'Location days', 'href': '/planner/locations/', 'url_name': 'plannerLocations'},
    {'id': 'progress', 'name': 'Progress', 'href': '/planner/progress/', 'url_name': 'plannerProgress'},
    {'id': 'scheduler', 'name': 'Appointments', 'href': '/scheduler/', 'url_name': 'scheduler'},
)


def _planner_context(request, nav_id, title, **kwargs):
    bind_scope_to_request(request, **kwargs)
    env = Env(request)
    return {
        'title': title,
        'env': env,
        'tab_list': get_tab_list(env),
        'tab_active_id': 'B',
        'planner_nav': PLANNER_NAV,
        'planner_nav_id': nav_id,
        'project': env.project,
        'script': env.script,
    }


@login_required
def planner(request, **kwargs):
    """Planner hub — links to F9–F12 views."""
    ctx = _planner_context(request, 'hub', 'Production planner', **kwargs)
    if ctx['project']:
        days = build_stripboard(ctx['project'], ctx['script'])
        progress = build_progress_dashboard(ctx['project'], ctx['script'])
        ctx['day_count'] = len(days['days'])
        ctx['unscheduled_count'] = len(days['unscheduled'])
        ctx['overall_progress'] = progress['project_totals']['overall']
    else:
        ctx['day_count'] = 0
        ctx['unscheduled_count'] = 0
        ctx['overall_progress'] = 0
    return render(request, 'X/planner.html', ctx)


@login_required
def planner_stripboard(request, **kwargs):
    """F9 — stripboard from Scenes + Appointments."""
    ctx = _planner_context(request, 'stripboard', 'Stripboard', **kwargs)
    if ctx['project']:
        ctx.update(build_stripboard(ctx['project'], ctx['script']))
    else:
        ctx['days'] = []
        ctx['unscheduled'] = []
    return render(request, 'X/planner_stripboard.html', ctx)


@login_required
def planner_dood(request, **kwargs):
    """F9 — day-out-of-days matrix."""
    ctx = _planner_context(request, 'dood', 'Day out of days', **kwargs)
    if ctx['project']:
        ctx.update(build_dood(ctx['project'], ctx['script']))
    else:
        ctx['columns'] = []
        ctx['rows'] = []
        ctx['day_count'] = 0
    return render(request, 'X/planner_dood.html', ctx)


@login_required
def planner_cast(request, **kwargs):
    """F10 — cast availability vs scene roles."""
    ctx = _planner_context(request, 'cast', 'Cast conflicts', **kwargs)
    if ctx['project']:
        ctx.update(build_cast_availability(ctx['project'], ctx['script']))
    else:
        ctx['reports'] = []
    return render(request, 'X/planner_cast.html', ctx)


@login_required
def planner_locations(request, **kwargs):
    """F11 — location day grouping / shoot suggestions."""
    ctx = _planner_context(request, 'locations', 'Location days', **kwargs)
    if ctx['project']:
        ctx.update(build_location_groups(ctx['project'], ctx['script']))
    else:
        ctx['groups'] = []
        ctx['suggestions'] = []
    return render(request, 'X/planner_locations.html', ctx)


@login_required
def planner_progress(request, **kwargs):
    """F12 — progress dashboard from scene sliders."""
    ctx = _planner_context(request, 'progress', 'Progress dashboard', **kwargs)
    if ctx['project']:
        # Dashboard shows all scripts in the project for producer overview
        ctx.update(build_progress_dashboard(ctx['project'], script=None))
    else:
        ctx['scripts'] = []
        ctx['project_totals'] = {
            'scene_count': 0,
            'progress_script': 0,
            'progress_pre': 0,
            'progress_shot': 0,
            'progress_post': 0,
            'overall': 0,
        }
    return render(request, 'X/planner_progress.html', ctx)
