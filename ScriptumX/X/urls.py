"""
Definition of urls for polls viewing and voting.
"""

from django.conf.urls import patterns, url
from X.views import *
from X.view_script import *
from X.view_gadget import *
import X

urlpatterns = [

    url(r'^script/(?P<scene_id>\d+)?$', X.view_script.script, name='script'),
    url(r'^script/tag/(?P<tag_id>\w+)?$', X.view_script.scriptTag, name='scriptTag'),

    url(r'^gadget/(?P<gadget_id>\d+)?$', X.view_gadget.gadget, name='gadget'),
    url(r'^gadget/tag/(?P<tag_id>\w+)?$', X.view_gadget.gadgetTag, name='gadgetTag'),

    url(r'^project/(?P<id>\d+)?$', X.views.dummy, name='dummy'),
    url(r'^scene/(?P<id>\d+)?$', X.views.dummy, name='dummy'),
    url(r'^set/(?P<id>\d+)?$', X.views.dummy, name='dummy'),
    url(r'^role/(?P<id>\d+)?$', X.views.dummy, name='dummy'),
    url(r'^folk/(?P<id>\d+)?$', X.views.dummy, name='dummy'),
    url(r'^sfx/(?P<id>\d+)?$', X.views.dummy, name='dummy'),
    url(r'^audio/(?P<id>\d+)?$', X.views.dummy, name='dummy'),
    url(r'^schedule/(?P<id>\d+)?$', X.views.dummy, name='dummy'),
    ]
