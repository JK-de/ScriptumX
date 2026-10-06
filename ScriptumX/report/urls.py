"""
Report app URL routes.
"""
from django.urls import re_path

from report import views
from report import view_C
from report.view_L import (
    L_RoleView, L_PersonView, L_TimeView, L_LocationView, L_GadgetView,
    L_SFXView, L_AudioView, L_SceneView,
    L_GroupedRoleView, L_GroupedPersonView, L_GroupedTimeView,
    L_GroupedLocationView, L_GroupedGadgetView, L_GroupedSFXView, L_GroupedAudioView,
)
from report.view_M import (
    M_SceneRoleView, M_ScenePersonView, M_SceneTimeView, M_SceneLocationView,
    M_SceneGadgetView, M_SceneSFXView, M_SceneAudioView,
)
from report.view_S import ScriptView, ScriptPDFView
from report.view_C import CardsView
from report.views import Test3View, TestM1View, TestM2View
from report.collab import SharedReportView, revoke_share_link

app_name = 'report'

_SCOPE = r'^p/(?P<project_id>\d+)/s/(?P<script_id>\d+)/'

urlpatterns = [
    re_path(r'^test$', view_C.cards, name='export_cards'),
    re_path(r'^s/(?P<selected_scene_id>\d+)?$', ScriptView.as_view(), name='s'),

    re_path(r'^test1$', views.test1, name='test1'),
    re_path(r'^test2$', views.test2, name='test2'),
    re_path(r'^test3$', Test3View.as_view(), name='test3'),
    re_path(r'^testM1$', TestM1View.as_view(), name='testM1'),
    re_path(r'^testM2$', TestM2View.as_view(), name='testM2'),

    re_path(r'^L$', L_GroupedGadgetView.as_view(), name='L_'),
    re_path(r'^M$', M_SceneRoleView.as_view(), name='M_'),

    # F14: tokenized read-only share links (no login)
    re_path(r'^report/share/(?P<token>[-A-Za-z0-9_=]+)/$', SharedReportView.as_view(), name='shared_report'),
    re_path(r'^report/share/(?P<token>[-A-Za-z0-9_=]+)/revoke/$', revoke_share_link, name='revoke_share'),

    re_path(r'^report/L/simple_role$', L_RoleView.as_view(), name='L_Role'),
    re_path(r'^report/L/simple_person$', L_PersonView.as_view(), name='L_Person'),
    re_path(r'^report/L/simple_time$', L_TimeView.as_view(), name='L_Time'),
    re_path(r'^report/L/simple_location$', L_LocationView.as_view(), name='L_Location'),
    re_path(r'^report/L/simple_gadget$', L_GadgetView.as_view(), name='L_Gadget'),
    re_path(r'^report/L/simple_sfx$', L_SFXView.as_view(), name='L_SFX'),
    re_path(r'^report/L/simple_audio$', L_AudioView.as_view(), name='L_Audio'),
    re_path(r'^report/L/simple_scene$', L_SceneView.as_view(), name='L_Scene'),

    re_path(r'^report/L/grouped_role$', L_GroupedRoleView.as_view(), name='L_g_Role'),
    re_path(r'^report/L/grouped_person$', L_GroupedPersonView.as_view(), name='L_g_Person'),
    re_path(r'^report/L/grouped_time$', L_GroupedTimeView.as_view(), name='L_g_Time'),
    re_path(r'^report/L/grouped_location$', L_GroupedLocationView.as_view(), name='L_g_Location'),
    re_path(r'^report/L/grouped_gadget$', L_GroupedGadgetView.as_view(), name='L_g_Gadget'),
    re_path(r'^report/L/grouped_sfx$', L_GroupedSFXView.as_view(), name='L_g_SFX'),
    re_path(r'^report/L/grouped_audio$', L_GroupedAudioView.as_view(), name='L_g_Audio'),

    re_path(r'^report/M/scene_role$', M_SceneRoleView.as_view(), name='M_SceneRole'),
    re_path(r'^report/M/scene_person$', M_ScenePersonView.as_view(), name='M_ScenePerson'),
    re_path(r'^report/M/scene_time$', M_SceneTimeView.as_view(), name='M_SceneTime'),
    re_path(r'^report/M/scene_location$', M_SceneLocationView.as_view(), name='M_SceneLocation'),
    re_path(r'^report/M/scene_gadget$', M_SceneGadgetView.as_view(), name='M_SceneGadget'),
    re_path(r'^report/M/scene_sfx$', M_SceneSFXView.as_view(), name='M_SceneSFX'),
    re_path(r'^report/M/scene_audio$', M_SceneAudioView.as_view(), name='M_SceneAudio'),

    re_path(r'^report/S/read/(?P<selected_scene_id>\d+)?$', ScriptView.as_view(), name='S_read'),
    re_path(r'^report/S/readpdf/(?P<selected_scene_id>\d+)?$', ScriptPDFView.as_view(), name='S_readpdf'),

    re_path(r'^report/C/script$', CardsView.as_view(), name='C_Script'),

    # Scoped deep links: /p/<project_id>/s/<script_id>/report/…
    re_path(_SCOPE + r'report/L/simple_role$', L_RoleView.as_view(), name='L_Role_scoped'),
    re_path(_SCOPE + r'report/L/simple_person$', L_PersonView.as_view(), name='L_Person_scoped'),
    re_path(_SCOPE + r'report/L/simple_time$', L_TimeView.as_view(), name='L_Time_scoped'),
    re_path(_SCOPE + r'report/L/simple_location$', L_LocationView.as_view(), name='L_Location_scoped'),
    re_path(_SCOPE + r'report/L/simple_gadget$', L_GadgetView.as_view(), name='L_Gadget_scoped'),
    re_path(_SCOPE + r'report/L/simple_sfx$', L_SFXView.as_view(), name='L_SFX_scoped'),
    re_path(_SCOPE + r'report/L/simple_audio$', L_AudioView.as_view(), name='L_Audio_scoped'),
    re_path(_SCOPE + r'report/L/simple_scene$', L_SceneView.as_view(), name='L_Scene_scoped'),
    re_path(_SCOPE + r'report/L/grouped_role$', L_GroupedRoleView.as_view(), name='L_g_Role_scoped'),
    re_path(_SCOPE + r'report/L/grouped_person$', L_GroupedPersonView.as_view(), name='L_g_Person_scoped'),
    re_path(_SCOPE + r'report/L/grouped_time$', L_GroupedTimeView.as_view(), name='L_g_Time_scoped'),
    re_path(_SCOPE + r'report/L/grouped_location$', L_GroupedLocationView.as_view(), name='L_g_Location_scoped'),
    re_path(_SCOPE + r'report/L/grouped_gadget$', L_GroupedGadgetView.as_view(), name='L_g_Gadget_scoped'),
    re_path(_SCOPE + r'report/L/grouped_sfx$', L_GroupedSFXView.as_view(), name='L_g_SFX_scoped'),
    re_path(_SCOPE + r'report/L/grouped_audio$', L_GroupedAudioView.as_view(), name='L_g_Audio_scoped'),
    re_path(_SCOPE + r'report/M/scene_role$', M_SceneRoleView.as_view(), name='M_SceneRole_scoped'),
    re_path(_SCOPE + r'report/M/scene_person$', M_ScenePersonView.as_view(), name='M_ScenePerson_scoped'),
    re_path(_SCOPE + r'report/M/scene_time$', M_SceneTimeView.as_view(), name='M_SceneTime_scoped'),
    re_path(_SCOPE + r'report/M/scene_location$', M_SceneLocationView.as_view(), name='M_SceneLocation_scoped'),
    re_path(_SCOPE + r'report/M/scene_gadget$', M_SceneGadgetView.as_view(), name='M_SceneGadget_scoped'),
    re_path(_SCOPE + r'report/M/scene_sfx$', M_SceneSFXView.as_view(), name='M_SceneSFX_scoped'),
    re_path(_SCOPE + r'report/M/scene_audio$', M_SceneAudioView.as_view(), name='M_SceneAudio_scoped'),
    re_path(_SCOPE + r'report/S/read/(?P<selected_scene_id>\d+)?$', ScriptView.as_view(), name='S_read_scoped'),
    re_path(_SCOPE + r'report/S/readpdf/(?P<selected_scene_id>\d+)?$', ScriptPDFView.as_view(), name='S_readpdf_scoped'),
    re_path(_SCOPE + r'report/C/script$', CardsView.as_view(), name='C_Script_scoped'),
]
