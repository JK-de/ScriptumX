from django.db.models import Q

from X.models import *

###############################################################################

g_tag_queries = [ 
    Q(note__isnull=False), 
    Q(tag1=True), 
    Q(tag2=True), 
    Q(tag3=True), 
    Q(tag4=True), 
    Q(tag5=True), 
    Q(tag6=True), 
    Q(tag7=True), 
    Q(tag8=True), 
    Q(tag9=True), 
    Q(tag10=True), 
    Q(tag11=True), 
    Q(tag12=True), 
    ]

g_tag_query_none = Q(tag1=False) & Q(tag2=False) & Q(tag3=False) & Q(tag4=False) & Q(tag5=False) & Q(tag6=False) & Q(tag7=False) & Q(tag8=False) & Q(tag9=False) & Q(tag10=False) & Q(tag11=False) & Q(tag12=False)

###############################################################################

class Env():
    request = None
    user = None
    project_id = 0
    project = None
    script_id = 0
    script = None
    scene_id = 0
    scene = None

    def __init__(self, request, *args, **kwargs):
        super(Env, self).__init__(*args, **kwargs)

        self.request = request

        self.project_id = request.session.get('ProjectID', 1)
        try:
            self.user = request.user
            #self.project = Project.objects.get(pk=self.project_id, users=self.user)
            self.project = Project.objects.get(pk=self.project_id)
        except:
            pass

        self.script_id = request.session.get('ScriptID', 0)
        try:
            if self.script_id==0:
                self.script = Script.objects.filter(project=self.project).last()
                self.script_id = self.script.id
            else:
                self.script = Script.objects.get(pk=self.script_id, project=self.project)
        except:
            pass

        self.scene_id = request.session.get('SceneID', 0)
        try:
            if self.scene_id==0:
                self.scene = Scene.objects.filter(project=self.project, script=self.script).first()
                self.scene_id = self.scene.id
            else:
                self.scene = Scene.objects.get(pk=self.scene_id, project=self.project, scene=self.script)
        except:
            pass

    def setScript(self, script):
        self.script = script
        if script:
            self.script_id = self.script.id
        else:
            self.script_id = 0
        self.request.session['ScriptID'] = self.script_id

    def setScene(self, scene):
        self.scene = scene
        if scene:
            self.scene_id = self.scene.id
        else:
            self.scene_id = 0
        self.request.session['SceneID'] = self.scene_id

###############################################################################
