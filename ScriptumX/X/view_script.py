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
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, ButtonHolder, Div, Field, MultiField, HTML, Row, Column
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.utils import render_crispy_form

from X.models import *
from X.forms import NoteForm
from X.views import g_tab_list
from X.views import Q
from X.common import *

from .tags import FormSymbol, scene_tag_list, handleTagRequest, getTagRequestList
#from X.generator import get_sentences, get_paragraph

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
            'name',
            'short',
            'abstract',
            'description',
            'indentation',
            'color',
            'duration',
            'progress_script',
            'progress_pre',
            'progress_shot',
            'progress_post',
            'set_location',
            'persons',
            'gadgets',
            'audios',
            'sfxs',
            ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.fields['persons'].queryset = Person.objects.filter(project=env.project)
        #self.fields['gadgets'].queryset = Gadget.objects.filter(project=env.project)
        #self.fields['audios'].queryset = Audio.objects.filter(project=env.project)
        #self.fields['sfxs'].queryset = SFX.objects.filter(project=env.project)

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
                css_class='col-sm-offset-2', style="margin-top:0px;", 
            ),
#                MultiField( 'TEXT1', 
#                    #Field('name', field_class='col-sm-4', style="max-width:30%; min-width:3%;", ), 
#                    #Field('short', field_class='col-sm-1',style="max-width:10%; min-width:1%;", ),
#                    Field('name', field_class='col-sm-4', ), 
#                    Field('short', field_class='col-sm-3',),
#                    #css_class='row',
#                    ),
##field_class = ‘’
#Layout(
#    Column(
#        'name',
#        'short',
        
#    )
#),
#Layout(
#    Column(
#                    Field('name', css_class='col-sm-4', ), 
#                    Field('short', css_class='col-sm-1', ),
                  
#    )
#),
#    Column(
#                    Field('name', css_class='col-sm-4', ), 
#                    Field('short', css_class='col-sm-1', ),
             
#    ),
            Field('name', style="max-width:30em; min-width:30em;" ), 
            Field('short', style="max-width:5em; min-width:5em;", ),
            Field('duration', style="max-width:10em; min-width:10em;", ),

            Field('abstract', style="max-width:100%; min-width:100%;", rows=2),

            Field('set_location', css_class='chosen-select'),

            Field('persons', css_class='chosen-select', style="max-width:100%; min-width:100%; min-height:48px;"),
            Field('gadgets', css_class='chosen-select', style="max-width:100%; min-width:100%; min-height:48px;"),
            Field('audios', css_class='chosen-select', style="max-width:100%; min-width:100%; min-height:48px;"),
            Field('sfxs', css_class='chosen-select', style="max-width:100%; min-width:100%; min-height:48px;"),

            Field('indentation', template="X/tmpl_slider_indentation.html"),

            Field('progress_script', template="X/tmpl_slider_progress_script.html"),
            Field('progress_pre', template="X/tmpl_slider_progress_pre.html"),
            Field('progress_shot', template="X/tmpl_slider_progress_shot.html"),
            Field('progress_post', template="X/tmpl_slider_progress_post.html"),

            # http://jscolor.com/examples/
            Field('color', style="width:10%;", css_class="jscolor {width:243, height:150, position:'right', borderColor:'#FFF', insetColor:'#FFF', backgroundColor:'#666'}"),

            Field('description', style="max-width:100%; min-width:100%;", rows=10),

        )

    def clean_name(self):
      name = self.cleaned_data.get('name')
      return name

###############################################################################

@login_required
def script(request, scene_id, new_order=0):
    """Handles page requests for Script"""
    
    env = Env(request)

    tag_list = getTagRequestList(request, 'scene')
    
    try:
        selected_scene = Scene.objects.get(pk = scene_id)
        selected_note = selected_scene.note
    except ObjectDoesNotExist:
        selected_scene = None
        selected_note = None

    ### create new scene object on request '/script/0'
    if scene_id == '0':
        selected_scene = Scene(project=env.project, script=env.script);
        selected_scene.setAllTags(True)
        selected_scene.order = new_order

    ### handle buttons
    if request.method == 'POST':
        if not selected_scene:   # you shall not pass ... without valid scope
            raise AssertionError 

        # generate forms and/or get data out of the edited forms
        formNote = NoteForm(request.POST or None, instance=selected_note)
        if formNote.is_valid():
            selected_note = formNote.instance
        formItem = SceneForm(request.POST or None, instance=selected_scene)
        if formItem.is_valid():
            selected_scene = formItem.instance

        # 'Delete'-Button
        if request.POST.get('btn_delete'):
            if selected_note:
                if selected_note.id:
                    selected_note.delete()
            selected_scene.note = None
            selected_scene.delete()
            return HttpResponseRedirect('/script/')

        # 'Add Note'-Button
        if request.POST.get('btn_note'):
            selected_note = Note(project=env.project, author=env.user)
            selected_scene.note = selected_note
            #formNote = NoteForm(request.POST or None, instance=selected_note) #JK may be re-connect to form???

        # 'Save'-Button
        if request.POST.get('btn_save'):
            if selected_note:
                if selected_note.text=='':
                    if selected_note.id:
                        selected_note.delete()
                    selected_note = None
                else:
                    selected_note.project=env.project
                    selected_note.author=env.user
                    selected_note.save()

            selected_scene.note = selected_note

            if selected_scene:
                if formItem.is_valid():
                    formItem.save()
                #selected_scene.save()

            if scene_id == '0':   # previously new item
                return HttpResponseRedirect('/script/' + str(selected_scene.id))
    else:
        formItem = SceneForm(instance=selected_scene)
        formNote = NoteForm(instance=selected_note)

    formItem.fields['set_location'].queryset = Location.objects.filter(project=env.project)
    formItem.fields['persons'].queryset = Person.objects.filter(project=env.project)
    formItem.fields['gadgets'].queryset = Gadget.objects.filter(project=env.project)
    formItem.fields['audios'].queryset = Audio.objects.filter(project=env.project)
    formItem.fields['sfxs'].queryset = SFX.objects.filter(project=env.project)
    
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
    
    scenes = Scene.objects.filter( project=env.project_id, script=env.script_id ).filter( query )

    return render(request, 'X/script.html', {
        'title': 'Script',
        'env': env,
        'tab_list': g_tab_list,
        'tab_active_id': 'C',
        'tag_list': tag_list,
        'scenes': scenes,
        'selected_scene': selected_scene,
        'form': formItem,
        'formNote': formNote,
        #'error_message': "Please make a selection.",
    })

###############################################################################

@login_required
def scriptTag(request, tag_id):

    handleTagRequest(request, tag_id, 'scene')

    return script(request, None)

###############################################################################

@login_required
def scriptMove(request, scene_id, offset):

    env = Env(request)

    try:
        scene = Scene.objects.filter( project=env.project_id, script=env.script_id )
        
        offset = int(offset)
        if offset < 0:
            offset -= 1
        if offset > 0:
            offset += 1
        newOrder = getOrderNumber(scene, scene_id, offset)
        if newOrder:
            selected_scene = Scene.objects.get( project=env.project_id, script=env.script_id, id=scene_id )
            selected_scene.order = newOrder
            selected_scene.save()
            
    except:
        pass

    url ='/script/' + scene_id
    return HttpResponseRedirect(url)

###############################################################################

def scriptNew(request, scene_id, offset):

    env = Env(request)

    try:
        scene = Scene.objects.filter( project=env.project_id, script=env.script_id )
        
        newOrder = getOrderNumber(scene, scene_id, offset)
    except:
        newOrder = 0

    url ='/script/0/' + str(newOrder)
    return HttpResponseRedirect(url)

###############################################################################
