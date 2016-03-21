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

            Field('users'),

            )

    def clean_name(self):
      name = self.cleaned_data.get('name')
      return name

###############################################################################

def project(request, project_id):
    """Handles page requests for Projects"""

    env = Env(request)


    tag_list = getTagRequestList(request, 'project')

    #projects = get_list_or_404(Project)
    
    try:
        active_project = Project.objects.get(pk = project_id)
        active_id = active_project.id
    except ObjectDoesNotExist:
        active_project = None
        active_id = None

    ### create new project object on request '/project/0'
    if project_id == '0':
        active_project = Project(project=env.project);

    ### handle buttons
    if request.method == 'POST':
        if not active_project:   # you shall not pass ... without valid scope
            raise AssertionError 

        # generate forms and/or get data out of the edited forms
        formItem = ProjectForm(request.POST or None, instance=active_project)
        if formItem.is_valid():
            active_project = formItem.instance

        # 'Delete'-Button
        if request.POST.get('btn_delete'):
            active_project.delete()
            return HttpResponseRedirect('/project/')

        # 'Save'-Button
        if request.POST.get('btn_save'):
            if active_project:
                active_project.save()

            if project_id == '0':   # previously new item
                return HttpResponseRedirect('/project/' + str(active_project.id))
    else:
        formItem = ProjectForm(instance=active_project)
    
    ### conglomerate queries
    
    projects = Project.objects.filter( users=env.user ).order_by(Lower('name'))

    return render(request, 'X/project.html', {
        'title': 'Project',
        'env': env,
        'tab_list': g_tab_list,
        'tab_active_id': 'P',
        'projects': projects,
        'active_project': active_project,
        'active_id': active_id,
        'form': formItem,
        'datetime': datetime.now(),
        #'error_message': "Please make a selection.",
    })

###############################################################################


###############################################################################
