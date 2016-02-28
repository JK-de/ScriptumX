"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import *

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form- control',
                                   'placeholder':'Password'}))

class GadgetForm(forms.ModelForm):
    """Edit form for Gadget model"""
    class Meta:
        model = Gadget
        fields = [
            'tag0',
            'tag1',
            'name',
            'description',
            'marker_map',
            'progress',
            ]

    
    def clean_name(self):
      name = self.cleaned_data.get('name')
      return name



    #    #Props
    #name = models.CharField(max_length=30)
    #description = models.TextField(blank=True)
    ##tag_map = models.PositiveIntegerField(default=0x7FFFFFFF)
    #marker_map = models.PositiveIntegerField(default=0)

    #tag0 = models.BooleanField(default=0)
    #tag1 = models.BooleanField(default=0)
    #tag2 = models.BooleanField(default=0)
    #tag3 = models.BooleanField(default=0)
    #tag4 = models.BooleanField(default=0)
    #tag5 = models.BooleanField(default=0)
    #tag6 = models.BooleanField(default=0)
    #tag7 = models.BooleanField(default=0)
    #tag8 = models.BooleanField(default=0)
    #tag9 = models.BooleanField(default=0)

    #progress = models.PositiveSmallIntegerField(default=0)
