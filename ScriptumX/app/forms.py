"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, ButtonHolder
from crispy_forms.bootstrap import InlineCheckboxes


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

    def __init__(self, *args, **kwargs):
        super(GadgetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'blueForms'
        self.helper.form_action = 'submit_survey'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-2'
        self.helper.field_class = 'col-xs-8'
        self.helper.layout = Layout(
            Fieldset(
                'first arg is the legend of the fieldset',
                'name',
                'description',
                InlineCheckboxes('tag0'),
                InlineCheckboxes('tag1'),
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            ),
            #InlineCheckboxes('tag0','tag1',),
            #StrictButton('Sign in', css_class='btn-default'),
        )

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
