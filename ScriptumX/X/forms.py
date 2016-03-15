"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, ButtonHolder, Div, Field, HTML
from crispy_forms.bootstrap import InlineCheckboxes
from .tags import FormSymbol, gadget_tag_list


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

###############################################################################
###############################################################################

class NoteForm(forms.ModelForm):
    """Edit form for Gadget model"""
    class Meta:
        model = Note
        fields = [
            'text',
            ]

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        #self.helper.form_action = 'submit_survey'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = ''
        self.helper.field_class = 'col-sm-12'
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            #Div(
            #    FormSymbol('img/note.png'),
            #    #HTML("<br/>Lorem Ipsum<br/>{{ formNote.text }}"),
            #    css_class='pull-left', style="", 
            #),
            Div(
                #FormSymbol('img/note.png'),
                Field('text', style="max-width:100%; min-width:100%; background-color:palegoldenrod;", autocomplete='on', rows=2),
                css_class='col-sm-offset-2', style="", 
            ),
        )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

###############################################################################
