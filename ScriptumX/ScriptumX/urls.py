"""
Definition of urls for ScriptumX.
"""

from datetime import datetime
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from app.forms import BootstrapAuthenticationForm
import app
import  django.contrib.auth.views
from . import settings

admin.autodiscover()

urlpatterns = [
    url(r'^', include('app.urls', namespace="app")),

    url(r'^$', app.views.home, name='home'),

    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^seed', app.views.seed, name='seed'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
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
    url(r'^admin/', include(admin.site.urls)),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
