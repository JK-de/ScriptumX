"""
Definition of urls for polls viewing and voting.
"""

from django.conf.urls import patterns, url
from X.views import *
from X.view_project import *
from X.view_script import *
from X.view_scene import *
from X.view_roles import *
from X.view_persons import *
from X.view_locations import *
from X.view_gadgets import *
from X.view_audios import *
from X.view_sfxs import *
from X.view_scheduler import *
import X

urlpatterns = [

    url(r'^project/import$', X.view_project.project_import, name='projectImport'),
    url(r'^project/(?P<project_id>\d+)/(?P<script_id>\d+)?$', X.view_project.project, name='project'),
    url(r'^project/(?P<project_id>\d+)?$', X.view_project.project, name='project'),

    url(r'^script/new/(?P<scene_id>\d+)/(?P<offset>[-]?\d+)$', X.view_script.scriptNew, name='scriptNew'),
    url(r'^script/move/(?P<scene_id>\d+)/(?P<offset>[-]?\d+)$', X.view_script.scriptMove, name='scriptMove'),
    url(r'^script/(?P<scene_id>[0])/(?P<new_order>\d+)$', X.view_script.script, name='script'),
    url(r'^script/(?P<scene_id>\d+)?$', X.view_script.script, name='script'),
    url(r'^script/tag/(?P<tag_id>\w+)$', X.view_script.scriptTag, name='scriptTag'),

    url(r'^scene/new/(?P<sceneitem_type>[NADTR])/(?P<sceneitem_id>\d+)/(?P<offset>[-]?\d+)$', X.view_scene.sceneNew, name='sceneNew'),
    url(r'^scene/move/(?P<sceneitem_id>\d+)/(?P<offset>[-]?\d+)$', X.view_scene.sceneMove, name='sceneMove'),
    url(r'^scene/(?P<sceneitem_id>[0])/(?P<new_type>[NADTR])/(?P<new_order>\d+)$', X.view_scene.scene, name='scene'),
    url(r'^scene/(?P<sceneitem_id>\d+)?$', X.view_scene.scene, name='scene'),
    url(r'^scene/tag/(?P<tag_id>\w+)$', X.view_scene.sceneTag, name='sceneTag'),
    url(r'^scene/set/(?P<scene_id>\w+)$', X.view_scene.sceneSet, name='sceneSet'),

    url(r'^role/(?P<role_id>\d+)?$', X.view_roles.role, name='role'),
    url(r'^role/tag/(?P<tag_id>\w+)?$', X.view_roles.roleTag, name='roleTag'),

    url(r'^person/(?P<person_id>\d+)?$', X.view_persons.person, name='person'),
    url(r'^person/tag/(?P<tag_id>\w+)?$', X.view_persons.personTag, name='personTag'),

    url(r'^location/(?P<location_id>\d+)?$', X.view_locations.location, name='location'),
    url(r'^location/tag/(?P<tag_id>\w+)?$', X.view_locations.locationTag, name='locationTag'),

    url(r'^gadget/(?P<gadget_id>\d+)?$', X.view_gadgets.gadget, name='gadget'),
    url(r'^gadget/tag/(?P<tag_id>\w+)?$', X.view_gadgets.gadgetTag, name='gadgetTag'),

    url(r'^audio/(?P<audio_id>\d+)?$', X.view_audios.audio, name='audio'),
    url(r'^audio/tag/(?P<tag_id>\w+)?$', X.view_audios.audioTag, name='audioTag'),

    url(r'^sfx/(?P<sfx_id>\d+)?$', X.view_sfxs.sfx, name='sfx'),
    url(r'^sfx/tag/(?P<tag_id>\w+)?$', X.view_sfxs.sfxTag, name='sfxTag'),

    url(r'^scheduler/(?P<appointment_id>\d+)?$', X.view_scheduler.scheduler, name='scheduler'),
    url(r'^scheduler/tag/(?P<tag_id>\w+)?$', X.view_scheduler.schedulerTag, name='schedulerTag'),

    #url(r'^project/(?P<id>\d+)?$', X.views.dummy, name='dummy'),
    #url(r'^schedule/(?P<id>\d+)?$', X.views.dummy, name='dummy'),
    ]
