"""
Definition of views.
"""

from os import path
from datetime import datetime
import random

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.template import RequestContext
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, ButtonHolder, Div, Field, HTML
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.utils import render_crispy_form

from app.models import *
from app.forms import NoteForm
from app.views import g_tab_list
from app.views import Q
from app.common import *

from .tags import FormSymbol, scene_tag_list, handleTagRequest, getTagRequestList
#from app.generator import get_sentences, get_paragraph

###############################################################################


class SceneForm(forms.ModelForm):
    """Edit form for Script model"""
    class Meta:
        model = Scene
        fields = [
            'tag1',
            'tag2',
            'tag3',
            'tag4',
            'tag5',
            'tag6',
            'tag7',
            'tag8',
            'tag9',
            'tag10',
            'tag11',
            'name',
            'description',
            'marker_map',
            ]

    def __init__(self, *args, **kwargs):
        super(SceneForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        #self.helper.form_action = 'submit_survey'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Div(
                Div(FormSymbol(scene_tag_list[1]['img']),  Field('tag1'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(scene_tag_list[2]['img']),  Field('tag2'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(scene_tag_list[3]['img']),  Field('tag3'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(scene_tag_list[4]['img']),  Field('tag4'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(scene_tag_list[5]['img']),  Field('tag5'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                css_class='col-sm-offset-2', style="margin-top:10px;", 
            ),
                Field('name'),
                Field('description', style="max-width:100%; min-width:100%;", rows=10),

        )

    def clean_name(self):
      name = self.cleaned_data.get('name')
      return name

###############################################################################

def script(request, scene_id):
    """Handles page requests for Script"""
    
    project_id = request.session.get('ProjectID', 1)
    try:
        active_user = request.user
        project = Project.objects.get(pk=project_id) #, users=active_user)
    except:
        project = None

    tag_list = getTagRequestList(request, 'scene')
    
    try:
        active_scene = Scene.objects.get(pk = scene_id)
        active_id = active_scene.id
        active_note = active_scene.note
    except ObjectDoesNotExist:
        active_scene = None
        active_id = None
        active_note = None

    ### create new scene object on request '/script/0'
    if scene_id == '0':
        active_scene = Scene(project=project);

    ### handle buttons
    if request.method == 'POST':
        if not active_scene:   # you shall not pass ... without valid scope
            raise AssertionError 

        # generate forms and/or get data out of the edited forms
        formNote = NoteForm(request.POST or None, instance=active_note)
        if formNote.is_valid():
            active_note = formNote.instance
        formItem = SceneForm(request.POST or None, instance=active_scene)
        if formItem.is_valid():
            active_scene = formItem.instance

        # 'Delete'-Button
        if request.POST.get('btn_delete'):
            if active_note:
                if active_note.id:
                    active_note.delete()
            active_scene.note = None
            active_scene.delete()
            return HttpResponseRedirect('/script/')

        # 'Add Note'-Button
        if request.POST.get('btn_note'):
            active_note = Note(author=request.user, created=datetime.now(), project=project)
            active_scene.note = active_note
            #formNote = NoteForm(request.POST or None, instance=active_note) #JK may be re-connect to form???

        # 'Save'-Button
        if request.POST.get('btn_save'):
            if active_note:
                if active_note.text=='':
                    if active_note.id:
                        active_note.delete()
                    active_note = None
                else:
                    active_note.save()

            active_scene.note = active_note

            if active_scene:
                active_scene.save()

            if scene_id == '0':   # previously new item
                return HttpResponseRedirect('/script/' + str(active_scene.id))
    else:
        formItem = SceneForm(instance=active_scene)
        formNote = NoteForm(instance=active_note)
    
    ### conglomerate queries
    query = Q()
    for tag in tag_list:
        if tag['active']:
            if len(query)==0:
                query = g_tag_queries[tag['idx']]
            else:
                query |= g_tag_queries[tag['idx']]

    if len(query)==len(tag_list):
        query = Q()
    elif len(query)==0:
        query = g_tag_query_none
    
    scenes = Scene.objects.filter( project=project_id ).filter( query )

    return render(request, 'app/script.html', {
        'title': 'Script',
        'tab_list': g_tab_list,
        'tab_active_id': 'C',
        'tag_list': tag_list,
        'scenes': scenes,
        'active_scene': active_scene,
        'active_id': active_id,
        'form': formItem,
        'formNote': formNote,
        'datetime': datetime.now(),
        #'error_message': "Please make a selection.",
    })

###############################################################################

def scriptTag(request, tag_id):

    handleTagRequest(request, tag_id, 'scene')

    return script(request, None)

###############################################################################
