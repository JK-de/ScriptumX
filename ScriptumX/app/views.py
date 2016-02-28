"""
Definition of views.
"""

from app.models import *
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.template import RequestContext
from django.utils import timezone
from django.views.generic import ListView, DetailView
from os import path
from django.core.exceptions import ObjectDoesNotExist
from app.forms import GadgetForm
from crispy_forms.utils import render_crispy_form

import json

def home(request):
    """Handles home page"""
    
    return render(request, 'app/home.html', {
        'title': 'Home',
        'datetime': datetime.now(),
    })


class PollListView(ListView):
    """Renders the home page, with a list of all polls."""
    model = Poll

    def get_context_data(self, **kwargs):
        context = super(PollListView, self).get_context_data(**kwargs)
        context['title'] = 'Polls'
        context['year'] = datetime.now().year
        return context

class PollDetailView(DetailView):
    """Renders the poll details page."""
    model = Poll

    def get_context_data(self, **kwargs):
        context = super(PollDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Poll'
        context['year'] = datetime.now().year
        return context

class PollResultsView(DetailView):
    """Renders the results page."""
    model = Poll

    def get_context_data(self, **kwargs):
        context = super(PollResultsView, self).get_context_data(**kwargs)
        context['title'] = 'Results'
        context['year'] = datetime.now().year
        return context

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        })
    )

def vote(request, poll_id):
    """Handles voting. Validates input and updates the repository."""
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'app/details.html', {
            'title': 'Poll',
            'year': datetime.now().year,
            'poll': poll,
            'error_message': "Please make a selection.",
    })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('app:results', args=(poll.id,)))

import random
import string
def random_text(letters=32):
    return ''.join([random.choice(string.ascii_letters + string.digits + "     ") for n in range(letters)])


@login_required
def seed(request):
    """Seeds the database with sample polls."""
    samples_path = path.join(path.dirname(__file__), 'samples.json')
    with open(samples_path, 'r') as samples_file:
        samples_polls = json.load(samples_file)

    for sample_poll in samples_polls:
        poll = Poll()
        poll.text = sample_poll['text']
        poll.pub_date = timezone.now()
        poll.save()

        for sample_choice in sample_poll['choices']:
            choice = Choice()
            choice.poll = poll
            choice.text = sample_choice
            choice.votes = 0
            choice.save()

    # generate Gadgets
    for i in range(0, 10):
        gadget = Gadget()
        gadget.name = "Gadget-" + str(i)
        gadget.description = random_text()
        gadget.progress = i
        gadget.save()

    
    # generate SceneItem with linked Scenes
    for s in range(0, 5):
        scene = Scene()
        scene.name = "Scene-" + str(s)
        gadget.description = random_text()
        gadget.progress = i
        scene.save()

        for s in range(0, 5):
            item = SceneItem()
            item.text = random_text(300)
            item.scene = scene
            item.save()

    

    return HttpResponseRedirect(reverse('app:home'))



#def get_or_none(classmodel, **kwargs):
#    try:
#        return classmodel.objects.get(**kwargs)
#    except classmodel.DoesNotExist:
#        return None
tab_list1 = (
    ( 'P', 'Project', '/gadget', 'app/img/Tab/Project-16.png' ),
    ( 'G', 'Gadget',  '/gadget', 'app/img/Tab/Gadget-16.png' ),
    )

tab_list2 = (
    { 'active':'P', 'name':'Project',  'href':'/project',  'img':'app/img/Tab/Project-16.png' },
    { 'active':'C', 'name':'Script',   'href':'/script',   'img':'app/img/Tab/Script-16.png' },
    { 'active':'S', 'name':'Scene',    'href':'/scene',    'img':'app/img/Tab/Scene-16.png' },
    { 'active':'L', 'name':'Set',      'href':'/set',      'img':'app/img/Tab/Set-16.png' },
    { 'active':'R', 'name':'Role',     'href':'/role',     'img':'app/img/Tab/Role-16.png' },
    { 'active':'F', 'name':'Folk',     'href':'/folk',     'img':'app/img/Tab/Folk-16.png' },
    { 'active':'G', 'name':'Gadget',   'href':'/gadget',   'img':'app/img/Tab/Gadget-16.png' },
    { 'active':'X', 'name':'SFX',      'href':'/sfx',      'img':'app/img/Tab/SFX-16.png' },
    { 'active':'A', 'name':'Audio',    'href':'/audio',    'img':'app/img/Tab/Audio-16.png' },
    { 'active':'T', 'name':'Schedule', 'href':'/schedule', 'img':'app/img/Tab/Schedule-16.png' },
    )

gadget_tag_list = (
    { 'bit': 0, 'name':'Requisite', 'img':'app/img/G/tag/Requisite.png' },
    { 'bit': 1, 'name':'Costume',   'img':'app/img/G/tag/Costume.png' },
    { 'bit': 2, 'name':'MakeUp',    'img':'app/img/G/tag/MakeUp.png' },
    { 'bit': 3, 'name':'Camera',    'img':'app/img/G/tag/Camera.png' },
    { 'bit': 4, 'name':'Gaffer',    'img':'app/img/G/tag/Gaffer.png' },
    { 'bit': 5, 'name':'Grip',      'img':'app/img/G/tag/Grip.png' },
    { 'bit': 6, 'name':'Audio',     'img':'app/img/G/tag/Audio.png' },
    { 'bit': 7, 'name':'Special',   'img':'app/img/G/tag/Special.png' },
    { 'bit': 8, 'name':'Tool',      'img':'app/img/G/tag/Tool.png' },
    { 'bit': 9, 'name':'Phyro',     'img':'app/img/G/tag/Phyro.png' },
    { 'bit':10, 'name':'Catering',  'img':'app/img/G/tag/Catering.png' },
    )

def gadget(request, gadget_id):
    """Handles ..."""
    
    gadgets = get_list_or_404(Gadget)
    
    try:
        active_gadget = Gadget.objects.get(pk = gadget_id)
        active_id = active_gadget.id
    except ObjectDoesNotExist:
        active_gadget = None
        active_id = None

    #if request.method == 'POST':
    #    print request.POST

    if request.method == 'POST':
        form = GadgetForm(request.POST or None, instance=active_gadget)

        if form.is_valid():
            instance = form.save()
    else:
        form = GadgetForm(instance=active_gadget)

    return render(request, 'app/gadget.html', {
        'title': 'Gadget',
        'form': form,
        'tab_active': 'G',
        'tab_list': tab_list1,
        'tab_list2': tab_list2,
        'tag_list': gadget_tag_list,
        'datetime': datetime.now(),
        'gadgets': gadgets,
        'active_gadget': active_gadget,
        'active_id': active_id,
        #'error_message': "Please make a selection.",
    })

def dummy(request, id):
    """Handles ..."""
    
    return render(request, 'app/gadget.html', {
        'title': 'DUMMY',
        'tab_active': 'P',
        'tab_list': tab_list1,
        'tab_list2': tab_list2,
        'datetime': datetime.now(),
    })



#To make things easier, here is a snippet of the code I wrote, based on inputs from the wonderful replies here:

#class MyManager(models.Manager):

#    def get_or_none(self, **kwargs):
#        try:
#            return self.get(**kwargs)
#        except ObjectDoesNotExist:
#            return None

#And then in your model:

#class MyModel(models.Model):
#    objects = MyManager()

#That's it. Now you have MyModel.objects.get() as well as MyModel.objetcs.get_or_none()
#shareimprove this answer
	
#answered Jul 22 '14 at 13:05
#Moti Radomski
#656
	
#1
	
#also, don't forget to import: from django.core.exceptions import ObjectDoesNotExist – Moti Radomski Jul 22 '14 at 13:07 
