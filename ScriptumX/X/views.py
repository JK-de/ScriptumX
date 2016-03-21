"""
Definition of views.
"""

from X.models import *
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
from X.forms import NoteForm
from crispy_forms.utils import render_crispy_form
from .tags import gadget_tag_list, handleTagRequest, getTagRequestList
from django.db.models import Q
#from X.generator import get_sentences, get_paragraph
import random

import json
from X.views import Q

#http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/


from X.common import *

from .importer import ImporterBase


def test(request):

    env = Env(request)

    html_parser = html.parser.HTMLParser()

    pattern = re.compile(r'''
        <p                      # begin of paragraph block - opening pattern
        .*?                     # any other token
        class="(?P<key>.*?)"    # Header name
        .*?                     # any other token
        >                       # begin of paragraph block - closing pattern
        (?P<value>.*?)          # content
        </p>                    # end of paragraph block
        ''', re.VERBOSE | re.MULTILINE | re.DOTALL)

    pattern_ws = r'&nbsp;|<br>|\n|:$'

    keys = {}


    with open('/tmp/test.celtx', 'rb') as f:

        #data = mmap.mmap(f.fileno(), 0)
        data_b = f.read()
        data = data_b.decode('cp1252', 'ignore')   # 'utf-8' 'ascii'

        for match in re.finditer(pattern, data):
            #print(match)

            #key = match.group(1)
            #value = match.group(2)
            key = match.group('key')
            value_raw = match.group('value')

            value = re.sub(pattern_ws, r' ', value_raw)
            value = value.strip()
            #if s.endswith(" "): s = s[:-1]
            #if s.startswith(" "): s = s[1:]

            value = re.sub(r'<span style="font-weight: bold;">(.*?)</span>', r'<b>\1</b>', value)   # replace bold token with shorter one


            #value = html.unescape(value)
            try:
                value = html_parser.unescape(value)
            except:
                pass

            value = value.replace('´', "'")   # '&acute;' -> '´' -> UnicodeEncodeError : 'charmap' codec can't encode character '\xb4' in position 18: character maps to <undefined>


            if key=='action':
                pass

            elif key=='character':
                value = re.sub(r'\s+', r' ', value)
                value = value.rstrip(':')
                pass

            elif key=='parenthetical':
                pass

            elif key=='dialog':
                pass

            elif key=='shot':
                pass
            elif key=='sceneheading':
                pass

            elif key=='transition':
                pass


            print(key + '|' + value + '|')

            keys[key] = value

        print(keys)
        f.close()



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
    
    #env = Env(request)

    #imp = ImporterBase(env)
    #imp.doImport('/tmp/test.celtx')
   

    return render(request, 'X/home.html', {
        'title': 'Home',
        'datetime': datetime.now(),
    })

###############################################################################

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'X/contact.html',
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
        'X/about.html',
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
        project.owner = request.user
        project.save()
        project.users.add(request.user)
        project.save()

    # generate Script
    try:
        script = Script.objects.get(pk=1)
    except:
        script = Script()
        script.project = project
        script.workingtitle = 'Long Story - Short'
        script.abstract = markov.generate_markov_text(random.randint(2, 5))
        script.description = markov.generate_markov_text(random.randint(20, 30))
        script.author = markov.generate_markov_text(random.randint(2, 3))
        script.copyright = markov.generate_markov_text(random.randint(2, 3))
        script.version = '0.1-beta'
        script.save()

    # generate Gadgets
    for i in range(0, 30):
        gadget = Gadget()
        gadget.project = project
        gadget.name = markov.generate_markov_text(random.randint(2, 5))
        gadget.description = markov.generate_markov_text(random.randint(5, 50))
        gadget.progress = i
        #gadget.note__text = "Hallo"
        tagRef = gadget.getTag(random.randint(0, 10))
        tagRef = True
        gadget.setTag(random.randint(1, 11), True)
        if random.randint(0, 5) == 0:
            n = Note(project=project)
            n.text = markov.generate_markov_text(random.randint(5, 50))
            n.save()
            gadget.note = n
        gadget.save()

    
    # generate SceneItem with linked Scenes
    for s in range(0, 25):
        scene = Scene()
        scene.project = project
        scene.script = script
        scene.name = markov.generate_markov_text(random.randint(5, 7))
        scene.short = str(s)
        scene.abstract = markov.generate_markov_text(random.randint(10, 30))
        scene.description = markov.generate_markov_text(random.randint(30, 50))
        if random.randint(0, 5) == 0:
            scene.progress_script = random.randint(0, 100)
        if random.randint(0, 5) == 0:
            scene.progress_pre = random.randint(0, 100)
        if random.randint(0, 5) == 0:
            scene.progress_shot = random.randint(0, 100)
        if random.randint(0, 5) == 0:
            scene.progress_post = random.randint(0, 100)
        if random.randint(0, 5) == 0:
            scene.indentation = random.randint(0, 5)*10
        scene.setTag(random.randint(1, 11), False)
        if random.randint(0, 5) == 0:
            n = Note(project=project)
            n.text = markov.generate_markov_text(random.randint(5, 50))
            n.save()
            scene.note = n
        scene.save()

        for s in range(0, 25):
            item = SceneItem()
            item.text = markov.generate_markov_text(random.randint(5, 30))
            item.scene = scene
            if random.randint(0, 5) == 0:
                n = Note(project=project)
                n.text = markov.generate_markov_text(random.randint(5, 50))
                n.save()
                item.note = n
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
    { 'id':'P', 'name':'Project',   'href':'/project',  'class':'x-project',  'img':'img/tab/project-24.png' },
    { 'id':'C', 'name':'Script',    'href':'/script',   'class':'x-script',   'img':'img/tab/script-24.png' },
    { 'id':'S', 'name':'Scene',     'href':'/scene',    'class':'x-scene',    'img':'img/tab/scene-24.png' },
    { 'id':'R', 'name':'Roles',     'href':'/role',     'class':'x-role',     'img':'img/tab/role-24.png' },
    { 'id':'F', 'name':'Persons',   'href':'/person',   'class':'x-person',   'img':'img/tab/person-24.png' },
    { 'id':'L', 'name':'Locations', 'href':'/location', 'class':'x-location', 'img':'img/tab/location-24.png' },
    { 'id':'G', 'name':'Gadgets',   'href':'/gadget',   'class':'x-gadget',   'img':'img/tab/gadget-24.png' },
    { 'id':'X', 'name':'SFXs',      'href':'/sfx',      'class':'x-sfx',      'img':'img/tab/sfx-24.png' },
    { 'id':'A', 'name':'Audios',    'href':'/audio',    'class':'x-audio',    'img':'img/tab/audio-24.png' },
    { 'id':'T', 'name':'Scheduler', 'href':'/scheduler','class':'x-scheduler','img':'img/tab/scheduler-24.png' },
    )



def dummy(request, id):
    """Handles ..."""
    
    return render(request, 'X/gadget.html', {
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
