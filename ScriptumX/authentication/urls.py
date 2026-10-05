"""
Authentication URL routes.
"""
from datetime import datetime

from django.contrib.auth import views as auth_views
from django.urls import re_path

from .forms import BootstrapAuthenticationForm

app_name = 'authentication'

urlpatterns = [
    re_path(
        r'^login/?$',
        auth_views.LoginView.as_view(
            template_name='authentication/login.html',
            authentication_form=BootstrapAuthenticationForm,
            extra_context={
                'title': 'Log in',
                'datetime': datetime.now(),
            },
        ),
        name='login',
    ),
    re_path(
        r'^logout/?$',
        auth_views.LogoutView.as_view(next_page='/'),
        name='logout',
    ),
]
