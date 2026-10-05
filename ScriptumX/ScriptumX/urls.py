"""
Definition of urls for ScriptumX.
"""

from django.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from . import settings
from X import views as x_views

admin.autodiscover()

urlpatterns = [
    re_path(r'', include(('X.urls', 'X'), namespace='X')),
    re_path(r'', include(('web.urls', 'web'), namespace='web')),
    re_path(r'', include(('report.urls', 'report'), namespace='report')),
    re_path(r'', include(('authentication.urls', 'authentication'), namespace='authentication')),

    re_path(r'^', include('django.contrib.auth.urls')),

    re_path(r'^seed/?$', x_views.seed, name='seed'),
    re_path(r'^importceltx/?$', x_views.importceltx, name='importceltx'),

    re_path(r'^admin/', admin.site.urls),

    re_path(
        r'^favicon\.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('favicon.ico'),
            permanent=False,
        ),
        name='favicon',
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
