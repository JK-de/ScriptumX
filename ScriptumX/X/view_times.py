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

from .tags import FormSymbol, time_tag_list, handleTagRequest, getTagRequestList

###############################################################################

class TimeForm(forms.ModelForm):
    """Edit form for Time model"""
    class Meta:
        model = Time
        fields = [
            'tag1',
            'tag2',
            'tag3',
            'tag4',
            'tag5',
            'name',
            'abstract',
            'description',
            'persons',
            'gadgets',
            'day',
            'hour'
            ]

    def __init__(self, *args, **kwargs):
        #super(TimeForm, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Div(
                Div(FormSymbol(time_tag_list[1]['img']),  Field('tag1'),  title=time_tag_list[1]['name'], css_class='checkbox-inline checkbox-tags'),
                Div(FormSymbol(time_tag_list[2]['img']),  Field('tag2'),  title=time_tag_list[2]['name'], css_class='checkbox-inline checkbox-tags'),
                Div(FormSymbol(time_tag_list[3]['img']),  Field('tag3'),  title=time_tag_list[3]['name'], css_class='checkbox-inline checkbox-tags'),
                Div(FormSymbol(time_tag_list[4]['img']),  Field('tag4'),  title=time_tag_list[4]['name'], css_class='checkbox-inline checkbox-tags'),
                Div(FormSymbol(time_tag_list[5]['img']),  Field('tag5'),  title=time_tag_list[5]['name'], css_class='checkbox-inline checkbox-tags'),
                css_class='col-sm-offset-2 checkbox-tags-group', 
                ),

            Field('name'),
            Field('abstract', rows=1),

            Field('day'),
            Field('hour'),

            Field('persons', css_class='chosen-select-multi'),
            Field('gadgets', css_class='chosen-select-multi'),

            Field('description', style="max-width:100%; min-width:100%;", rows=10),
            )

        for field_name in self.fields:
            if field_name[:3] == 'tag':
                field = self.fields.get(field_name)
                field.label = ''

    def clean_name(self):
      name = self.cleaned_data.get('name')
      return name

###############################################################################

@login_required
def time(request, time_id):
    """Handles page requests for Times"""

    env = Env(request)


    tag_list = getTagRequestList(request, 'time')

    #times = get_list_or_404(Time)
    
    try:
        selected_time = Time.objects.get(pk = time_id)
        selected_note = selected_time.note
    except ObjectDoesNotExist:
        selected_time = None
        selected_note = None

    ### create new time object on request '/time/0'
    if time_id == '0':
        selected_time = Time(project=env.project);

    ### handle buttons
    if request.method == 'POST':
        if not selected_time:   # you shall not pass ... without valid scope
            raise AssertionError 

        # generate forms and/or get data out of the edited forms
        formNote = NoteForm(request.POST or None, instance=selected_note)
        if formNote.is_valid():
            selected_note = formNote.instance
        formItem = TimeForm(request.POST or None, instance=selected_time)
        if formItem.is_valid():
            selected_time = formItem.instance

        # 'Delete'-Button
        if request.POST.get('btn_delete'):
            if selected_note:
                if selected_note.id:
                    selected_note.delete()
            selected_time.note = None
            selected_time.delete()
            return HttpResponseRedirect('/time/')

        # 'Add Note'-Button
        if request.POST.get('btn_note'):
            selected_note = Note(project=env.project, author=env.user )
            selected_time.note = selected_note
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

            selected_time.note = selected_note

            if selected_time:
                if formItem.is_valid():
                    formItem.save()
                #selected_time.save()

            if time_id == '0':   # previously new item
                return HttpResponseRedirect('/time/' + str(selected_time.id))
    else:
        formItem = TimeForm(instance=selected_time)
        formNote = NoteForm(instance=selected_note)

    formItem.fields['persons'].queryset = Person.objects.filter(project=env.project)
    formItem.fields['gadgets'].queryset = Gadget.objects.filter(project=env.project)

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
    
    times = Time.objects.filter( project=env.project_id ).filter( query ).order_by('day', 'hour')

    return render(request, 'X/times.html', {
        'title': 'Time',
        'env': env,
        'tab_list': g_tab_list,
        'tab_active_id': 'T',
        'tag_list': tag_list,
        'times': times,
        'selected_time': selected_time,
        'form': formItem,
        'formNote': formNote,
        #'error_message': "Please make a selection.",
    })

###############################################################################

@login_required
def timeTag(request, tag_id):

    handleTagRequest(request, tag_id, 'time')

    return time(request, None)

###############################################################################
