"""
Definition of urls for ScriptumX.
"""

from datetime import datetime
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from X.forms import BootstrapAuthenticationForm
import X
import  django.contrib.auth.views
from . import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = [
    url(r'^', include('X.urls', namespace="X")),

    url(r'^$', X.views.home, name='home'),

    url(r'^contact$', X.views.contact, name='contact'),
    url(r'^about', X.views.about, name='about'),
    url(r'^seed', X.views.seed, name='seed'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'X/login.html',
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

    url(
        r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('favicon.ico'),
            permanent=False),
        name="favicon"
        ),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
