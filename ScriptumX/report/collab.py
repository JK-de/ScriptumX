"""Shared helpers for report share links (F14) and filter presets (F15)."""
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import View

from crispy_forms.layout import Div, Field, HTML, Submit

from X.common import Env
from X.models import Project, Role, Scene, Script
from X.tags import all_tag_list, getTagRequestList

from report.models import FilterPreset, ReportShareLink


# report URL name → lazy view class resolver (avoids circular imports at module load)
REPORT_VIEW_REGISTRY = {
    'L_Role': ('report.view_L', 'L_RoleView'),
    'L_Person': ('report.view_L', 'L_PersonView'),
    'L_Time': ('report.view_L', 'L_TimeView'),
    'L_Location': ('report.view_L', 'L_LocationView'),
    'L_Gadget': ('report.view_L', 'L_GadgetView'),
    'L_SFX': ('report.view_L', 'L_SFXView'),
    'L_Audio': ('report.view_L', 'L_AudioView'),
    'L_Scene': ('report.view_L', 'L_SceneView'),
    'L_g_Role': ('report.view_L', 'L_GroupedRoleView'),
    'L_g_Person': ('report.view_L', 'L_GroupedPersonView'),
    'L_g_Time': ('report.view_L', 'L_GroupedTimeView'),
    'L_g_Location': ('report.view_L', 'L_GroupedLocationView'),
    'L_g_Gadget': ('report.view_L', 'L_GroupedGadgetView'),
    'L_g_SFX': ('report.view_L', 'L_GroupedSFXView'),
    'L_g_Audio': ('report.view_L', 'L_GroupedAudioView'),
    'M_SceneRole': ('report.view_M', 'M_SceneRoleView'),
    'M_ScenePerson': ('report.view_M', 'M_ScenePersonView'),
    'M_SceneTime': ('report.view_M', 'M_SceneTimeView'),
    'M_SceneLocation': ('report.view_M', 'M_SceneLocationView'),
    'M_SceneGadget': ('report.view_M', 'M_SceneGadgetView'),
    'M_SceneSFX': ('report.view_M', 'M_SceneSFXView'),
    'M_SceneAudio': ('report.view_M', 'M_SceneAudioView'),
    'S_read': ('report.view_S', 'ScriptView'),
    'S_readpdf': ('report.view_S', 'ScriptPDFView'),
    'C_Script': ('report.view_C', 'CardsView'),
}


def resolve_report_view(report_name):
    entry = REPORT_VIEW_REGISTRY.get(report_name)
    if not entry:
        raise Http404('Unknown report type')
    module_path, class_name = entry
    module = __import__(module_path, fromlist=[class_name])
    return getattr(module, class_name)


def form_to_filter_payload(form, tag_group):
    """Serialize cleaned form data into a JSON-safe filter payload."""
    data = form.cleaned_data
    tags = {}
    for tag in all_tag_list.get(tag_group, ()):
        key = 'tag%d' % tag['idx']
        if key in data:
            tags[str(tag['idx'])] = bool(data[key])
    payload = {
        'tags': tags,
        'show_notes': bool(data.get('show_notes', False)),
    }
    for optional in (
        'show_links', 'show_details', 'columns', 'layout',
        'exterior_only', 'time_day', 'role_id', 'preset_name', 'preset_id',
    ):
        if optional in data and data[optional] not in (None, ''):
            value = data[optional]
            if optional == 'role_id' and hasattr(value, 'pk'):
                value = value.pk
            elif optional == 'roles':
                continue
            payload[optional] = value
    # ModelChoiceField / multiple roles
    if 'roles' in data and data['roles'] is not None:
        payload['roles'] = [r.pk for r in data['roles']]
    return payload


def payload_to_tag_list(payload, tag_group):
    """Build a getTagRequestList-compatible tag list from a frozen payload."""
    tags_map = payload.get('tags') or {}
    tag_list = []
    for tag in all_tag_list[tag_group]:
        item = {
            'idx': tag['idx'],
            'name': tag['name'],
            'img': tag['img'],
            'active': bool(tags_map.get(str(tag['idx']), tags_map.get(tag['idx'], True))),
        }
        if 'type' in tag:
            item['type'] = tag['type']
        tag_list.append(item)
    return tag_list


def payload_to_form_data(payload, tag_group):
    """Flatten payload into form initial/POST-like dict."""
    data = {}
    tags_map = payload.get('tags') or {}
    for tag in all_tag_list.get(tag_group, ()):
        data['tag%d' % tag['idx']] = bool(tags_map.get(str(tag['idx']), tags_map.get(tag['idx'], True)))
    for key in (
        'show_notes', 'show_links', 'show_details', 'columns', 'layout',
        'exterior_only', 'time_day', 'role_id',
    ):
        if key in payload:
            data[key] = payload[key]
    if 'roles' in payload:
        data['roles'] = payload['roles']
    return data


def apply_payload_to_session(request, payload, tag_group):
    """Write tag actives from payload into the user's session (editor/report seed)."""
    tags_map = payload.get('tags') or {}
    for tag in all_tag_list.get(tag_group, ()):
        key = '_%s_tag_%d' % (tag_group, tag['idx'])
        request.session[key] = bool(tags_map.get(str(tag['idx']), tags_map.get(tag['idx'], True)))


def apply_advanced_scene_filters(queryset, payload):
    """Apply Role-X / exterior / day filters stored in payload (beyond boolean tags)."""
    role_id = payload.get('role_id')
    if hasattr(role_id, 'pk'):
        role_id = role_id.pk
    if role_id:
        queryset = queryset.filter(sceneitem__role_id=role_id).distinct()
    if payload.get('exterior_only'):
        queryset = queryset.filter(story_location__tag2=True)
    time_day = payload.get('time_day')
    if time_day not in (None, ''):
        try:
            queryset = queryset.filter(story_time__day=int(time_day))
        except (TypeError, ValueError):
            pass
    return queryset


def filter_payload_from_request_form(request, form, tag_group):
    """Prefer frozen share payload; otherwise serialize the validated form."""
    share = getattr(request, '_share_context', None)
    if share and share.get('payload') is not None:
        return share['payload']
    if hasattr(form, 'cleaned_data') and isinstance(form.cleaned_data, dict):
        # BoundFilterData already holds a flat dict; validated forms need serialization
        if type(form).__name__ == 'BoundFilterData':
            return form.cleaned_data
        try:
            return form_to_filter_payload(form, tag_group)
        except Exception:
            return dict(form.cleaned_data)
    return {}


def _share_tab_for_report(report_name):
    """Map report name to membership tab for share-create rights."""
    name = (report_name or '').lower()
    mapping = (
        ('person', 'person'),
        ('role', 'role'),
        ('time', 'time'),
        ('location', 'location'),
        ('gadget', 'gadget'),
        ('sfx', 'sfx'),
        ('audio', 'audio'),
        ('scene', 'scene'),
        ('script', 'script'),
        ('card', 'script'),
    )
    for needle, tab in mapping:
        if needle in name:
            return tab
    return 'reports'


def user_can_share_project(user, project, report_name=''):
    if not user or not user.is_authenticated or not project:
        return False
    from X.access import can_create_share, user_is_site_admin
    if user_is_site_admin(user):
        return True
    tab = _share_tab_for_report(report_name)
    return can_create_share(user, project, tab)


def create_share_link(request, report_name, title, tag_group, form):
    env = Env(request)
    if not env.project:
        return None, 'No project selected.'
    if not user_can_share_project(request.user, env.project, report_name=report_name):
        return None, 'You cannot create share links for this project.'
    payload = form_to_filter_payload(form, tag_group)
    label = (form.cleaned_data.get('preset_name') or '').strip()
    link = ReportShareLink.objects.create(
        project=env.project,
        script=env.script,
        report_name=report_name,
        title=title or report_name,
        label=label,
        filter_payload=payload,
        created_by=request.user if request.user.is_authenticated else None,
    )
    return link, None


def save_filter_preset(request, tag_group, report_name, form):
    if not request.user.is_authenticated:
        return None, 'Login required to save presets.'
    name = (form.cleaned_data.get('preset_name') or '').strip()
    if not name:
        return None, 'Enter a preset name before saving.'
    payload = form_to_filter_payload(form, tag_group)
    apply_payload_to_session(request, payload, tag_group)
    preset, _created = FilterPreset.objects.update_or_create(
        user=request.user,
        name=name,
        tag_group=tag_group,
        defaults={
            'report_name': report_name or '',
            'payload': payload,
        },
    )
    return preset, None


def load_filter_preset(request, preset_id, tag_group):
    if not request.user.is_authenticated:
        return None, 'Login required.'
    preset = get_object_or_404(FilterPreset, pk=preset_id, user=request.user)
    if tag_group and preset.tag_group != tag_group:
        return None, 'Preset does not match this filter group.'
    apply_payload_to_session(request, preset.payload, preset.tag_group)
    return preset, None


def attach_collab_fields(form, request, tag_group, report_name):
    """Add share/preset fields + submit buttons onto an existing crispy filter form."""
    if getattr(form, '_collab_attached', False):
        return form

    if 'preset_name' not in form.fields:
        form.fields['preset_name'] = forms.CharField(
            label='Preset / share label',
            max_length=100,
            required=False,
        )
    presets = []
    if request.user.is_authenticated:
        presets = list(
            FilterPreset.objects.filter(user=request.user, tag_group=tag_group).order_by('name')
        )
    choices = [('', '— load saved preset —')] + [(str(p.pk), p.name) for p in presets]
    form.fields['preset_id'] = forms.ChoiceField(
        label='Saved presets',
        choices=choices,
        required=False,
    )

    # Scene advanced filters (Role X / exteriors / day) when form supports them
    if tag_group == 'scene':
        if 'exterior_only' not in form.fields:
            form.fields['exterior_only'] = forms.BooleanField(
                label='Exteriors only (location Extern)',
                required=False,
            )
        if 'time_day' not in form.fields:
            form.fields['time_day'] = forms.IntegerField(
                label='Story day',
                required=False,
                min_value=1,
            )
        if 'role_id' not in form.fields:
            env = Env(request)
            role_qs = Role.objects.filter(project=env.project_id).order_by('name') if env.project_id else Role.objects.none()
            form.fields['role_id'] = forms.ModelChoiceField(
                label='Scenes with role',
                queryset=role_qs,
                required=False,
                empty_label='— any role —',
            )

    if form.helper and form.helper.layout is not None:
        extra = []
        if tag_group == 'scene':
            extra.extend([
                Field('exterior_only'),
                Field('time_day'),
                Field('role_id'),
            ])
        extra.extend([
            HTML('<hr/><h5>Share &amp; presets</h5>'),
            Field('preset_name'),
            Field('preset_id'),
        ])
        form.helper.layout.extend(extra)

    # Extra submits (Show List already added by FormHelperX / individual forms)
    form.helper.add_input(Submit('create_share', 'Create share link', css_class='btn-info'))
    form.helper.add_input(Submit('save_preset', 'Save preset', css_class='btn-default'))
    form.helper.add_input(Submit('load_preset', 'Load preset', css_class='btn-default'))
    form._collab_attached = True
    return form


def handle_collab_post(view, request, form, tag_list, report_name):
    """
    Process create_share / save_preset / load_preset actions.
    Returns an HttpResponse if handled, else None (caller should render_list).
    `form` must already have collab fields attached before this is called.
    """
    tag_group = view.x_group

    if 'load_preset' in request.POST:
        preset_id = request.POST.get('preset_id') or form.data.get('preset_id')
        if not preset_id:
            # Still need a bound form with fields for redisplay
            if not form.is_bound:
                pass
            form = view.form_class(request.POST)
            attach_collab_fields(form, request, tag_group, report_name)
            form.add_error('preset_id', 'Select a preset to load.')
            return view.render_form(request, form)
        preset, err = load_filter_preset(request, preset_id, tag_group)
        if err:
            form = view.form_class(request.POST)
            attach_collab_fields(form, request, tag_group, report_name)
            form.add_error(None, err)
            return view.render_form(request, form)
        initial = payload_to_form_data(preset.payload, tag_group)
        initial['preset_name'] = preset.name
        initial['preset_id'] = str(preset.pk)
        new_form = view.form_class(initial=initial)
        attach_collab_fields(new_form, request, tag_group, report_name)
        return view.render_form(request, new_form)

    if not form.is_valid():
        return view.render_form(request, form)

    # Refresh tag actives from cleaned data
    for tag in tag_list:
        key = 'tag%d' % tag['idx']
        if key in form.cleaned_data:
            tag['active'] = form.cleaned_data[key]

    if 'create_share' in request.POST:
        link, err = create_share_link(request, report_name, view.title, tag_group, form)
        if err:
            form.add_error(None, err)
            return view.render_form(request, form)
        share_url = request.build_absolute_uri(
            reverse('report:shared_report', kwargs={'token': link.token})
        )
        return render(request, 'report/share_created.html', {
            'title': 'Share link created',
            'link': link,
            'share_url': share_url,
            'report_title': view.title,
        })

    if 'save_preset' in request.POST:
        preset, err = save_filter_preset(request, tag_group, report_name, form)
        if err:
            form.add_error(None, err)
            return view.render_form(request, form)
        return render(request, 'report/preset_saved.html', {
            'title': 'Preset saved',
            'preset': preset,
            'report_title': view.title,
        })

    return None


def prepare_filter_form(view, request, data=None, initial=None):
    """Build a filter form with collab fields attached (required before is_valid)."""
    if data is not None:
        form = view.form_class(data)
    else:
        form = view.form_class(initial=initial or {})
    attach_collab_fields(form, request, view.x_group, view.get_report_url_name())
    return form


class BoundFilterData:
    """Minimal stand-in for a validated form when rendering a shared report."""

    def __init__(self, payload, tag_group):
        self.cleaned_data = payload_to_form_data(payload, tag_group)
        # Normalize types expected by render_list
        if 'show_notes' not in self.cleaned_data:
            self.cleaned_data['show_notes'] = False
        if 'roles' in payload:
            self.cleaned_data['roles'] = Role.objects.filter(pk__in=payload['roles'])
        if 'role_id' in self.cleaned_data and self.cleaned_data['role_id']:
            try:
                self.cleaned_data['role_id'] = Role.objects.get(pk=self.cleaned_data['role_id'])
            except Role.DoesNotExist:
                self.cleaned_data['role_id'] = None


class SharedReportView(View):
    """Public read-only report via token (no login)."""

    def get(self, request, token, *args, **kwargs):
        link = get_object_or_404(ReportShareLink, token=token)
        if not link.is_active():
            raise Http404('This share link is no longer available.')

        view_cls = resolve_report_view(link.report_name)
        view = view_cls()
        tag_group = view.x_group
        payload = link.filter_payload or {}
        tag_list = payload_to_tag_list(payload, tag_group)
        form = BoundFilterData(payload, tag_group)

        request._share_context = {
            'project': link.project,
            'script': link.script,
            'link': link,
            'read_only': True,
            'payload': payload,
        }

        response = view.render_list(request, form, tag_list)
        # Mark shared views as read-only in context when possible
        if hasattr(response, 'context_data') and response.context_data is not None:
            response.context_data['shared_read_only'] = True
            response.context_data['share_link'] = link
        return response


@login_required
def revoke_share_link(request, token):
    link = get_object_or_404(ReportShareLink, token=token)
    if not user_can_share_project(request.user, link.project):
        return HttpResponseForbidden('Not allowed')
    if request.method == 'POST':
        link.revoked = True
        link.save(update_fields=['revoked'])
    return redirect(request.META.get('HTTP_REFERER') or '/')
