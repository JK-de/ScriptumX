"""
Definition of urls for polls viewing and voting.
"""

from django.conf.urls import patterns, url
from app.views import *
import app

urlpatterns = [

    url(r'^gadget/(?P<gadget_id>\d+)?$', app.views.gadget, name='gadget'),
    url(r'^gadget/tag/(?P<tag_id>\w+)?$', app.views.gadgetTag, name='gadgetTag'),

    url(r'^project/(?P<id>\d+)?$', app.views.dummy, name='dummy'),
    url(r'^script/(?P<id>\d+)?$', app.views.dummy, name='dummy'),
    url(r'^scene/(?P<id>\d+)?$', app.views.dummy, name='dummy'),
    url(r'^set/(?P<id>\d+)?$', app.views.dummy, name='dummy'),
    url(r'^role/(?P<id>\d+)?$', app.views.dummy, name='dummy'),
    url(r'^folk/(?P<id>\d+)?$', app.views.dummy, name='dummy'),
    url(r'^sfx/(?P<id>\d+)?$', app.views.dummy, name='dummy'),
    url(r'^audio/(?P<id>\d+)?$', app.views.dummy, name='dummy'),
    url(r'^schedule/(?P<id>\d+)?$', app.views.dummy, name='dummy'),
    ]
