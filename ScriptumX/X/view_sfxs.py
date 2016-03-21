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
from django.db.models.functions import Lower

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, ButtonHolder, Div, Field, HTML
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.utils import render_crispy_form

from X.models import *
from X.forms import NoteForm
from X.views import g_tab_list
from X.views import Q
from X.common import *

from .tags import FormSymbol, sfx_tag_list, handleTagRequest, getTagRequestList

###############################################################################

class SFXForm(forms.ModelForm):
    """Edit form for SFX model"""
    class Meta:
        model = SFX
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
            'progress',
            ]

    def __init__(self, *args, **kwargs):
        super(SFXForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Div(
                Div(FormSymbol(sfx_tag_list[1]['img']),  Field('tag1'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(sfx_tag_list[2]['img']),  Field('tag2'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(sfx_tag_list[3]['img']),  Field('tag3'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(sfx_tag_list[4]['img']),  Field('tag4'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(sfx_tag_list[5]['img']),  Field('tag5'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(sfx_tag_list[6]['img']),  Field('tag6'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(sfx_tag_list[7]['img']),  Field('tag7'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(sfx_tag_list[8]['img']),  Field('tag8'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(sfx_tag_list[9]['img']),  Field('tag9'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(sfx_tag_list[10]['img']), Field('tag10'), style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(sfx_tag_list[11]['img']), Field('tag11'), style="padding:0; margin:0;", css_class='checkbox-inline'),
                css_class='col-sm-offset-2', style="margin-top:0px;", 
                ),

            Field('name', style="width:30em; min-width:30em; max-width:100%; "),

            Field('progress', template="X/tmpl_slider_progress.html"),

            Field('description', style="max-width:100%; min-width:100%;", rows=10),
            )

    def clean_name(self):
      name = self.cleaned_data.get('name')
      return name

###############################################################################

def sfx(request, sfx_id):
    """Handles page requests for SFXs"""

    env = Env(request)


    tag_list = getTagRequestList(request, 'sfx')

    #sfxs = get_list_or_404(SFX)
    
    try:
        active_sfx = SFX.objects.get(pk = sfx_id)
        active_id = active_sfx.id
        active_note = active_sfx.note
    except ObjectDoesNotExist:
        active_sfx = None
        active_id = None
        active_note = None

    ### create new sfx object on request '/sfx/0'
    if sfx_id == '0':
        active_sfx = SFX(project=env.project);

    ### handle buttons
    if request.method == 'POST':
        if not active_sfx:   # you shall not pass ... without valid scope
            raise AssertionError 

        # generate forms and/or get data out of the edited forms
        formNote = NoteForm(request.POST or None, instance=active_note)
        if formNote.is_valid():
            active_note = formNote.instance
        formItem = SFXForm(request.POST or None, instance=active_sfx)
        if formItem.is_valid():
            active_sfx = formItem.instance

        # 'Delete'-Button
        if request.POST.get('btn_delete'):
            if active_note:
                if active_note.id:
                    active_note.delete()
            active_sfx.note = None
            active_sfx.delete()
            return HttpResponseRedirect('/sfx/')

        # 'Add Note'-Button
        if request.POST.get('btn_note'):
            active_note = Note(project=env.project, author=env.user )
            active_sfx.note = active_note
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

            active_sfx.note = active_note

            if active_sfx:
                active_sfx.save()

            if sfx_id == '0':   # previously new item
                return HttpResponseRedirect('/sfx/' + str(active_sfx.id))
    else:
        formItem = SFXForm(instance=active_sfx)
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
    
    sfxs = SFX.objects.filter( project=env.project_id ).filter( query ).order_by(Lower('name'))

    return render(request, 'X/sfxs.html', {
        'title': 'SFX',
        'env': env,
        'tab_list': g_tab_list,
        'tab_active_id': 'X',
        'tag_list': tag_list,
        'sfxs': sfxs,
        'active_sfx': active_sfx,
        'active_id': active_id,
        'form': formItem,
        'formNote': formNote,
        'datetime': datetime.now(),
        #'error_message': "Please make a selection.",
    })

###############################################################################

def sfxTag(request, tag_id):

    handleTagRequest(request, tag_id, 'sfx')

    return sfx(request, None)

###############################################################################
