"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Field, HTML
from crispy_forms.bootstrap import InlineCheckboxes


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses bootstrap CSS."""
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'User name',
        }),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }),
    )
