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

from .tags import FormSymbol, role_tag_list, handleTagRequest, getTagRequestList

###############################################################################

class RoleForm(forms.ModelForm):
    """Edit form for Role model"""
    class Meta:
        model = Role
        fields = [
            'tag1',
            'tag2',
            'tag3',
            'name',
            'description',
            'color',
            'actor',
            'gadgets',
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

            Div(
                Div(FormSymbol(role_tag_list[1]['img']),  Field('tag1'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(role_tag_list[2]['img']),  Field('tag2'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(role_tag_list[3]['img']),  Field('tag3'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                css_class='col-sm-offset-2', style="margin-top:0px;", 
                ),

            #Field('name', style="width:30em; min-width:10em; max-width:100%; "),
            Field('name'),

            Field('actor', css_class='chosen-select-box'),

            Field('gadgets', css_class='chosen-select', style="max-width:100%; min-width:100%; min-height:48px;"),

            Field('color'),

            Field('description', style="max-width:100%; min-width:100%;", rows=10),

            )

    def clean_name(self):
      name = self.cleaned_data.get('name')
      return name

###############################################################################

@login_required
def role(request, role_id):
    """Handles page requests for Roles"""

    env = Env(request)


    tag_list = getTagRequestList(request, 'role')

    #roles = get_list_or_404(Role)
    
    try:
        selected_role = Role.objects.get(pk = role_id)
        selected_note = selected_role.note
    except ObjectDoesNotExist:
        selected_role = None
        selected_note = None

    ### create new role object on request '/role/0'
    if role_id == '0':
        selected_role = Role(project=env.project);

    ### handle buttons
    if request.method == 'POST':
        if not selected_role:   # you shall not pass ... without valid scope
            raise AssertionError 

        # generate forms and/or get data out of the edited forms
        formNote = NoteForm(request.POST or None, instance=selected_note)
        if formNote.is_valid():
            selected_note = formNote.instance
        formItem = RoleForm(request.POST or None, instance=selected_role)
        if formItem.is_valid():
            selected_role = formItem.instance

        # 'Delete'-Button
        if request.POST.get('btn_delete'):
            if selected_note:
                if selected_note.id:
                    selected_note.delete()
            selected_role.note = None
            selected_role.delete()
            return HttpResponseRedirect('/role/')

        # 'Add Note'-Button
        if request.POST.get('btn_note'):
            selected_note = Note(project=env.project, author=env.user )
            selected_role.note = selected_note
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

            selected_role.note = selected_note

            if selected_role:
                if formItem.is_valid():
                    formItem.save()
                #selected_role.save()

            if role_id == '0':   # previously new item
                return HttpResponseRedirect('/role/' + str(selected_role.id))
    else:
        formItem = RoleForm(instance=selected_role)
        formNote = NoteForm(instance=selected_note)
    
    formItem.fields['actor'].queryset = Person.objects.filter(project=env.project)
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
    
    roles = Role.objects.filter( project=env.project_id ).filter( query ).order_by(Lower('name'))

    return render(request, 'X/roles.html', {
        'title': 'Role',
        'env': env,
        'tab_list': g_tab_list,
        'tab_active_id': 'R',
        'tag_list': tag_list,
        'roles': roles,
        'selected_role': selected_role,
        'form': formItem,
        'formNote': formNote,
        #'error_message': "Please make a selection.",
    })

###############################################################################

@login_required
def roleTag(request, tag_id):

    handleTagRequest(request, tag_id, 'role')

    return role(request, None)

###############################################################################
