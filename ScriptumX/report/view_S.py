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

def collect_sceneheader(list, scene, options):
    link = None

    t = ''
    if scene.short:
        t += '[' + scene.short + '] '

    t += scene.name

    if scene.story_location:
        t += ' - ' + scene.story_location.name

    if scene.story_time:
        t += ' - ' + scene.story_time.name + ' (' + str(scene.story_time.day) + '. ' + str(scene.story_time.hour) + 'h)'

    if options['show_links']:
        link = '/script/' + str(scene.id)

    item = { 'class':'sceneheading', 'text':t, 'href':link}
    list.append(item)

###############################################################################

def collect_sceneitems(list, scene, sceneitems, options):
    link = None

    for sceneitem in sceneitems:
        if options['show_links']:
            link = '/scene/' + str(sceneitem.id)

        if sceneitem.type == 'A':
            item = { 'class':'action', 'text':sceneitem.text, 'href':link}
            list.append(item)
        
        if sceneitem.type == 'T':
            item = { 'class':'transition', 'text':sceneitem.text, 'href':link}
            list.append(item)

        if sceneitem.type == 'D':
            item = { 'class':'character', 'text':sceneitem.role.name}
            list.append(item)
            if sceneitem.parenthetical:
                item = { 'class':'parenthetical', 'text':sceneitem.parenthetical}
                list.append(item)
            if sceneitem.text:
                color = None
                if sceneitem.role in options['colorize_roles']:
                    color = sceneitem.role.color
                item = { 'class':'dialog', 'text':sceneitem.text, 'color':color, 'href':link}
                list.append(item)

        if sceneitem.type == 'R':
            item = { 'class':'character', 'text':sceneitem.role.name}
            list.append(item)
            if sceneitem.text:
                item = { 'class':'action', 'text':sceneitem.text, 'href':link}
                list.append(item)

        if sceneitem.type == 'N':
            if options['show_notes']:
                item = { 'class':'note', 'text':sceneitem.text, 'href':link}
                list.append(item)


###############################################################################

@login_required
def script(request, scene_id=None):
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
    
    sceneitems = SceneItem.objects.filter(scene=env.scene).order_by('order')

    list = []

    collect_sceneheader(list, env.scene)
    collect_sceneitems(list, env.scene, sceneitems)

    return render(request, 'report/script.html', {
        'title': 'Script',
        'env': env,
        'scenes': scenes,
        'sceneitems': sceneitems,
        'scriptitems': list,
        #'error_message': "Please make a selection.",
    })

###############################################################################

class ScriptFilterForm(forms.Form):

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
    
    show_links = forms.BooleanField(
        label = "Show Links", 
        required = False,
        )
    
    choices = (
        ('legacy|"Courier New", Courier, monospace|',                       
            'Legacy - Courier (Typewriter Style)'), 
        ('legacy|"Times New Roman", Times, serif|',                       
            'Legacy - Times (Serif)'), 
        ('modern|Arial, Helvetica, sans-serif|',                            
            'Modern Helvetica (Sans Serif)'),
        ('modern|"Lucida Sans Unicode", "Lucida Grande", sans-serif|',      
            'Modern Lucida (Sans Serif)'),
        ('modern|Verdana, Geneva, sans-serif|',                             
            'Modern Verdana (Sans Serif)'),
        ('modern|"Times New Roman", Times, serif|',                         
            'Modern Times (Serif)'),
        ('modern|"Palatino Linotype", "Book Antiqua", Palatino, serif|',    
            'Modern Palatino (Serif)'),
        ('modern|"Lucida Console", Monaco, monospace|',                     
            'Modern Console (Monospace)'),
        ('modern|"Trebuchet MS", Helvetica, sans-serif|',                     
            'Modern Trebuchet MS (Sans Serif)'),

        ('modern|Amiri, serif|Amiri:400,700,400italic,700italic',                     
            'G Amiri (Sans Serif)'),
        ('modern|Lato, serif|Lato:400,700,400italic,700italic',                     
            'G Lato (Sans Serif)'),
        ('modern|"Open Sans", sans-serif|Open+Sans:400,700,400italic,700italic',
            'G Open Sans (Sans Serif)'),
        ('modern|"Source Sans Pro", sans-serif|Source+Sans+Pro:400,700,400italic,700italic',
            'G Source Sans Pro (Sans Serif)'),
        ('modern|"PT Serif", serif|PT+Serif:400,700,400italic,700italic',
            'G PT Serif (Serif)'),
        ('modern|"PT Sans", sans-serif|PT+Sans:400,700,700italic,400italic',
            'G PT Sans (Sans Serif)'),
        ('modern|"Source Serif Pro", serif|Source+Serif+Pro:400,700',
            'G Source Serif Pro (Sans Serif)'),
        ('modern|"Source Code Pro"|Source+Code+Pro:400,700',
            'G Source Code Pro (Monospace)'),
        ('modern|"PT Mono"|PT+Mono',
            'G PT Mono (Monospace)'),
        ('modern|"Cutive Mono"|Cutive+Mono',
            'G Cutive Mono (Monospace)'),
        ('modern|"Alegreya Sans", sans-serif|Alegreya+Sans:400,700,400italic,700italic',
            'G Alegreya Sans (Sans Serif)'),
        ('modern|"Droid Sans Mono"|Droid+Sans+Mono',
            'G Droid Sans Mono (Monospace)'),
        ('modern|Rambla, sans-serif|Rambla:400,400italic,700,700italic',
            'G Rambla (Sans Serif)'),

        ('test|"Courier New", Courier, monospace|',                       
            'TEST'), 
        )
    #https://www.google.com/fonts
    layout = forms.TypedChoiceField(
        label = "Layout",
        choices = choices,
        #widget = forms.RadioSelect,
        initial = choices[0][0],
        required = False,
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

    roles_queryset = Role.objects.all()
    #roles_queryset = Role.objects.none()
    #roles_queryset = Role.objects.first()
    roles = forms.ModelMultipleChoiceField(
        label = "Colorize Roles", 
        queryset=roles_queryset, 
        widget=forms.CheckboxSelectMultiple(),
        required = False,
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-FilterForm'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-7'

        self.helper.add_input(Submit('show', 'Show Script'))
        self.helper.add_input(Submit('pdf', 'Download PDF'))

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
            Field('show_links'), 
            Field('layout'), 
            #Field('checkboxes'),
            Field('roles'),
        )

###############################################################################

class ScriptView(View):
    form_class = ScriptFilterForm
    x_group = 'scene'
    initial = {'show_notes': True}
    template_name = "report/common_form.html"
    title = 'Script'
    selected_scene_id = None

    def render_form(self, request, form):
        env = Env(request)

        form.fields['roles'].queryset = Role.objects.filter(project=env.project)

        return render(
            request, 
            self.template_name, {
            'title': self.title,
            'form': form,
            })

    def render_list(self, request, form, tag_list):
        env = Env(request)

        list = []
        options = {}

        options['show_notes'] = form.cleaned_data['show_notes']
        options['show_links'] = form.cleaned_data['show_links']
        options['colorize_roles'] = form.cleaned_data['roles']
        options['layout'] = form.cleaned_data['layout']
        pdf = request.POST.get('pdf')

        if self.selected_scene_id:
            pass

        query = getTagQuery(tag_list)
        scenes = Scene.objects.filter(project=env.project_id, script=env.script_id).filter(query).order_by('order')

        for scene in scenes:    
            sceneitems = SceneItem.objects.filter(scene=scene).order_by('order').select_related()

            collect_sceneheader(list, scene, options)
            collect_sceneitems(list, scene, sceneitems, options)

        template, font, google_link = form.cleaned_data['layout'].split('|', 2)

        self.template_name = "report/script_" + template + ".html"
        self.context = {
            'title': 'Script: ' + env.script.name,
            'font': font,
            'google_link': google_link,
            'env': env,
            'scenes': scenes,
            'sceneitems': sceneitems,
            'scriptitems': list,
            'PDF': pdf,
            'options': options,
            }

        if pdf:
            return render_to_pdf_response(
                self.template_name, 
                self.context )
        else:
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
