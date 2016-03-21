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

from .tags import FormSymbol, sceneitem_tag_list, handleTagRequest, getTagRequestList

###############################################################################

class SceneForm(forms.ModelForm):
    """Edit form for SceneItem model"""
    class Meta:
        model = SceneItem
        fields = [
            'role',
            'parenthetical',
            'text',
            ]

    def __init__(self, *args, **kwargs):
        super(SceneForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Field('role'),

            Field('parenthetical', style="max-width:100%; min-width:100%;"),

            Field('text', style="max-width:100%; min-width:100%;", rows=10),
            )

    def clean_name(self):
      name = self.cleaned_data.get('name')
      return name

###############################################################################

def scene(request, sceneitem_id):
    """Handles page requests for SceneItems"""

    env = Env(request)


    tag_list = getTagRequestList(request, 'sceneitem')

    #sceneitems = get_list_or_404(SceneItem)
    
    try:
        active_sceneitem = SceneItem.objects.get(pk = sceneitem_id)
        active_id = active_sceneitem.id
        active_note = active_sceneitem.note
    except ObjectDoesNotExist:
        active_sceneitem = None
        active_id = None
        active_note = None

    ### create new sceneitem object on request '/scene/0'
    if sceneitem_id == '0':
        active_sceneitem = SceneItem(script=env.script, scene=env.scene);

    ### handle buttons
    if request.method == 'POST':
        if not active_sceneitem:   # you shall not pass ... without valid scope
            raise AssertionError 

        # generate forms and/or get data out of the edited forms
        formNote = NoteForm(request.POST or None, instance=active_note)
        if formNote.is_valid():
            active_note = formNote.instance
        formItem = SceneForm(request.POST or None, instance=active_sceneitem)
        if formItem.is_valid():
            active_sceneitem = formItem.instance

        # 'Delete'-Button
        if request.POST.get('btn_delete'):
            if active_note:
                if active_note.id:
                    active_note.delete()
            active_sceneitem.note = None
            active_sceneitem.delete()
            return HttpResponseRedirect('/scene/')

        # 'Add Note'-Button
        if request.POST.get('btn_note'):
            active_note = Note(project=env.project, author=env.user )
            active_sceneitem.note = active_note
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

            active_sceneitem.note = active_note

            if active_sceneitem:
                active_sceneitem.save()

            if sceneitem_id == '0':   # previously new item
                return HttpResponseRedirect('/scene/' + str(active_sceneitem.id))
    else:
        formItem = SceneForm(instance=active_sceneitem)
        formNote = NoteForm(instance=active_note)
    
    ### conglomerate queries
    #query = Q()
    #for tag in tag_list:
    #    if tag['active']:
    #        if len(query)==0:
    #            query = g_tag_queries[tag['idx']]
    #        else:
    #            query |= g_tag_queries[tag['idx']]

    #if len(query)==len(tag_list):
    #    query = Q()
    #elif len(query)==0:
    #    query = g_tag_query_none
    
    #filter(script=env.script, scene=env.scene)
    sceneitems = SceneItem.objects.all().order_by(Lower('order'))

    return render(request, 'X/scene.html', {
        'title': 'SceneItem',
        'env': env,
        'tab_list': g_tab_list,
        'tab_active_id': 'S',
        'tag_list': tag_list,
        'sceneitems': sceneitems,
        'active_sceneitem': active_sceneitem,
        'active_id': active_id,
        'form': formItem,
        'formNote': formNote,
        'datetime': datetime.now(),
        #'error_message': "Please make a selection.",
    })

###############################################################################

def sceneTag(request, tag_id):

    handleTagRequest(request, tag_id, 'sceneitem')

    return scene(request, None)

###############################################################################
