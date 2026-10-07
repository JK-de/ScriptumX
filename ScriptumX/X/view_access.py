"""Site-admin and producer user/project access dashboard."""

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from X.access import (
    PRODUCER_ASSIGNABLE_ROLES,
    ROLE_CHOICES,
    ROLE_PRODUCER,
    TAB_KEYS,
    apply_preset_to_membership,
    assignable_roles_for,
    can_invite,
    deactivate_user,
    ensure_membership,
    projects_for_user,
    user_is_site_admin,
)
from X.common import Env, get_tab_list
from X.models import Project, ProjectMembership

User = get_user_model()


def _dashboard_allowed(user):
    if user_is_site_admin(user):
        return True
    return ProjectMembership.objects.filter(
        user=user, role=ROLE_PRODUCER
    ).exists() or ProjectMembership.objects.filter(user=user, can_invite=True).exists()


@login_required
def access_dashboard(request):
    if not _dashboard_allowed(request.user):
        return HttpResponseForbidden('Access dashboard requires site admin or producer.')

    env = Env(request)
    is_admin = user_is_site_admin(request.user)
    if is_admin:
        users = User.objects.order_by('username')
        projects = Project.objects.order_by('name')
    else:
        projects = projects_for_user(request.user).filter(
            memberships__user=request.user,
            memberships__role=ROLE_PRODUCER,
        ).distinct().order_by('name')
        # Producers may assign existing accounts (cannot create site users).
        users = User.objects.filter(is_active=True).order_by('username')

    memberships = ProjectMembership.objects.filter(
        project__in=projects
    ).select_related('user', 'project').order_by('project__name', 'user__username')

    return render(request, 'X/access_dashboard.html', {
        'title': 'User access',
        'env': env,
        'tab_list': get_tab_list(env),
        'tab_active_id': 'P',
        'is_site_admin': is_admin,
        'users': users,
        'projects': projects,
        'memberships': memberships,
        'role_choices': ROLE_CHOICES,
        'producer_roles': PRODUCER_ASSIGNABLE_ROLES,
        'tab_keys': TAB_KEYS,
    })


@login_required
@require_POST
def access_create_user(request):
    if not user_is_site_admin(request.user):
        return HttpResponseForbidden('Only site admins can create users.')
    username = (request.POST.get('username') or '').strip()
    email = (request.POST.get('email') or '').strip()
    password = request.POST.get('password') or ''
    if not username or not password:
        messages.error(request, 'Username and password are required.')
        return redirect('/access/')
    if User.objects.filter(username=username).exists():
        messages.error(request, 'Username already exists.')
        return redirect('/access/')
    user = User.objects.create_user(username=username, email=email, password=password)
    messages.success(request, 'Created user %s.' % user.username)
    return redirect('/access/')


@login_required
@require_POST
def access_update_user(request, user_id):
    if not user_is_site_admin(request.user):
        return HttpResponseForbidden('Only site admins can update users.')
    user = get_object_or_404(User, pk=user_id)
    if request.POST.get('deactivate'):
        if user.pk == request.user.pk:
            messages.error(request, 'You cannot deactivate yourself.')
            return redirect('/access/')
        deactivate_user(user)
        messages.success(request, 'Deactivated %s and removed memberships.' % user.username)
        return redirect('/access/')
    email = (request.POST.get('email') or '').strip()
    user.email = email
    if request.POST.get('activate'):
        user.is_active = True
    user.save()
    messages.success(request, 'Updated %s.' % user.username)
    return redirect('/access/')


@login_required
@require_POST
def access_assign(request):
    """Assign a user to a project with a role preset (and optional tab overrides)."""
    project = get_object_or_404(Project, pk=request.POST.get('project_id'))
    if not can_invite(request.user, project) and not user_is_site_admin(request.user):
        return HttpResponseForbidden('Cannot invite on this project.')

    user = get_object_or_404(User, pk=request.POST.get('user_id'))
    role = (request.POST.get('role') or '').strip()
    allowed = assignable_roles_for(request.user, project)
    if role not in allowed:
        messages.error(request, 'You cannot assign role %r.' % role)
        return redirect('/access/')

    # Producers cannot create site admins or raise rights to producer/director
    if not user_is_site_admin(request.user):
        if role == ROLE_PRODUCER or user.is_superuser:
            messages.error(request, 'Producers cannot grant site admin or producer.')
            return redirect('/access/')
        if 'is_superuser' in request.POST:
            messages.error(request, 'Producers cannot grant site admin.')
            return redirect('/access/')

    overrides = {}
    for tab in TAB_KEYS:
        if request.POST.get('override_%s' % tab):
            overrides[tab] = {
                'read': bool(request.POST.get('read_%s' % tab)),
                'edit': bool(request.POST.get('edit_%s' % tab)),
            }

    membership = ensure_membership(
        project, user, role, overrides=overrides or None
    )
    messages.success(
        request,
        'Assigned %s as %s on %s.' % (user.username, membership.role, project.name),
    )
    return redirect('/access/')


@login_required
@require_POST
def access_membership_update(request, membership_id):
    membership = get_object_or_404(
        ProjectMembership.objects.select_related('project', 'user'),
        pk=membership_id,
    )
    project = membership.project
    if not can_invite(request.user, project) and not user_is_site_admin(request.user):
        return HttpResponseForbidden('Cannot manage this membership.')

    if request.POST.get('remove'):
        membership.delete()
        from X.access import sync_legacy_m2m
        sync_legacy_m2m(project)
        messages.success(request, 'Removed membership.')
        return redirect('/access/')

    role = (request.POST.get('role') or membership.role).strip()
    allowed = assignable_roles_for(request.user, project)
    if role not in allowed and not user_is_site_admin(request.user):
        messages.error(request, 'You cannot assign role %r.' % role)
        return redirect('/access/')
    if not user_is_site_admin(request.user) and role == ROLE_PRODUCER:
        messages.error(request, 'Producers cannot grant producer.')
        return redirect('/access/')

    overrides = {}
    for tab in TAB_KEYS:
        if request.POST.get('override_%s' % tab):
            overrides[tab] = {
                'read': bool(request.POST.get('read_%s' % tab)),
                'edit': bool(request.POST.get('edit_%s' % tab)),
            }
    apply_preset_to_membership(membership, role, overrides=overrides or None)
    messages.success(request, 'Updated membership.')
    return redirect('/access/')
