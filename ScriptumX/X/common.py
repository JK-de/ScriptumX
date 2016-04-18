from django.db.models import Q

from X.models import *

###############################################################################

g_tab_list = (
    { 'id':'P', 'name':'Project',   'href':'/project',  'class':'x-project',  'img':'img/tab/project-24.png' },
    { 'id':'C', 'name':'Script',    'href':'/script',   'class':'x-script',   'img':'img/tab/script-24.png' },
    { 'id':'S', 'name':'Scene',     'href':'/scene',    'class':'x-scene',    'img':'img/tab/scene-24.png' },
    { 'id':'L', 'name':'Location',  'href':'/location', 'class':'x-location', 'img':'img/tab/location-24.png' },
    { 'id':'T', 'name':'Time',      'href':'/location', 'class':'x-time',     'img':'img/tab/time-24.png' },
    { 'id':'R', 'name':'Role',      'href':'/role',     'class':'x-role',     'img':'img/tab/role-24.png' },
    { 'id':'F', 'name':'Person',    'href':'/person',   'class':'x-person',   'img':'img/tab/person-24.png' },
    { 'id':'G', 'name':'Gadget',    'href':'/gadget',   'class':'x-gadget',   'img':'img/tab/gadget-24.png' },
    { 'id':'X', 'name':'SFX',       'href':'/sfx',      'class':'x-sfx',      'img':'img/tab/sfx-24.png' },
    { 'id':'A', 'name':'Audio',     'href':'/audio',    'class':'x-audio',    'img':'img/tab/audio-24.png' },
    { 'id':'T', 'name':'', 'href':'/scheduler','class':'x-scheduler','img':'img/tab/scheduler-24.png' },
    )

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

def getTagQuery(tag_list):
    query = Q()
    for tag in tag_list:
        if tag['active']:
            if len(query)==0:
                query = g_tag_queries[tag['idx']]
            else:
                query |= g_tag_queries[tag['idx']]

    if len(query)==len(tag_list):
        query = Q()
    elif len(query)==0:
        query = g_tag_query_none
    
    return query

###############################################################################

class Env():
    request = None
    user = None
    user_level = 0
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
        if not self.user.is_active:
            self.user = None

        # get project
        self.project_id = request.session.get('ProjectID', 0)
        #test self.project_id = 123
        try:
            self.project = Project.objects.get(pk=self.project_id)
        except:
            self.project_id = 0

        if not self.project:
            try:
                self.project = Project.objects.filter( Q(owner=self.user) | Q(users=self.user) | Q(guests=self.user) ).last()
                #self.project_id = self.project.id
                self.setProject(self.project)
            except:
                self.project_id = 0

        if not self.project:
            self.script = None
            self.scene = None
            self.user_level = 0
            return

        if self.project:
            if self.user.is_superuser:
                self.user_level = 42
            elif self.user.is_staff:
                self.user_level = 40
            elif self.project.owner == self.user:
                self.user_level = 30
            elif self.project.users.filter(pk=self.user.id):
                self.user_level = 20
            elif self.project.guests.filter(pk=self.user.id):
                self.user_level = 10
            else:
                self.user_level = 0
                self.project = None

        # get script
        self.script_id = request.session.get('ScriptID', 0)
        try:
            self.script = Script.objects.get(pk=self.script_id, project=self.project)
        except:
            self.script_id = 0

        if not self.script:
            try:
                self.script = Script.objects.filter(project=self.project).last()
                #self.script_id = self.script.id
                self.setScript(self.script)
            except:
                pass

        # get scene
        self.scene_id = request.session.get('SceneID', 0)
        try:
            self.scene = Scene.objects.get(pk=self.scene_id, project=self.project, script=self.script)
        except:
            self.scene_id = 0

        if not self.scene:
            try:
                self.scene = Scene.objects.filter(project=self.project, script=self.script).first()
                #self.scene_id = self.scene.id
                self.setScene(self.scene)
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

