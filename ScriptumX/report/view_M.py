from os import path
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.template import RequestContext
from django.utils import timezone
from django.views.generic import View, ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.functions import Lower
from django.views.generic.base import TemplateView
from django import forms

from crispy_forms.utils import render_crispy_form
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, ButtonHolder, Div, Field, HTML, Submit
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineCheckboxes

#from easy_pdf.views import PDFTemplateView

from report.models import *
from X.models import *
from X.common import *
from X.tags import FormSymbol, gadget_tag_list, handleTagRequest, getTagRequestList
from .M import *
from .view_L import *

###############################################################################

#http://www.fileformat.info/info/unicode/char/search.htm?q=circle&preview=entity
M_SYMBOL_PERVASIVE = "&#x26ac;"   # MEDIUM SMALL WHITE CIRCLE
M_SYMBOL_LINKED_INDIRECT = "&#x26AA;"   # MEDIUM WHITE CIRCLE
M_SYMBOL_LINKED = "&#x26AB;"   # MEDIUM BLACK CIRCLE
#◯⊙⊚⊛⊗⦿⭕⦾⚪⚫○●⚬•❍✪➲⌼⎊◌◍◖◗⚇⚉❂❶➀⓵⇴     𝒳𝓧𝓍𝔁   𝒮𝒸𝓇𝒾𝓅𝓉𝓊𝓂𝒳   𝒮𝒳   𝓢𝓧   &#x1d4e7;

###############################################################################

class M_BaseView(View):
    form_class = GadgetFilterForm
    x_group = '???'
    initial = {}
    template_name = "report/M_X.html"
    title = '??? List'

    def render_form(self, request, form):
        return render(request, self.template_name, {
            'title': self.title,
            'form': form,
        })

    #def render_list(self, request, form, tag_list):

    def get(self, request, *args, **kwargs):
        tag_list = getTagRequestList(request, self.x_group)
        for tag in tag_list:
            self.initial['tag'+str(tag['idx'])] = tag['active']
        form = self.form_class(initial=self.initial)
        return self.render_form(request, form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            tag_list = getTagRequestList(request, self.x_group)
            for tag in tag_list:
                tag['active'] = form.cleaned_data['tag'+str(tag['idx'])]
            return self.render_list(request, form, tag_list)

        return self.render_form(request, form)

###############################################################################

class M_SceneRoleView(M_BaseView):
    form_class = RoleFilterForm
    x_group = 'role'
    initial = {'show_notes': True}
    title = 'Scene vs Role Matrix'

    def render_list(self, request, form, tag_list):
        env = Env(request)
        query = getTagQuery(tag_list)
        roles = Role.objects.filter( project=env.project_id ).filter(query).order_by(Lower('name'))
        scenes = Scene.objects.filter( project=env.project_id, script=env.script_id ).order_by('order')

        m = M(roles, scenes)

        for role in roles:
            col = m.getColIndex(role)
            m.cells[0][col].background_color = role.color

        for scene in scenes:
            row = m.getRowIndex(scene)

            sceneitems = SceneItem.objects.filter( scene=scene )
            for sceneitem in sceneitems:
                if sceneitem.role:
                    col = m.getColIndex(sceneitem.role)
                    if col:
                        m.cells[row][col].text = M_SYMBOL_LINKED

        return render(request, self.template_name, {
            'title': self.title,
            'env': env,
            'tag_list': tag_list,
            'M': m,
            'show_notes': form.cleaned_data['show_notes'],
        })

###############################################################################

class M_ScenePersonView(M_BaseView):
    form_class = PersonFilterForm
    x_group = 'person'
    initial = {'show_notes': True}
    title = 'Scene vs Person Matrix'

    def render_list(self, request, form, tag_list):
        env = Env(request)
        query = getTagQuery(tag_list)
        persons = Person.objects.filter( project=env.project_id ).filter(query).order_by(Lower('name'))
        scenes = Scene.objects.filter( project=env.project_id, script=env.script_id ).order_by('order')

        m = M(persons, scenes)

        #for person in persons:
        #    col = m.getColIndex(person)
        #    #m.cells[0][col].background_color = person.color

        for scene in scenes:
            row = m.getRowIndex(scene)

            # mark pervasive gadgets
            for person in persons:
                if person.pervasive:
                    col = m.getColIndex(person)
                    m.cells[row][col].text = M_SYMBOL_PERVASIVE   # MEDIUM SMALL WHITE CIRCLE

            # search for linked persons over scene -> sceneitem -> role.actor
            sceneitems = SceneItem.objects.filter( scene=scene )
            for sceneitem in sceneitems:
                if sceneitem.role:
                    linked_person = sceneitem.role.actor
                    if linked_person:
                        col = m.getColIndex(linked_person)
                        if col:
                            m.cells[row][col].text = M_SYMBOL_LINKED   # MEDIUM WHITE CIRCLE

            # search for linked persons over scene -> story_time.persons
            linked_time = scene.story_time
            if linked_time:
                linked_persons = linked_time.persons.all()
                for item in linked_persons:
                    col = m.getColIndex(item)
                    if col:
                        m.cells[row][col].text = M_SYMBOL_LINKED

            # search for linked persons over scene -> story_location.persons
            linked_location = scene.story_location
            if linked_location:
                linked_persons = linked_location.persons.all()
                for item in linked_persons:
                    col = m.getColIndex(item)
                    if col:
                        m.cells[row][col].text = M_SYMBOL_LINKED

            # search for linked gadgets
            linked_persons = scene.persons.all()
            for item in linked_persons:
                col = m.getColIndex(item)
                if col:
                    m.cells[row][col].text = M_SYMBOL_LINKED   # MEDIUM BLACK CIRCLE

        return render(request, self.template_name, {
            'title': self.title,
            'env': env,
            'tag_list': tag_list,
            'M': m,
            'show_notes': form.cleaned_data['show_notes'],
        })

###############################################################################

class M_SceneGadgetView(M_BaseView):
    form_class = GadgetFilterForm
    x_group = 'gadget'
    initial = {'show_notes': True}
    title = 'Scene vs Gadget Matrix'

    def render_list(self, request, form, tag_list):
        env = Env(request)
        query = getTagQuery(tag_list)
        gadgets = Gadget.objects.filter( project=env.project_id ).filter(query).order_by(Lower('name'))
        scenes = Scene.objects.filter( project=env.project_id, script=env.script_id ).order_by('order')

        m = M(gadgets, scenes)

        #for gadget in gadgets:
        #    col = m.getColIndex(gadget)
        #    #m.cells[0][col].background_color = gadget.color

        for scene in scenes:
            row = m.getRowIndex(scene)

            # mark pervasive gadgets
            for gadget in gadgets:
                if gadget.pervasive:
                    col = m.getColIndex(gadget)
                    m.cells[row][col].text = M_SYMBOL_PERVASIVE

            # search for linked gadgets over scene -> sceneitem -> role
            sceneitems = SceneItem.objects.filter( scene=scene )
            for sceneitem in sceneitems:
                if sceneitem.role:
                    linked_gadgets = sceneitem.role.gadgets.all()
                    for item in linked_gadgets:
                        col = m.getColIndex(item)
                        if col:
                            m.cells[row][col].text = M_SYMBOL_LINKED   # MEDIUM WHITE CIRCLE

            # search for linked gadgets over scene -> story_time.gadgets
            linked_time = scene.story_location
            if linked_time:
                linked_gadgets = linked_time.gadgets.all()
                for item in linked_gadgets:
                    col = m.getColIndex(item)
                    if col:
                        m.cells[row][col].text = M_SYMBOL_LINKED

            # search for linked gadgets over scene -> story_location.gadgets
            linked_location = scene.story_location
            if linked_location:
                linked_gadgets = linked_location.gadgets.all()
                for item in linked_gadgets:
                    col = m.getColIndex(item)
                    if col:
                        m.cells[row][col].text = M_SYMBOL_LINKED

            # search for linked gadgets
            linked_gadgets = scene.gadgets.all()
            for item in linked_gadgets:
                col = m.getColIndex(item)
                if col:
                    m.cells[row][col].text = M_SYMBOL_LINKED   # MEDIUM BLACK CIRCLE

        return render(request, self.template_name, {
            'title': self.title,
            'env': env,
            'tag_list': tag_list,
            'M': m,
            'show_notes': form.cleaned_data['show_notes'],
        })

###############################################################################

class M_SceneSFXView(M_BaseView):
    form_class = SFXFilterForm
    x_group = 'sfx'
    initial = {'show_notes': True}
    title = 'Scene vs SFX Matrix'

    def render_list(self, request, form, tag_list):
        env = Env(request)
        query = getTagQuery(tag_list)
        sfxs = SFX.objects.filter( project=env.project_id ).filter(query).order_by(Lower('name'))
        scenes = Scene.objects.filter( project=env.project_id, script=env.script_id ).order_by('order')

        m = M(dfxs, scenes)

        for sfx in sfxs:
            col = m.getColIndex(sfx)
            #m.cells[0][col].background_color = dfx.color

        for scene in scenes:
            row = m.getRowIndex(scene)

            linked_sfxs = scene.sfxs.all()
            for item in linked_sfxs:
                col = m.getColIndex(item)
                if col:
                    m.cells[row][col].text = M_SYMBOL_LINKED

        return render(request, self.template_name, {
            'title': self.title,
            'env': env,
            'tag_list': tag_list,
            'M': m,
            'show_notes': form.cleaned_data['show_notes'],
        })

###############################################################################

class M_SceneAudioView(M_BaseView):
    form_class = AudioFilterForm
    x_group = 'audio'
    initial = {'show_notes': True}
    title = 'Scene vs Audio Matrix'

    def render_list(self, request, form, tag_list):
        env = Env(request)
        query = getTagQuery(tag_list)
        audios = Audio.objects.filter( project=env.project_id ).filter(query).order_by(Lower('name'))
        scenes = Scene.objects.filter( project=env.project_id, script=env.script_id ).order_by('order')

        m = M(audios, scenes)

        for audio in audios:
            col = m.getColIndex(audio)
            #m.cells[0][col].background_color = audio.color

        for scene in scenes:
            row = m.getRowIndex(scene)

            linked_audios = scene.audios.all()
            for item in linked_audios:
                col = m.getColIndex(item)
                if col:
                    m.cells[row][col].text = M_SYMBOL_LINKED

        return render(request, self.template_name, {
            'title': self.title,
            'env': env,
            'tag_list': tag_list,
            'M': m,
            'show_notes': form.cleaned_data['show_notes'],
        })

###############################################################################

class M_SceneTimeView(M_BaseView):
    form_class = TimeFilterForm
    x_group = 'time'
    initial = {'show_notes': True}
    title = 'Scene vs Time Matrix'

    def render_list(self, request, form, tag_list):
        env = Env(request)
        query = getTagQuery(tag_list)
        times = Time.objects.filter( project=env.project_id ).filter(query).order_by(Lower('name'))
        scenes = Scene.objects.filter( project=env.project_id, script=env.script_id ).order_by('order')

        m = M(times, scenes)

        for time in times:
            col = m.getColIndex(time)
            #m.cells[0][col].background_color = time.color

        for scene in scenes:
            row = m.getRowIndex(scene)

            linked_time = scene.story_time
            if linked_time:
                col = m.getColIndex(linked_time)
                if col:
                    m.cells[row][col].text = M_SYMBOL_LINKED

        return render(request, self.template_name, {
            'title': self.title,
            'env': env,
            'tag_list': tag_list,
            'M': m,
            'show_notes': form.cleaned_data['show_notes'],
        })

###############################################################################

class M_SceneLocationView(M_BaseView):
    form_class = LocationFilterForm
    x_group = 'location'
    initial = {'show_notes': True}
    title = 'Scene vs Location Matrix'

    def render_list(self, request, form, tag_list):
        env = Env(request)
        query = getTagQuery(tag_list)
        locations = Location.objects.filter( project=env.project_id ).filter(query).order_by(Lower('name'))
        scenes = Scene.objects.filter( project=env.project_id, script=env.script_id ).order_by('order')

        m = M(locations, scenes)

        for location in locations:
            col = m.getColIndex(location)
            #m.cells[0][col].background_color = location.color

        for scene in scenes:
            row = m.getRowIndex(scene)

            linked_location = scene.story_location
            if linked_location:
                col = m.getColIndex(linked_location)
                if col:
                    m.cells[row][col].text = M_SYMBOL_LINKED

        return render(request, self.template_name, {
            'title': self.title,
            'env': env,
            'tag_list': tag_list,
            'M': m,
            'show_notes': form.cleaned_data['show_notes'],
        })

###############################################################################

###############################################################################
