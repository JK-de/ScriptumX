from .models import *


class ImporterBase():
    class Meta:
        #abstract = True
        pass

    actUser = None
    actProject = None
    actScript = None
    actScene = None
    actSceneItem = None


###############################################################################

    def __init__(self, user, project, *args, **kwargs):
        super(ImporterBase, self).__init__(*args, **kwargs)

        actProject = project

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

        try:
            script = Role.objects.get(name=name)
        except:
            role = Role()
            role.name = name
            role.project = actProject
            role.save()

        return role

###############################################################################

    def getLocation(self, name):
        if name==None:
            name = '<unknown>'

        try:
            location = Location.objects.get(name=name)
        except:
            location = Location()
            location.name = name
            location.project = actProject
            location.save()

        return location

###############################################################################

    def getScene(self, name):
        if name==None:
            name = '<unknown>'

        scene = Scene()
        scene.name = name
        scene.project = actProject
        scene.save()

        actScene = scene
        return scene

###############################################################################

    def getScript(self, name):
        if name==None:
            name = '<unknown>'

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
            script.project = actProject
            project.users.add(actUser)
            script.save()

        actScript = script
        return script

###############################################################################

    def getProject(self, name):
        if name==None:
            name = '<unknown>'

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
        pass

###############################################################################
###############################################################################
