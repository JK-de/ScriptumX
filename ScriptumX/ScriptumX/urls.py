"""
Definition of urls for ScriptumX.
"""

from datetime import datetime
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
import  django.contrib.auth.views, django.contrib.auth.urls
from . import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

import X
import web
import report
import authentication

admin.autodiscover()

urlpatterns = [
    url(r'', include('X.urls', namespace="X")),
    url(r'', include('web.urls', namespace="web")),
    url(r'', include('report.urls', namespace="report")),
    url(r'', include('authentication.urls', namespace="authentication")),

    url('^', include('django.contrib.auth.urls')),

    url(r'^seed', X.views.seed, name='seed'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('favicon.ico'),
            permanent=False),
        name="favicon"
        ),

    ] + static('static', document_root=settings.STATIC_ROOT)
    #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
