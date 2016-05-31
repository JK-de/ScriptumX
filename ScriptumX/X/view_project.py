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

from .tags import FormSymbol, handleTagRequest, getTagRequestList

###############################################################################

class ProjectForm(forms.ModelForm):
    """Edit form for Project model"""
    class Meta:
        model = Project
        fields = [
            'name',
            'users',
            'guests',
            'owner',
            ]

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Field('name', style="width:30em; min-width:30em; max-width:100%; "),

            Field('users', css_class='chosen-select-multi', style="max-width:100%; min-width:100%; min-height:48px;"),

            Field('guests', css_class='chosen-select-multi', style="max-width:100%; min-width:100%; min-height:48px;"),

            Field('owner', css_class='chosen-select-single'),
            )

    def clean_name(self):
      name = self.cleaned_data.get('name')
      return name

###############################################################################

class ScriptForm(forms.ModelForm):
    """Edit form for Script model"""
    class Meta:
        model = Script
        fields = [
            'name',
            'abstract',
            'description',
            'author',
            'version',
            'copyright',
            'persons',
            ]

    def __init__(self, *args, **kwargs):
        super(ScriptForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Field('name', style="width:30em; min-width:30em; max-width:100%; "),

            Field('abstract', style="max-width:100%; min-width:100%;", rows=2),

            Field('persons', css_class='chosen-select-multi', style="max-width:100%; min-width:100%; min-height:48px;"),

            Field('author', style="max-width:100%; min-width:100%;"),
            Field('version', style="max-width:100%; min-width:100%;"),
            Field('copyright', style="max-width:100%; min-width:100%;"),

            Field('description', style="max-width:100%; min-width:100%;", rows=10),
            )

    def clean_name(self):
      name = self.cleaned_data.get('name')
      return name

###############################################################################

@login_required
def project(request, project_id, script_id=None):
    """Handles page requests for Projects"""

    env = Env(request)

    selected_project = None
    selected_script = None
    
    if project_id == '0':
        ### create new project object on request '/project/0'
        selected_project = Project(owner=env.user);
    else:
        try:
            selected_project = Project.objects.get(pk = project_id)
        except ObjectDoesNotExist:
            selected_project = None

        if script_id == '0':
            ### create new project object on request '/project/0'
            if selected_project:
                selected_script = Script(project=selected_project);
            else:
                selected_script = Script(project=env.project);
        else:
            try:
                selected_script = Script.objects.get(pk = script_id)
            except ObjectDoesNotExist:
                selected_script = None


    formItemProject = None
    formItemScript = None
    
    if selected_script:
        
        ### handle buttons
        if request.method == 'POST':
            if not selected_script:   # you shall not pass ... without valid scope
                raise AssertionError 

            # generate forms and/or get data out of the edited forms
            formItemScript = ScriptForm(request.POST or None, instance=selected_script)
            if formItemScript.is_valid():
                selected_script = formItemScript.instance

            # 'Delete'-Button
            if request.POST.get('btn_delete'):
                selected_script.delete()
                return HttpResponseRedirect('/project/' + str(selected_project.id))

            # 'Save'-Button
            if request.POST.get('btn_save'):
                if formItemScript.is_valid():
                    formItemScript.save()

                if script_id == '0':   # previously new item
                    env.setProject(selected_project)
                    env.setScript(selected_script)
                    return HttpResponseRedirect('/project/' + str(selected_project.id) + '/' + str(selected_script.id))

            # 'Activate'-Button
            if request.POST.get('btn_activate'):
                env.setProject(selected_project)
                env.setScript(selected_script)

        else:
            formItemScript = ScriptForm(instance=selected_script)
    
    elif selected_project:

        ### handle buttons
        if request.method == 'POST':
            if not selected_project:   # you shall not pass ... without valid scope
                raise AssertionError 

            # generate forms and/or get data out of the edited forms
            formItemProject = ProjectForm(request.POST or None, instance=selected_project)
            if formItemProject.is_valid():
                selected_project = formItemProject.instance

            # 'Delete'-Button
            if request.POST.get('btn_delete'):
                selected_project.delete()
                return HttpResponseRedirect('/project/')

            # 'Save'-Button
            if request.POST.get('btn_save'):
                if formItemProject.is_valid():
                    formItemProject.save()

                if project_id == '0':   # previously new item
                    return HttpResponseRedirect('/project/' + str(selected_project.id))
        else:
            formItemProject = ProjectForm(instance=selected_project)

    ### conglomerate queries
    
    projects = Project.objects.filter( Q(owner=env.user) | Q(users=env.user) | Q(guests=env.user) ).distinct()

    if selected_project:
        scripts = Script.objects.filter( project=selected_project )
        scenes_project_id = selected_project.id
    else:
        scripts = Script.objects.filter( project=env.project )
        scenes_project_id = env.project_id


    return render(request, 'X/project.html', {
        'title': 'Project',
        'env': env,
        'tab_list': g_tab_list,
        'tab_active_id': 'P',
        'projects': projects,
        'scripts': scripts,
        'selected_project': selected_project,
        'selected_script': selected_script,
        'formScript': formItemScript,
        'formProject': formItemProject,
        'scenes_project_id': scenes_project_id,
        #'error_message': "Please make a selection.",
    })

###############################################################################

@login_required
def project_import(request):
    """Handles import page"""
    
    return render(request, 'X/home.html', {
        'title': 'Home',
    })

###############################################################################


###############################################################################
