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

        # get user
        self.user = request.user

        # get project
        self.project_id = request.session.get('ProjectID', 1)
        try:
            self.project = Project.objects.get(pk=self.project_id, users=self.user)
            #self.project = Project.objects.get(pk=self.project_id)
        except:
            self.project_id = 0
            pass

        # get script
        self.script_id = request.session.get('ScriptID', 0)
        try:
            self.script = Script.objects.get(pk=self.script_id, project=self.project)
        except:
            self.script_id = 0

        if self.script_id == 0:
            try:
                self.script = Script.objects.filter(project=self.project).last()
                self.script_id = self.script.id
            except:
                pass

        # get scene
        self.scene_id = request.session.get('SceneID', 0)
        try:
            self.scene = Scene.objects.get(pk=self.scene_id, project=self.project, script=self.script)
        except:
            self.scene_id = 0

        if self.scene_id == 0:
            try:
                self.scene = Scene.objects.filter(project=self.project, script=self.script).first()
                self.scene_id = self.scene.id
            except:
                pass



    def setProject(self, project):
        self.project = project
        if project:
            self.project_id = self.project.id
        else:
            self.project_id = 0
        self.request.session['ProjectID'] = self.project_id

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

ORDER_STEP = 65536

def reorderList(list):
    
    newOrder = ORDER_STEP

    for item in list:
        oldIndex = item.order
        if oldIndex != newOrder:
            item.order = newOrder
            item.save()
        newOrder += ORDER_STEP


def getOrderNumber(list,ref_id,offset):
    
    ref_id = int(ref_id)
    refIndex = None
    items = len(list)
    for i in range(items):
        if list[i].id == ref_id:
            refIndex = i
            break

    if not refIndex:
        return None

    offset = int(offset)
    if offset < 0:   # befor...
        newIndex = refIndex + offset + 1
        if newIndex <= 0:
            newIndex = 0
            if list[newIndex].order < 2:
                reorderList(list)
            return int(list[newIndex].order / 2)
        else:
            if (list[newIndex].order - list[newIndex-1].order) < 2:
                reorderList(list)
            return int((list[newIndex].order - list[newIndex-1].order) / 2) + list[newIndex-1].order
            
    elif offset > 0:   # after...
        newIndex = refIndex + offset - 1
        if newIndex >= items-1:
            newIndex = items-1
            return list[newIndex].order + ORDER_STEP
        else:
            if (list[newIndex+1].order - list[newIndex].order) < 2:
                reorderList(list)
            return int((list[newIndex+1].order - list[newIndex].order) / 2) + list[newIndex].order
            
    else:
        return list[refIndex].order



        
    

###############################################################################

