"""
Definition of urls for polls viewing and voting.
"""
from datetime import datetime
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
import  django.contrib.auth.views, django.contrib.auth.urls
#from . import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

import authentication
from authentication.views import *
from .forms import BootstrapAuthenticationForm


from django.conf.urls import patterns, url

urlpatterns = [

    url(r'^login/',
        django.contrib.auth.views.login,
        {
            'template_name': 'authentication/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'datetime':datetime.now(),
            }
        },
        name='login'),

    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    

    #url(r'^$', web.views.home, name='home'),

    #url(r'^contact$', web.views.contact, name='contact'),
    #url(r'^about', web.views.about, name='about'),
    ]
