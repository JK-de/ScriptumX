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
from X import data_safety
from X import view_planner

app_name = 'X'

# Explicit project/script deep-link prefix (H17). Legacy session-only routes remain below.
_SCOPE = r'^p/(?P<project_id>\d+)/s/(?P<script_id>\d+)/'

urlpatterns = [
    re_path(r'^project/import$', view_project.project_import, name='projectImport'),
    re_path(r'^project/restore$', view_project.project_restore, name='projectRestore'),
    re_path(r'^project/(?P<project_id>\d+)/export(?:\.(?P<fmt>json|zip))?$', view_project.project_export, name='projectExport'),
    re_path(r'^project/(?P<project_id>\d+)/(?P<script_id>\d+)?$', view_project.project, name='project'),
    re_path(r'^project/(?P<project_id>\d+)?$', view_project.project, name='project'),

    re_path(r'^script/new/(?P<scene_id>\d+)/(?P<offset>[-]?\d+)$', view_script.scriptNew, name='scriptNew'),
    re_path(r'^script/move/(?P<scene_id>\d+)/(?P<offset>[-]?\d+)$', view_script.scriptMove, name='scriptMove'),
    re_path(r'^script/undo-move$', view_script.scriptUndoMove, name='scriptUndoMove'),
    re_path(r'^script/autosave/(?P<scene_id>\d+)$', data_safety.script_autosave, name='scriptAutosave'),
    re_path(r'^script/(?P<scene_id>[0])/(?P<new_order>\d+)$', view_script.script, name='script'),
    re_path(r'^script/(?P<scene_id>\d+)?$', view_script.script, name='script'),
    re_path(r'^script/tag/(?P<tag_id>\w+)$', view_script.scriptTag, name='scriptTag'),

    re_path(r'^scene/new/(?P<sceneitem_type>[NADTR])/(?P<sceneitem_id>\d+)/(?P<offset>[-]?\d+)$', view_scene.sceneNew, name='sceneNew'),
    re_path(r'^scene/move/(?P<sceneitem_id>\d+)/(?P<offset>[-]?\d+)$', view_scene.sceneMove, name='sceneMove'),
    re_path(r'^scene/undo-move$', view_scene.sceneUndoMove, name='sceneUndoMove'),
    re_path(r'^scene/autosave/(?P<sceneitem_id>\d+)$', data_safety.scene_autosave, name='sceneAutosave'),
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

    re_path(r'^planner/?$', view_planner.planner, name='planner'),
    re_path(r'^planner/stripboard/?$', view_planner.planner_stripboard, name='plannerStripboard'),
    re_path(r'^planner/dood/?$', view_planner.planner_dood, name='plannerDood'),
    re_path(r'^planner/cast/?$', view_planner.planner_cast, name='plannerCast'),
    re_path(r'^planner/locations/?$', view_planner.planner_locations, name='plannerLocations'),
    re_path(r'^planner/progress/?$', view_planner.planner_progress, name='plannerProgress'),

    # --- Scoped deep links: /p/<project_id>/s/<script_id>/… ---
    re_path(_SCOPE + r'script/(?P<scene_id>\d+)?$', view_script.script, name='script_scoped'),
    re_path(_SCOPE + r'scene/(?P<sceneitem_id>\d+)?$', view_scene.scene, name='scene_scoped'),
    re_path(_SCOPE + r'shot/(?P<sceneitem_id>\d+)?$', view_shot.shot, name='shot_scoped'),
    re_path(_SCOPE + r'role/(?P<role_id>\d+)?$', view_roles.role, name='role_scoped'),
    re_path(_SCOPE + r'person/(?P<person_id>\d+)?$', view_persons.person, name='person_scoped'),
    re_path(_SCOPE + r'time/(?P<time_id>\d+)?$', view_times.time, name='time_scoped'),
    re_path(_SCOPE + r'location/(?P<location_id>\d+)?$', view_locations.location, name='location_scoped'),
    re_path(_SCOPE + r'gadget/(?P<gadget_id>\d+)?$', view_gadgets.gadget, name='gadget_scoped'),
    re_path(_SCOPE + r'audio/(?P<audio_id>\d+)?$', view_audios.audio, name='audio_scoped'),
    re_path(_SCOPE + r'sfx/(?P<sfx_id>\d+)?$', view_sfxs.sfx, name='sfx_scoped'),
    re_path(_SCOPE + r'scheduler/(?P<appointment_id>\d+)?$', view_scheduler.scheduler, name='scheduler_scoped'),
    re_path(_SCOPE + r'planner/?$', view_planner.planner, name='planner_scoped'),
    re_path(_SCOPE + r'planner/stripboard/?$', view_planner.planner_stripboard, name='plannerStripboard_scoped'),
    re_path(_SCOPE + r'planner/dood/?$', view_planner.planner_dood, name='plannerDood_scoped'),
    re_path(_SCOPE + r'planner/cast/?$', view_planner.planner_cast, name='plannerCast_scoped'),
    re_path(_SCOPE + r'planner/locations/?$', view_planner.planner_locations, name='plannerLocations_scoped'),
    re_path(_SCOPE + r'planner/progress/?$', view_planner.planner_progress, name='plannerProgress_scoped'),
]
