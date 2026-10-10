"""
Web app URL routes.
"""
from django.urls import re_path

from . import views

app_name = 'web'

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^contact/?$', views.contact, name='contact'),
    re_path(r'^about/?$', views.about, name='about'),
    re_path(r'^impressum/?$', views.impressum, name='impressum'),
    re_path(r'^datenschutz/?$', views.datenschutz, name='datenschutz'),
]
