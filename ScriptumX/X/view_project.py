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

from .tags import FormSymbol, project_tag_list, handleTagRequest, getTagRequestList

###############################################################################

class ProjectForm(forms.ModelForm):
    """Edit form for Project model"""
    class Meta:
        model = Project
        fields = [
            'name',
            'users',
            'guests',
            'owner'
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

            Field('users', css_class='chosen-select', style="max-width:100%; min-width:100%; min-height:48px;"),

            Field('guests', css_class='chosen-select', style="max-width:100%; min-width:100%; min-height:48px;"),

            Field('owner', css_class='chosen-select-box'),
            )

    def clean_name(self):
      name = self.cleaned_data.get('name')
      return name

###############################################################################

@login_required
def project(request, project_id, script_id=0):
    """Handles page requests for Projects"""

    env = Env(request)


    tag_list = getTagRequestList(request, 'project')

    #projects = get_list_or_404(Project)
    
    try:
        selected_project = Project.objects.get(pk = project_id)
        selected_id = selected_project.id
    except ObjectDoesNotExist:
        selected_project = None
        selected_id = None

    ### create new project object on request '/project/0'
    if project_id == '0':
        selected_project = Project(project=env.project);
    
    #TODO
    ### handle buttons
    if request.method == 'POST':
        if not selected_project:   # you shall not pass ... without valid scope
            raise AssertionError 

        # generate forms and/or get data out of the edited forms
        formItem = ProjectForm(request.POST or None, instance=selected_project)
        if formItem.is_valid():
            selected_project = formItem.instance

        # 'Delete'-Button
        if request.POST.get('btn_delete'):
            selected_project.delete()
            return HttpResponseRedirect('/project/')

        # 'Save'-Button
        if request.POST.get('btn_save'):
            if selected_project:
                selected_project.save()

            if project_id == '0':   # previously new item
                return HttpResponseRedirect('/project/' + str(selected_project.id))
    else:
        formItem = ProjectForm(instance=selected_project)
    
    ### conglomerate queries
    
    projects = Project.objects.filter( users=env.user )
    scripts = Script.objects.filter( project=env.project )

    return render(request, 'X/project.html', {
        'title': 'Projects',
        'env': env,
        'tab_list': g_tab_list,
        'tab_active_id': 'P',
        'projects': projects,
        'scripts': scripts,
        'selected_project': selected_project,
        'selected_project_id': selected_id,
        'form': formItem,
        'datetime': datetime.now(),
        #'error_message': "Please make a selection.",
    })

###############################################################################

@login_required
def project_import(request):
    """Handles import page"""
    
    return render(request, 'X/home.html', {
        'title': 'Home',
        'datetime': datetime.now(),
    })

###############################################################################


###############################################################################
