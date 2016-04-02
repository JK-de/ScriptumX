
import re, mmap
import html
from os import path
from datetime import datetime
import random

from .models import *
from X.common import *


class ImporterBase():
    class Meta:
        #abstract = True
        pass

    env = None
    sceneItem_counter = 1
    scene_counter = 1


###############################################################################

    def __init__(self, env, *args, **kwargs):
        super(ImporterBase, self).__init__(*args, **kwargs)

        self.env = env

###############################################################################

    def begin(self):
        pass

###############################################################################

    def finish(self):
        pass

###############################################################################

    def getRole(self, name):
        if name==None:
            name = '<unknown>'

        name = name[:50]
        try:
            role = Role.objects.get(name__iexact=name)
        except:
            role = Role()
            role.name = name
            role.project = self.env.project
            role.save()

        return role

###############################################################################

    def getLocation(self, name):
        if name==None:
            name = '<unknown>'
        
        name = name[:50]
        try:
            location = Location.objects.get(name__iexact=name)
        except:
            location = Location()
            location.name = name
            location.project = self.env.project
            location.save()

        return location

###############################################################################

    def addScene(self, name):
        if name==None:
            name = '<unknown>'

        name = name[:50]
        self.sceneItem_counter = 1

        scene = Scene()
        scene.setAllTags(True)
        scene.name = name
        scene.project = self.env.project
        scene.script = self.env.script
        scene.order = self.scene_counter
        self.scene_counter += 1
        scene.save()

        self.env.setScene(scene)
        return scene


    def getScene(self, name):
        return self.addScene(name)

###############################################################################

    def addScript(self, name, abstract=''):
        if name==None:
            name = '<unknown>'

        name = name[:50]
        script = Script()
        script.workingtitle = name
        script.abstract = abstract
        #script.description = markov.generate_markov_text(random.randint(20, 30))
        #script.author = markov.generate_markov_text(random.randint(2, 3))
        #script.copyright = markov.generate_markov_text(random.randint(2, 3))
        #script.version = '0.1-beta'
        script.project = self.env.project
        script.save()

        self.env.setScript(script)
        return script

    def getScript(self, name):
        if name==None:
            name = '<unknown>'

        name = name[:50]
        try:
            script = Script.objects.get(name=name)
        except:
            script = Script()
            script.workingtitle = 'Long Story - Short'
            script.abstract = markov.generate_markov_text(random.randint(2, 5))
            script.description = markov.generate_markov_text(random.randint(20, 30))
            script.author = markov.generate_markov_text(random.randint(2, 3))
            script.copyright = markov.generate_markov_text(random.randint(2, 3))
            script.version = '0.1-beta'
            script.project = self.env.project
            script.save()

        self.actScript = script
        return script

###############################################################################

    def addSceneItem(self, type, role_name, parenthetical, text):

        sceneItem = SceneItem()
        sceneItem.type = type
        if role_name:
            role_name = role_name[:50]
            sceneItem.role = self.getRole(role_name)
        else:
            sceneItem.role = None
        parenthetical = parenthetical[:100]
        sceneItem.parenthetical = parenthetical
        sceneItem.text = text
        sceneItem.scene = self.env.scene
        sceneItem.order = self.sceneItem_counter
        self.sceneItem_counter += 1
        sceneItem.save()

        return sceneItem

###############################################################################

    def getProject(self, name):
        if name==None:
            name = '<unknown>'

        role_name = role_name[:50]
        try:
            project = Project.objects.get(name=name)
        except:
            project = Project()
            project.name = name
            #project.users.add = user
            project.save()

        return project

###############################################################################

    def doImport(self, filename):

        actRole = None
        actParenthetical = ''

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



        with open(filename, 'rb') as f:

            #data = mmap.mmap(f.fileno(), 0)
            data_b = f.read()
            data = data_b.decode('cp1252', 'ignore')   # 'utf-8' 'ascii'

            if data[0] != 'P' or data[1] != 'K':
                pass

            self.addScript('IMPORT', 'import from celtx ' + filename + ' at ' + str(datetime.now()))

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

                if value=='':
                    continue

                value = re.sub(r'<span style="font-weight: bold;">(.*?)</span>', r'<b>\1</b>', value)   # replace bold token with shorter one
                value = re.sub(r'<span style="text-decoration: underline;">(.*?)</span>', r'<u>\1</u>', value)   # replace underline token with shorter one


                #value = html.unescape(value)
                try:
                    value = html_parser.unescape(value)
                except:
                    pass

                value = value.replace('´', "'")   # '&acute;' -> '´' -> UnicodeEncodeError : 'charmap' codec can't encode character '\xb4' in position 18: character maps to <undefined>


                if key=='action':
                    self.addSceneItem('A', None, '', value)
                    pass

                elif key=='character':
                    value = re.sub(r'\s+', r' ', value)
                    value = value.rstrip(':')
                    actRole = value
                    pass

                elif key=='parenthetical':
                    actParenthetical = value
                    pass

                elif key=='dialog':
                    self.addSceneItem('D', actRole, actParenthetical, value)
                    actParenthetical = ''
                    pass

                elif key=='shot':
                    pass

                elif key=='sceneheading':
                    self.addScene(value)
                    pass

                elif key=='transition':
                    pass


                #print(key + '|' + value + '|')


            f.close()

            pass

###############################################################################
###############################################################################
