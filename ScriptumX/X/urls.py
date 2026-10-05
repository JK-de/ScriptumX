"""
X app URL routes.
"""
from django.urls import re_path

from X import view_project
from X import view_script
from X import view_scene
from X import view_shot
from X import view_roles
from X import view_persons
from X import view_times
from X import view_locations
from X import view_gadgets
from X import view_audios
from X import view_sfxs
from X import view_scheduler

app_name = 'X'

urlpatterns = [
    re_path(r'^project/import$', view_project.project_import, name='projectImport'),
    re_path(r'^project/(?P<project_id>\d+)/(?P<script_id>\d+)?$', view_project.project, name='project'),
    re_path(r'^project/(?P<project_id>\d+)?$', view_project.project, name='project'),

    re_path(r'^script/new/(?P<scene_id>\d+)/(?P<offset>[-]?\d+)$', view_script.scriptNew, name='scriptNew'),
    re_path(r'^script/move/(?P<scene_id>\d+)/(?P<offset>[-]?\d+)$', view_script.scriptMove, name='scriptMove'),
    re_path(r'^script/(?P<scene_id>[0])/(?P<new_order>\d+)$', view_script.script, name='script'),
    re_path(r'^script/(?P<scene_id>\d+)?$', view_script.script, name='script'),
    re_path(r'^script/tag/(?P<tag_id>\w+)$', view_script.scriptTag, name='scriptTag'),

    re_path(r'^scene/new/(?P<sceneitem_type>[NADTR])/(?P<sceneitem_id>\d+)/(?P<offset>[-]?\d+)$', view_scene.sceneNew, name='sceneNew'),
    re_path(r'^scene/move/(?P<sceneitem_id>\d+)/(?P<offset>[-]?\d+)$', view_scene.sceneMove, name='sceneMove'),
    re_path(r'^scene/(?P<sceneitem_id>[0])/(?P<new_type>[NADTR])/(?P<new_order>\d+)$', view_scene.scene, name='scene'),
    re_path(r'^scene/(?P<sceneitem_id>\d+)?$', view_scene.scene, name='scene'),
    re_path(r'^scene/tag/(?P<tag_id>\w+)$', view_scene.sceneTag, name='sceneTag'),
    re_path(r'^scene/set/(?P<scene_id>\w+)$', view_scene.sceneSet, name='sceneSet'),

    re_path(r'^shot/(?P<sceneitem_id>\d+)?$', view_shot.shot, name='shot'),
    re_path(r'^shot/set/(?P<scene_id>\w+)$', view_shot.shotSet, name='shotSet'),

    re_path(r'^role/(?P<role_id>\d+)?$', view_roles.role, name='role'),
    re_path(r'^role/tag/(?P<tag_id>\w+)?$', view_roles.roleTag, name='roleTag'),

    re_path(r'^person/(?P<person_id>\d+)?$', view_persons.person, name='person'),
    re_path(r'^person/tag/(?P<tag_id>\w+)?$', view_persons.personTag, name='personTag'),

    re_path(r'^time/(?P<time_id>\d+)?$', view_times.time, name='time'),
    re_path(r'^time/tag/(?P<tag_id>\w+)?$', view_times.timeTag, name='timeTag'),

    re_path(r'^location/(?P<location_id>\d+)?$', view_locations.location, name='location'),
    re_path(r'^location/tag/(?P<tag_id>\w+)?$', view_locations.locationTag, name='locationTag'),

    re_path(r'^gadget/(?P<gadget_id>\d+)?$', view_gadgets.gadget, name='gadget'),
    re_path(r'^gadget/tag/(?P<tag_id>\w+)?$', view_gadgets.gadgetTag, name='gadgetTag'),

    re_path(r'^audio/(?P<audio_id>\d+)?$', view_audios.audio, name='audio'),
    re_path(r'^audio/tag/(?P<tag_id>\w+)?$', view_audios.audioTag, name='audioTag'),

    re_path(r'^sfx/(?P<sfx_id>\d+)?$', view_sfxs.sfx, name='sfx'),
    re_path(r'^sfx/tag/(?P<tag_id>\w+)?$', view_sfxs.sfxTag, name='sfxTag'),

    re_path(r'^scheduler/(?P<appointment_id>\d+)?$', view_scheduler.scheduler, name='scheduler'),
    re_path(r'^scheduler/tag/(?P<tag_id>\w+)?$', view_scheduler.schedulerTag, name='schedulerTag'),
]
