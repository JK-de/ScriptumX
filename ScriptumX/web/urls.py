"""
Definition of urls for polls viewing and voting.
"""
import web
from web.views import *

from django.conf.urls import patterns, url

urlpatterns = [

    url(r'^$', web.views.home, name='home'),

    url(r'^contact$', web.views.contact, name='contact'),

    url(r'^about', web.views.about, name='about'),

    url(r'^impressum', web.views.impressum, name='impressum'),
    ]
