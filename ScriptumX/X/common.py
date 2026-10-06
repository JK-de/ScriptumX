from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from X.models import Project, Script, Scene

###############################################################################

# Base tab definitions. Use get_tab_list(env) for hrefs that embed project/script.
_TAB_DEFS = (
    {'id': 'P', 'name': _('Project'), 'path': '/project', 'class': 'x-project', 'img': 'img/tab/project-24.png'},
    {'id': 'C', 'name': _('Script'), 'path': '/script', 'class': 'x-script', 'img': 'img/tab/script-24.png'},
    {'id': 'S', 'name': _('Scene'), 'path': '/scene', 'class': 'x-scene', 'img': 'img/tab/scene-24.png'},
    {'id': 'H', 'name': _('Shot'), 'path': '/shot', 'class': 'x-scene', 'img': 'img/tab/shot-24.png'},
    {'id': 'R', 'name': _('Role'), 'path': '/role', 'class': 'x-role', 'img': 'img/tab/role-24.png'},
    {'id': 'L', 'name': _('Location'), 'path': '/location', 'class': 'x-location', 'img': 'img/tab/location-24.png'},
    {'id': 'T', 'name': _('Time'), 'path': '/time', 'class': 'x-time', 'img': 'img/tab/time-24.png'},
    {'id': 'F', 'name': _('Person'), 'path': '/person', 'class': 'x-person', 'img': 'img/tab/person-24.png'},
    {'id': 'G', 'name': _('Gadget'), 'path': '/gadget', 'class': 'x-gadget', 'img': 'img/tab/gadget-24.png'},
    {'id': 'X', 'name': _('SFX'), 'path': '/sfx', 'class': 'x-sfx', 'img': 'img/tab/sfx-24.png'},
    {'id': 'A', 'name': _('Audio'), 'path': '/audio', 'class': 'x-audio', 'img': 'img/tab/audio-24.png'},
    {'id': 'B', 'name': _('Plan'), 'path': '/planner', 'class': 'x-planner', 'img': 'img/tab/scheduler-24.png'},
)


def get_tab_list(env=None):
    """Return navbar tabs; when env has project+script, editor tabs use /p/<pid>/s/<sid>/…"""
    tabs = []
    for tab in _TAB_DEFS:
        item = {
            'id': tab['id'],
            'name': tab['name'],
            'class': tab['class'],
            'img': tab['img'],
        }
        path = tab['path']
        if env and env.project_id:
            if tab['id'] == 'P':
                if env.script_id:
                    item['href'] = '/project/%s/%s' % (env.project_id, env.script_id)
                else:
                    item['href'] = '/project/%s' % env.project_id
            elif env.script_id:
                item['href'] = '/p/%s/s/%s%s' % (env.project_id, env.script_id, path)
            else:
                item['href'] = path
        else:
            item['href'] = path
        tabs.append(item)
    return tabs


# Backward-compatible static list (session-only hrefs). Prefer get_tab_list(env).
g_tab_list = get_tab_list(None)

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

g_tag_query_none = (
    Q(tag1=False) & Q(tag2=False) & Q(tag3=False) & Q(tag4=False)
    & Q(tag5=False) & Q(tag6=False) & Q(tag7=False) & Q(tag8=False)
    & Q(tag9=False) & Q(tag10=False) & Q(tag11=False) & Q(tag12=False)
)


def getTagQuery(tag_list):
    query = Q()
    for tag in tag_list:
        if tag['active']:
            if len(query) == 0:
                query = g_tag_queries[tag['idx']]
            else:
                query |= g_tag_queries[tag['idx']]

    if len(query) == len(tag_list):
        query = Q()
    elif len(query) == 0:
        query = g_tag_query_none

    return query

###############################################################################


def bind_scope_to_request(request, **kwargs):
    """Attach explicit URL scope so Env(request) picks up project/script without rewriting every call site."""
    if 'project_id' in kwargs and kwargs['project_id'] is not None:
        request.scriptum_project_id = kwargs['project_id']
    if 'script_id' in kwargs and kwargs['script_id'] is not None:
        request.scriptum_script_id = kwargs['script_id']
    if 'scene_id' in kwargs and kwargs['scene_id'] is not None:
        request.scriptum_scene_id = kwargs['scene_id']


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
    read_only = False

    def __init__(self, request, project_id=None, script_id=None, scene_id=None, *args, **kwargs):
        super(Env, self).__init__(*args, **kwargs)

        self.request = request
        self.read_only = False

        # Tokenized share links hydrate project/script without a login (F14).
        share = getattr(request, '_share_context', None)
        if share and share.get('project'):
            self.user = None
            self.project = share['project']
            self.project_id = self.project.id
            self.script = share.get('script')
            self.script_id = self.script.id if self.script else 0
            self.scene = None
            self.scene_id = 0
            self.user_level = 5  # read-only share guest
            self.read_only = True
            return

        # get user
        self.user = getattr(request, 'user', None)
        if self.user is not None and (not getattr(self.user, 'is_authenticated', False) or not self.user.is_active):
            self.user = None

        # Prefer explicit kwargs, then request attrs (from scoped URLs), then session.
        if project_id is None:
            project_id = getattr(request, 'scriptum_project_id', None)
        if script_id is None:
            script_id = getattr(request, 'scriptum_script_id', None)
        if scene_id is None:
            scene_id = getattr(request, 'scriptum_scene_id', None)

        # get project
        if project_id is not None:
            try:
                self.project_id = int(project_id)
            except (TypeError, ValueError):
                self.project_id = 0
        else:
            self.project_id = request.session.get('ProjectID', 0)

        try:
            self.project = Project.objects.get(pk=self.project_id)
        except Exception:
            self.project_id = 0
            self.project = None

        if not self.project:
            try:
                self.project = Project.objects.filter(
                    Q(owner=self.user) | Q(users=self.user) | Q(guests=self.user)
                ).last()
                self.setProject(self.project)
            except Exception:
                self.project_id = 0

        if not self.project:
            self.script = None
            self.scene = None
            self.user_level = 0
            return

        if self.project:
            if not self.user:
                self.user_level = 0
                self.project = None
            elif self.user.is_superuser:
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

        if not self.project:
            self.script = None
            self.scene = None
            self.user_level = 0
            return

        # Persist explicit URL project into session for multi-tab/legacy links
        if project_id is not None:
            self.setProject(self.project)

        # get script
        if script_id is not None:
            try:
                self.script_id = int(script_id)
            except (TypeError, ValueError):
                self.script_id = 0
        else:
            self.script_id = request.session.get('ScriptID', 0)

        try:
            self.script = Script.objects.get(pk=self.script_id, project=self.project)
        except Exception:
            self.script_id = 0
            self.script = None

        if not self.script:
            try:
                self.script = Script.objects.filter(project=self.project).last()
                self.setScript(self.script)
            except Exception:
                pass
        elif script_id is not None:
            self.setScript(self.script)

        # get scene
        if scene_id is not None:
            try:
                self.scene_id = int(scene_id)
            except (TypeError, ValueError):
                self.scene_id = 0
        else:
            self.scene_id = request.session.get('SceneID', 0)

        try:
            self.scene = Scene.objects.get(
                pk=self.scene_id, project=self.project, script=self.script
            )
        except Exception:
            self.scene_id = 0
            self.scene = None

        if not self.scene:
            try:
                self.scene = Scene.objects.filter(
                    project=self.project, script=self.script
                ).first()
                self.setScene(self.scene)
            except Exception:
                pass
        elif scene_id is not None:
            self.setScene(self.scene)

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


def getOrderNumber(list, ref_id, offset):
    """Return an order value for inserting/moving relative to ref_id.

    Empty lists get ORDER_STEP (first item). Missing ref returns None.
    """
    items = len(list)
    if items == 0:
        return ORDER_STEP

    ref_id = int(ref_id)
    refIndex = None
    for i in range(items):
        if list[i].id == ref_id:
            refIndex = i
            break

    # Must use `is None` — index 0 is a valid reference (first item).
    if refIndex is None:
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
            if (list[newIndex].order - list[newIndex - 1].order) < 2:
                reorderList(list)
            return int((list[newIndex].order - list[newIndex - 1].order) / 2) + list[newIndex - 1].order

    elif offset > 0:   # after...
        newIndex = refIndex + offset - 1
        if newIndex >= items - 1:
            newIndex = items - 1
            return list[newIndex].order + ORDER_STEP
        else:
            if (list[newIndex + 1].order - list[newIndex].order) < 2:
                reorderList(list)
            return int((list[newIndex + 1].order - list[newIndex].order) / 2) + list[newIndex].order

    else:
        return list[refIndex].order
