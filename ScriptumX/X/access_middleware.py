"""Enforce tab read/write on matching URL paths (server-side, not only UI)."""

import re

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import Http404

from X.access import can, tab_for_path
from X.common import Env, bind_scope_to_request

_SCOPE_RE = re.compile(r'^/p/(?P<project_id>\d+)/s/(?P<script_id>\d+)/')
_PROJECT_RE = re.compile(r'^/project/(?P<project_id>\d+)')


class ProjectAccessMiddleware:
    """GET requires read; POST/PUT/PATCH/DELETE require edit for mapped tabs."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        # Skip auth/admin/static/share/ux helpers
        if (
            path.startswith('/static/')
            or path.startswith('/admin/')
            or path.startswith('/login')
            or path.startswith('/logout')
            or path.startswith('/password')
            or path.startswith('/access/')
            or path.startswith('/report/share/')
            or path.startswith('/ux/')
            or path.startswith('/favicon')
            or path.startswith('/seed')
            or path == '/'
        ):
            return self.get_response(request)

        tab = tab_for_path(path)
        if not tab:
            return self.get_response(request)

        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return redirect_to_login(path)

        scoped = _SCOPE_RE.match(path)
        if scoped:
            bind_scope_to_request(
                request,
                project_id=scoped.group('project_id'),
                script_id=scoped.group('script_id'),
            )
        else:
            proj = _PROJECT_RE.match(path)
            if proj:
                bind_scope_to_request(request, project_id=proj.group('project_id'))

        env = Env(request)

        # Allow project list / new / restore / import without a selected membership project
        bare = path.rstrip('/')
        if bare in ('/project',) or bare.startswith('/project/0') or bare in (
            '/project/restore',
            '/project/import',
        ):
            return self.get_response(request)

        if not env.project:
            raise Http404()

        write = request.method in ('POST', 'PUT', 'PATCH', 'DELETE')
        if not can(user, env.project, tab, write=write):
            raise PermissionDenied()

        return self.get_response(request)
