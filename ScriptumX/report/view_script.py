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
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, ButtonHolder, Div, Field, HTML, Hidden
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.utils import render_crispy_form

from X.models import *
from X.views import g_tab_list
from X.views import Q
from X.common import *

from X.tags import FormSymbol, sceneitem_tag_list, handleTagRequest, getTagRequestList

###############################################################################

def collect_sceneheader(list, scene):
    item = { 'class':'sceneheading', 'text':scene.name, 'href':'/script/'+str(scene.id)}
    list.append(item)

###############################################################################

def collect_sceneitems(list, scene, sceneitems):
    
    for sceneitem in sceneitems:
        if sceneitem.type == 'A':
            item = { 'class':'action', 'text':sceneitem.text, 'href':'/scene/'+str(scene.id)+'/'+str(sceneitem.id)}
            list.append(item)
        
        if sceneitem.type == 'T':
            item = { 'class':'transition', 'text':sceneitem.text, 'href':'/scene/'+str(scene.id)+'/'+str(sceneitem.id)}
            list.append(item)

        if sceneitem.type == 'D':
            item = { 'class':'character', 'text':sceneitem.role.name}
            list.append(item)
            if sceneitem.parenthetical:
                item = { 'class':'parenthetical', 'text':sceneitem.parenthetical}
                list.append(item)
            if sceneitem.text:
                item = { 'class':'dialog', 'text':sceneitem.text, 'color':sceneitem.role.color, 'href':'/scene/'+str(sceneitem.id)}
                list.append(item)

        if sceneitem.type == 'R':
            item = { 'class':'character', 'text':sceneitem.role.name}
            list.append(item)
            if sceneitem.text:
                item = { 'class':'action', 'text':sceneitem.text, 'href':'/scene/'+str(scene.id)+'/'+str(sceneitem.id)}
                list.append(item)

        if sceneitem.type == 'N':
            pass


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

    scenes = Scene.objects.filter( project=env.project_id, script=env.script_id ).order_by('order')
    
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

