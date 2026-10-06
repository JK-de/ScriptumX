"""
Definition of views.
"""

from os import path
from datetime import datetime
import random

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.utils import timezone
from django.views.generic import View, ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Lower
from django.views.generic.base import TemplateView
from django import forms

from crispy_forms.utils import render_crispy_form
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, ButtonHolder, Div, Field, HTML, Submit, Hidden
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.utils import render_crispy_form

from X.models import Scene
from X.common import Env, getTagQuery, bind_scope_to_request

from X.tags import FormSymbol, scene_tag_list, handleTagRequest, getTagRequestList

from django import http
from django.template.loader import get_template
from django.template import Context
import xhtml2pdf.pisa as pisa
try:
    import StringIO
    StringIO = StringIO.StringIO
except Exception:
    from io import StringIO

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
    report_url_name = 'C_Script'

    def get_report_url_name(self):
        return self.report_url_name

    def render_form(self, request, form):
        from report.collab import attach_collab_fields
        if 'preset_name' not in form.fields:
            attach_collab_fields(form, request, self.x_group, self.get_report_url_name())
        return render(
            request, 
            self.template_name, {
            'title': self.title,
            'form': form,
            })

    def render_list(self, request, form, tag_list):
        from report.collab import apply_advanced_scene_filters, filter_payload_from_request_form
        env = Env(request)

        options = {}

        options['show_notes'] = form.cleaned_data['show_notes']
        options['show_details'] = form.cleaned_data.get('show_details', False)
        options['columns'] = form.cleaned_data.get('columns', 4)

        query = getTagQuery(tag_list)
        scenes = Scene.objects.filter(project=env.project_id, script=env.script_id).filter(query).order_by('order')
        payload = filter_payload_from_request_form(request, form, self.x_group)
        scenes = apply_advanced_scene_filters(scenes, payload)

        self.template_name = "report/cards_script.html"
        self.context = {
            'title': 'Script: ' + (env.script.name if env.script else 'Script'),
            'env': env,
            'scenes': scenes,
            'options': options,
            'shared_read_only': bool(getattr(request, '_share_context', None)),
            }

        return render(
            request, 
            self.template_name, 
            self.context )

    def get(self, request, *args, **kwargs):
        from report.collab import prepare_filter_form
        tag_list = getTagRequestList(request, self.x_group)
        initial = dict(self.initial)
        for tag in tag_list:
            initial['tag' + str(tag['idx'])] = tag['active']
        form = prepare_filter_form(self, request, initial=initial)
        return self.render_form(request, form)

    def post(self, request, *args, **kwargs):
        from report.collab import handle_collab_post, prepare_filter_form
        form = prepare_filter_form(self, request, data=request.POST)
        tag_list = getTagRequestList(request, self.x_group)
        handled = handle_collab_post(self, request, form, tag_list, self.get_report_url_name())
        if handled is not None:
            return handled
        if form.is_valid():
            for tag in tag_list:
                tag['active'] = form.cleaned_data['tag' + str(tag['idx'])]
            return self.render_list(request, form, tag_list)

        return self.render_form(request, form)

###############################################################################
###############################################################################

@login_required
def cards(request, scene_id=None):
    """Legacy quick scene-cards dump (nav used to link /test here).

    Prefer CardsView at /report/C/script. Kept so /test does not 500.
    """
    env = Env(request)
    scenes = Scene.objects.filter(
        project=env.project_id, script=env.script_id
    ).order_by('order')
    return render(request, 'report/cards_script.html', {
        'title': 'Script: ' + (env.script.name if env.script else 'Script'),
        'env': env,
        'scenes': scenes,
        'options': {
            'show_notes': True,
            'show_details': True,
            'columns': 4,
        },
    })

###############################################################################
