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
            'script',
            'set_location',
            'persons',
            'gadgets',
            'audios',
            'sfxs',
 
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
                    Field('name', css_class='col-sm-4', ), 
                    Field('short', css_class='col-sm-1', ),

                Field('abstract', style="max-width:100%; min-width:100%;", rows=2),

                # http://jscolor.com/examples/
                Field('color', style="width:10%;", css_class="jscolor {width:243, height:150, position:'right', borderColor:'#FFF', insetColor:'#FFF', backgroundColor:'#666'}"),

                #Div(
                #    'progress_script',
                #    'progress_pre', 
                #    'progress_shot',
                #    'progress_post', 
                #    template="X/tmpl_slider_scene_progress.html"),
                Field('progress_script', template="X/tmpl_slider_progress_script.html"),
                Field('progress_pre', template="X/tmpl_slider_progress_pre.html"),
                Field('progress_shot', template="X/tmpl_slider_progress_shot.html"),
                Field('progress_post', template="X/tmpl_slider_progress_post.html"),

                Field('indentation', template="X/tmpl_slider_indentation.html"),
               
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
            active_note = Note(project=project, author=request.user)
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

    return render(request, 'X/script.html', {
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
#if not form.is_valid():
#    context['form_errors'] = form.errors
#    return render(request, template, context)

#and in your template:

#{% crispy form %}
#<div id='form-errors'>{{ form_errors }}</div>
