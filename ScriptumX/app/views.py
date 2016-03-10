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
from app.forms import NoteForm
from crispy_forms.utils import render_crispy_form
from .tags import gadget_tag_list, handleTagRequest, getTagRequestList
from django.db.models import Q
#from app.generator import get_sentences, get_paragraph
import random

import json
from app.views import Q

#http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/

###############################################################################

class Markov(object):
	
	def __init__(self, open_file):
		self.cache = {}
		self.open_file = open_file
		self.words = self.file_to_words()
		self.word_size = len(self.words)
		self.database()
		
	
	def file_to_words(self):
		self.open_file.seek(0)
		data = self.open_file.read()
		words = data.split()
		return words
		
	
	def triples(self):
		""" Generates triples from the given data string. So if our string were
				"What a lovely day", we'd generate (What, a, lovely) and then
				(a, lovely, day).
		"""
		
		if len(self.words) < 3:
			return
		
		for i in range(len(self.words) - 2):
			yield (self.words[i], self.words[i+1], self.words[i+2])
			
	def database(self):
		for w1, w2, w3 in self.triples():
			key = (w1, w2)
			if key in self.cache:
				self.cache[key].append(w3)
			else:
				self.cache[key] = [w3]
				
	def generate_markov_text(self, size=25):
		seed = random.randint(0, self.word_size-3)
		seed_word, next_word = self.words[seed], self.words[seed+1]
		w1, w2 = seed_word, next_word
		gen_words = []
		for i in range(size):
			gen_words.append(w1)
			w1, w2 = w2, random.choice(self.cache[(w1, w2)])
		gen_words.append(w2)
		return ' '.join(gen_words)
			
###############################################################################
###############################################################################
###############################################################################



def home(request):
    """Handles home page"""
    
    return render(request, 'app/home.html', {
        'title': 'Home',
        'datetime': datetime.now(),
    })

###############################################################################

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

###############################################################################

@login_required
def seed(request):
    """Seeds the database with samples."""
    #samples_path = path.join(path.dirname(__file__), 'samples.json')
    #with open(samples_path, 'r') as samples_file:
    #    samples_polls = json.load(samples_file)

    #for sample_poll in samples_polls:
    #    poll = Poll()
    #    poll.text = sample_poll['text']
    #    poll.pub_date = timezone.now()
    #    poll.save()

    #    for sample_choice in sample_poll['choices']:
    #        choice = Choice()
    #        choice.poll = poll
    #        choice.text = sample_choice
    #        choice.votes = 0
    #        choice.save()

    #file_ = open('app\loremipsum\default\sample.txt')
    file_ = open('jeeves.txt')

    markov = Markov(file_)

    text = markov.generate_markov_text(random.randint(2, 5))

    # generate Project
    try:
        project = Project.objects.get(pk=1)
    except:
        project = Project()
        project.name = 'Movie'
        #project.users.add = user
        project.save()

    # generate Script
    try:
        script = Script.objects.get(pk=1)
    except:
        script = Script()
        script.workingtitle = 'Long Story - Short'
        script.abstract = markov.generate_markov_text(random.randint(2, 5))
        script.description = markov.generate_markov_text(random.randint(20, 30))
        script.author = markov.generate_markov_text(random.randint(2, 3))
        script.copyright = markov.generate_markov_text(random.randint(2, 3))
        script.version = '0.1-beta'
        script.project = project
        project.users.add(request.user)
        script.save()

    # generate Gadgets
    for i in range(0, 30):
        gadget = Gadget()
        gadget.name = markov.generate_markov_text(random.randint(2, 5))
        gadget.description = markov.generate_markov_text(random.randint(5, 50))
        gadget.progress = i
        #gadget.note__text = "Hallo"
        tagRef = gadget.getTag(random.randint(0, 10))
        tagRef = True
        gadget.setTag(random.randint(1, 11), True)
        if random.randint(0, 5) == 0:
            n = Note()
            n.text = markov.generate_markov_text(random.randint(5, 50))
            n.save()
            gadget.note = n
        gadget.project = project
        gadget.save()

    
    # generate SceneItem with linked Scenes
    for s in range(0, 5):
        scene = Scene()
        scene.name = markov.generate_markov_text(random.randint(5, 7))
        scene.description = markov.generate_markov_text(random.randint(10, 30))
        scene.progress = i
        scene.script = script
        scene.save()

        for s in range(0, 15):
            item = SceneItem()
            item.text = markov.generate_markov_text(random.randint(5, 30))
            item.scene = scene
            item.save()


    

    #return HttpResponseRedirect(reverse('app:home'))
    return HttpResponseRedirect('/')

###############################################################################

#def get_or_none(classmodel, **kwargs):
#    try:
#        return classmodel.objects.get(**kwargs)
#    except classmodel.DoesNotExist:
#        return None

g_tab_list = (
    { 'id':'P', 'name':'Project',   'href':'/project',  'class':'x-project',  'img':'app/img/Tab/Project-24.png' },
    { 'id':'C', 'name':'Script',    'href':'/script',   'class':'x-script',   'img':'app/img/Tab/Script-24.png' },
    { 'id':'S', 'name':'Scene',     'href':'/scene',    'class':'x-scene',    'img':'app/img/Tab/Scene-24.png' },
    { 'id':'L', 'name':'Locations', 'href':'/set',      'class':'x-set',      'img':'app/img/Tab/Set-24.png' },
    { 'id':'R', 'name':'Roles',     'href':'/role',     'class':'x-role',     'img':'app/img/Tab/Role-24.png' },
    { 'id':'F', 'name':'Folks',     'href':'/folk',     'class':'x-folk',     'img':'app/img/Tab/Folk-24.png' },
    { 'id':'G', 'name':'Gadgets',   'href':'/gadget',   'class':'x-gadget',   'img':'app/img/Tab/Gadget-24.png' },
    { 'id':'X', 'name':'SFXs',      'href':'/sfx',      'class':'x-sfx',      'img':'app/img/Tab/SFX-24.png' },
    { 'id':'A', 'name':'Audios',    'href':'/audio',    'class':'x-audio',    'img':'app/img/Tab/Audio-24.png' },
    { 'id':'T', 'name':'Schedule',  'href':'/schedule', 'class':'x-schedule', 'img':'app/img/Tab/Schedule-24.png' },
    )



def dummy(request, id):
    """Handles ..."""
    
    return render(request, 'app/gadget.html', {
        'title': 'DUMMY',
        'tab_list': g_tab_list,
        'tab_active_id': 'P',
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
