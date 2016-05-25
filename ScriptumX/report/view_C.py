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
from django.views.generic import View, ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.db.models.functions import Lower
from django.views.generic.base import TemplateView
from django import forms

from crispy_forms.utils import render_crispy_form
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, ButtonHolder, Div, Field, HTML, Submit, Hidden
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.utils import render_crispy_form

#from report.models import *
from X.models import *
from X.views import g_tab_list
from X.views import Q
from X.common import *

from X.tags import FormSymbol, sceneitem_tag_list, handleTagRequest, getTagRequestList

# pip install xhtml2pdf==0.1a3
# https://pypi.python.org/pypi/xhtml2pdf/0.1a3
from django import http
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
import xhtml2pdf.pisa as pisa
try:
    import StringIO
    StringIO = StringIO.StringIO
except Exception:
    from io import StringIO
import cgi

#from django_xhtml2pdf.utils import render_to_pdf_response
from .pdf_utils import render_to_pdf_response

###############################################################################

class CardsFilterForm(forms.Form):

    tag0 = forms.BooleanField(label = "", required = False,)
    tag1 = forms.BooleanField(label = "", required = False,)
    tag2 = forms.BooleanField(label = "", required = False,)
    tag3 = forms.BooleanField(label = "", required = False,)
    tag4 = forms.BooleanField(label = "", required = False,)
    tag5 = forms.BooleanField(label = "", required = False,)

    show_notes = forms.BooleanField(
        label = "Show Notes", 
        required = False,
        )
    
    show_details = forms.BooleanField(
        label = "Show Details", 
        required = False,
        )
    
    columns = forms.IntegerField(
        label = "Columns", 
        required = False,
        min_value = 1,
        max_value = 10,
        )

    #checkboxes = forms.MultipleChoiceField(
    #    label = "Test", 
    #    choices = (('option_one', "Option one is this and that be sure to include why it's great"), 
    #        ('option_two', 'Option two can also be checked and included in form results'),
    #        ('option_three', 'Option three can yes, you guessed it also be checked and included in form results')),
    #    initial = 'option_one',
    #    widget = forms.CheckboxSelectMultiple,
    #    help_text = "<strong>Note:</strong> Labels surround all the options for much larger click areas and a more usable form.",
    #    required = False,
    #    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-FilterForm'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-7'

        self.helper.add_input(Submit('show', 'Show Scene Cards'))

        self.helper.layout = Layout(
            Div(#Div(FormSymbol(scene_tag_list[0]['img']), Field('tag0'), style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(scene_tag_list[1]['img']),  Field('tag1'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(scene_tag_list[2]['img']),  Field('tag2'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(scene_tag_list[3]['img']),  Field('tag3'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(scene_tag_list[4]['img']),  Field('tag4'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(scene_tag_list[5]['img']),  Field('tag5'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                css_class='col-sm-offset-2', style="margin-top:0px;",
                ),

            Field('show_notes'), 
            Field('show_details'), 
            Field('columns'), 
        )

###############################################################################

class CardsView(View):
    form_class = CardsFilterForm
    x_group = 'scene'
    initial = {'show_notes': True, 'show_details': True, 'columns':4}
    template_name = "report/common_form.html"
    title = 'Scene Cards'
    selected_scene_id = None

    def render_form(self, request, form):
        env = Env(request)

        return render(
            request, 
            self.template_name, {
            'title': self.title,
            'form': form,
            })

    def render_list(self, request, form, tag_list):
        env = Env(request)

        options = {}

        options['show_notes'] = form.cleaned_data['show_notes']
        options['show_details'] = form.cleaned_data['show_details']
        #options['show_links'] = form.cleaned_data['show_links']
        #options['colorize_roles'] = form.cleaned_data['roles']
        #options['layout'] = form.cleaned_data['layout']
        #pdf = request.POST.get('pdf')
        options['columns'] = form.cleaned_data['columns']

        query = getTagQuery(tag_list)
        scenes = Scene.objects.filter(project=env.project_id, script=env.script_id).filter(query).order_by('order')

        self.template_name = "report/cards_script.html"
        self.context = {
            'title': 'Script: ' + env.script.name,
            'env': env,
            'scenes': scenes,
            'options': options,
            }

        return render(
            request, 
            self.template_name, 
            self.context )

    def get(self, request, *args, **kwargs):
        tag_list = getTagRequestList(request, self.x_group)
        for tag in tag_list:
            self.initial['tag' + str(tag['idx'])] = tag['active']
        form = self.form_class(initial=self.initial)
        return self.render_form(request, form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            tag_list = getTagRequestList(request, self.x_group)
            for tag in tag_list:
                tag['active'] = form.cleaned_data['tag' + str(tag['idx'])]
            return self.render_list(request, form, tag_list)

        return self.render_form(request, form)

###############################################################################
###############################################################################

@login_required
def cards(request, scene_id=None):
    """Handles page requests for SceneItems"""

    env = Env(request)

    ### conglomerate queries
    #query = Q()
    #for tag in tag_list:
    #    if tag['active']:
    #        if len(query)==0:
    #            query = Q(type=tag['type'])
    #        else:
    #            query |= Q(type=tag['type'])

    #if len(query)==len(tag_list):
    #    query = Q()

    scenes = Scene.objects.filter(project=env.project_id, script=env.script_id).order_by('order')

    return render(request, 'report/scene_cards.html', {
        'title': 'Script',
        'env': env,
        'scenes': scenes,
        'columns': 5,
        #'error_message': "Please make a selection.",
    })

###############################################################################
