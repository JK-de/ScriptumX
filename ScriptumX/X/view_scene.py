"""
Definition of views.
"""

from os import path
from datetime import datetime
import random

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Lower
from django.views.decorators.http import require_http_methods

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, ButtonHolder, Div, Field, HTML, Hidden
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.utils import render_crispy_form

from X.models import Gadget, Role, Scene, SceneItem, SFX
from X.common import ORDER_STEP, Env, get_tab_list, getOrderNumber
from X import data_safety
from X.conflict import token_for

from .tags import FormSymbol, sceneitem_tag_list, handleTagRequest, getTagRequestList

###############################################################################

class SceneItemForm(forms.ModelForm):
    """Edit form for SceneItem model"""
    class Meta:
        model = SceneItem
        fields = [
            'role',
            'gadget',
            'sfx',
            'parenthetical',
            'text',
            ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Field('role', css_class='chosen-select-single'),

            Field('gadget', css_class='chosen-select-single'),

            Field('sfx', css_class='chosen-select-single'),

            Field('parenthetical', style="max-width:100%; min-width:100%;"),

            Field('text', style="max-width:100%; min-width:100%;", rows=10),
            )

    def clean_name(self):
      name = self.cleaned_data.get('name')
      return name


def _breakdown_name(sceneitem):
    """Derive a short entity name from a scene item."""
    import re
    import html as html_mod
    text = sceneitem.text or ''
    text = re.sub(r'<[^>]+>', '', text)
    text = html_mod.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    if sceneitem.role and sceneitem.role.name:
        return sceneitem.role.name[:50]
    if not text:
        return 'Item'
    # Prefer quoted prop/sfx names when present
    quoted = re.search(r'[\"“](.+?)[\"”]', text)
    if quoted:
        return quoted.group(1)[:50]
    return text[:50]


def apply_breakdown(env, sceneitem, kind):
    """One-click mark SceneItem as Role / Prop (Gadget) / SFX and link scene."""
    name = _breakdown_name(sceneitem)
    scene = sceneitem.scene

    if kind == 'role':
        if sceneitem.role:
            role = sceneitem.role
        else:
            try:
                role = Role.objects.get(project=env.project, name__iexact=name)
            except Role.DoesNotExist:
                role = Role(name=name, project=env.project)
                role.save()
            sceneitem.role = role
            if sceneitem.type in ('', 'A', 'N'):
                sceneitem.type = 'R'
        sceneitem.save()
        return role

    if kind == 'prop':
        try:
            gadget = Gadget.objects.get(project=env.project, name__iexact=name)
        except Gadget.DoesNotExist:
            gadget = Gadget(name=name, project=env.project)
            gadget.save()
        sceneitem.gadget = gadget
        sceneitem.save()
        if scene is not None:
            scene.gadgets.add(gadget)
        return gadget

    if kind == 'sfx':
        try:
            sfx = SFX.objects.get(project=env.project, name__iexact=name)
        except SFX.DoesNotExist:
            sfx = SFX(name=name, project=env.project)
            sfx.save()
        sceneitem.sfx = sfx
        sceneitem.save()
        if scene is not None:
            scene.sfxs.add(sfx)
        return sfx

    raise ValueError('Unknown breakdown kind: %s' % kind)

###############################################################################

@login_required
def scene(request, sceneitem_id=None, new_type='?', new_order=0, project_id=None, script_id=None):
    """Handles page requests for SceneItems"""

    env = Env(request, project_id=project_id, script_id=script_id)

    tag_list = getTagRequestList(request, 'sceneitem')
    conflict_message = None

    try:
        selected_sceneitem = SceneItem.objects.get(pk = sceneitem_id)
    except ObjectDoesNotExist:
        selected_sceneitem = None

    if selected_sceneitem and selected_sceneitem.scene != env.scene:
        env.setScene(selected_sceneitem.scene)

    ### create new sceneitem object on request '/scene/0'
    if sceneitem_id == '0':
        selected_sceneitem = SceneItem(scene=env.scene);
        selected_sceneitem.type = new_type
        selected_sceneitem.order = new_order

    ### handle buttons
    if request.method == 'POST':
        if not selected_sceneitem:   # you shall not pass ... without valid scope
            raise AssertionError 

        # generate forms and/or get data out of the edited forms
        formItem = SceneItemForm(request.POST or None, instance=selected_sceneitem)
        if formItem.is_valid():
            selected_sceneitem = formItem.instance

        # 'Delete'-Button
        if request.POST.get('btn_delete'):
            selected_sceneitem.delete()
            return HttpResponseRedirect('/scene/')

        # One-click breakdown buttons
        for kind, btn in (('role', 'btn_break_role'), ('prop', 'btn_break_prop'), ('sfx', 'btn_break_sfx')):
            if request.POST.get(btn):
                if formItem.is_valid():
                    formItem.save()
                    selected_sceneitem = formItem.instance
                apply_breakdown(env, selected_sceneitem, kind)
                return HttpResponseRedirect('/scene/' + str(selected_sceneitem.id))

        # 'Save'-Button
        if request.POST.get('btn_save'):
            blocked, conflict_message = data_safety.check_save_conflict(request, selected_sceneitem)
            if blocked and selected_sceneitem and selected_sceneitem.pk:
                from django.contrib import messages
                messages.error(request, conflict_message)
            else:
                if selected_sceneitem:
                    if formItem.is_valid():
                        formItem.save()
                        selected_sceneitem.refresh_from_db()

                if sceneitem_id == '0':   # previously new item
                    return HttpResponseRedirect('/scene/' + str(selected_sceneitem.id))
    else:
        formItem = SceneItemForm(instance=selected_sceneitem)
    
    if selected_sceneitem:
        if selected_sceneitem.type == 'A' or selected_sceneitem.type == 'N' or selected_sceneitem.type == 'T':
            formItem.helper[0:1].update_attributes(type="hidden")
            formItem.helper[3:4].update_attributes(type="hidden")
        if selected_sceneitem.type == 'N':
            formItem.helper[4:5].update_attributes(style="max-width:100%; min-width:100%; background-color:#FFFFA5;")
            formItem.fields['text'].label = "Note"

    formItem.fields['role'].queryset = Role.objects.filter(project=env.project)
    formItem.fields['gadget'].queryset = Gadget.objects.filter(project=env.project)
    formItem.fields['sfx'].queryset = SFX.objects.filter(project=env.project)

    ### conglomerate queries
    query = Q()
    for tag in tag_list:
        if tag['active']:
            if len(query)==0:
                query = Q(type=tag['type'])
            else:
                query |= Q(type=tag['type'])

    if len(query)==len(tag_list):
        query = Q()

    # scenes for toolbar
    scenes = Scene.objects.filter( project=env.project_id, script=env.script_id ).order_by('order')
    
    sceneitems = SceneItem.objects.filter(scene=env.scene).filter( query ).order_by('order')

    return render(request, 'X/scene.html', {
        'title': 'SceneItem',
        'env': env,
        'tab_list': get_tab_list(env),
        'tab_active_id': 'S',
        'tag_list': tag_list,
        'scenes': scenes,
        'selected_scene': env.scene,
        'sceneitems': sceneitems,
        'selected_sceneitem': selected_sceneitem,
        'form': formItem,
        'can_undo_move': data_safety.can_undo(request, 'sceneitem'),
        'conflict_message': conflict_message,
        'autosave_url': ('/scene/autosave/' + str(selected_sceneitem.id)) if selected_sceneitem and selected_sceneitem.pk else '',
        'expected_updated_at': token_for(selected_sceneitem) if selected_sceneitem and selected_sceneitem.pk else '',
    })

###############################################################################

@login_required
def sceneTag(request, tag_id):

    handleTagRequest(request, tag_id, 'sceneitem')

    return scene(request, None)

###############################################################################

@login_required
def sceneSet(request, scene_id):

    env = Env(request)

    try:
        next_scene = Scene.objects.get( project=env.project, script=env.script, id=scene_id )
        env.setScene(next_scene)
    except:
        pass

    return scene(request, None)

###############################################################################

@login_required
def sceneMove(request, sceneitem_id, offset):
    """Reorder a scene item. Requires POST after UI confirm; GET is a no-op redirect."""
    if request.method != 'POST':
        return HttpResponseRedirect('/scene/' + str(sceneitem_id))

    try:
        url = data_safety.perform_sceneitem_move(request, sceneitem_id, offset)
    except Exception:
        url = '/scene/' + str(sceneitem_id)

    return HttpResponseRedirect(url)

###############################################################################

@login_required
@require_http_methods(['POST'])
def sceneUndoMove(request):
    return data_safety.undo_sceneitem_move(request)

###############################################################################

def sceneNew(request, sceneitem_id, sceneitem_type, offset):

    env = Env(request)

    try:
        sceneitems = SceneItem.objects.filter(scene=env.scene).order_by('order')
        newOrder = getOrderNumber(sceneitems, sceneitem_id, offset)
    except Exception:
        newOrder = None

    if newOrder is None:
        newOrder = ORDER_STEP

    url = '/scene/0/' + sceneitem_type + '/' + str(newOrder)
    return HttpResponseRedirect(url)

###############################################################################
