"""
Definition of urls for polls viewing and voting.
"""
import report
from report.views import *
from report.view_L import *
from report.view_M import *
from report.view_S import *
from report.view_C import *
#from wkhtmltopdf.views import PDFTemplateView

from django.conf.urls import patterns, url

urlpatterns = [

    url(r'^test$', report.view_C.cards, name='export_cards'),
    url(r'^s/(?P<selected_scene_id>\d+)?$', ScriptView.as_view(), name='s'),

    url(r'^test1$', report.views.test1, name='test1'),
    url(r'^test2$', report.views.test2, name='test2'),
    url(r'^test3$', Test3View.as_view(), name='test3'),
    url(r'^testM1$', TestM1View.as_view(), name='testM1'),
    url(r'^testM2$', TestM2View.as_view(), name='testM2'),

    url(r'^L$', L_GroupedGadgetView.as_view(), name='L_'),
    url(r'^M$', M_SceneRoleView.as_view(), name='M_'),

    # simple List
    url(r'^report/L/simple_role$', L_RoleView.as_view(), name='L_Role'),
    url(r'^report/L/simple_person$', L_PersonView.as_view(), name='L_Person'),
    url(r'^report/L/simple_time$', L_TimeView.as_view(), name='L_Time'),
    url(r'^report/L/simple_location$', L_LocationView.as_view(), name='L_Location'),
    url(r'^report/L/simple_gadget$', L_GadgetView.as_view(), name='L_Gadget'),
    url(r'^report/L/simple_sfx$', L_SFXView.as_view(), name='L_SFX'),
    url(r'^report/L/simple_audio$', L_AudioView.as_view(), name='L_Audio'),
    url(r'^report/L/simple_scene$', L_SceneView.as_view(), name='L_Scene'),

    # grouped List
    url(r'^report/L/grouped_role$', L_GroupedRoleView.as_view(), name='L_g_Role'),
    url(r'^report/L/grouped_person$', L_GroupedPersonView.as_view(), name='L_g_Person'),
    url(r'^report/L/grouped_time$', L_GroupedTimeView.as_view(), name='L_g_Time'),
    url(r'^report/L/grouped_location$', L_GroupedLocationView.as_view(), name='L_g_Location'),
    url(r'^report/L/grouped_gadget$', L_GroupedGadgetView.as_view(), name='L_g_Gadget'),
    url(r'^report/L/grouped_sfx$', L_GroupedSFXView.as_view(), name='L_g_SFX'),
    url(r'^report/L/grouped_audio$', L_GroupedAudioView.as_view(), name='L_g_Audio'),

    # Scene vs X Matrix
    url(r'^report/M/scene_role$', M_SceneRoleView.as_view(), name='M_SceneRole'),
    url(r'^report/M/scene_person$', M_ScenePersonView.as_view(), name='M_ScenePerson'),
    url(r'^report/M/scene_time$', M_SceneTimeView.as_view(), name='M_SceneTime'),
    url(r'^report/M/scene_location$', M_SceneLocationView.as_view(), name='M_SceneLocation'),
    url(r'^report/M/scene_gadget$', M_SceneGadgetView.as_view(), name='M_SceneGadget'),
    url(r'^report/M/scene_sfx$', M_SceneSFXView.as_view(), name='M_SceneSFX'),
    url(r'^report/M/scene_audio$', M_SceneAudioView.as_view(), name='M_SceneAudio'),

    # Scripts
    url(r'^report/S/read/(?P<selected_scene_id>\d+)?$', ScriptView.as_view(), name='S_read'),
    url(r'^report/S/readpdf/(?P<selected_scene_id>\d+)?$', ScriptPDFView.as_view(), name='S_readpdf'),

    # Cards
    url(r'^report/C/script$', CardsView.as_view(), name='C_Script'),

    #url(r'^pdf2/$', MyPDF.as_view(), name='pdf2'),
    #url(r'^pdf1/$', PDFTemplateView.as_view(template_name='report/test2.html', filename='my_pdf.pdf'), name='pdf1'),
    ]
