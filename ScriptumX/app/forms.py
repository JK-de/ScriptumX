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
            'tag2',
            'tag3',
            'tag4',
            'tag5',
            'tag6',
            'tag7',
            'tag8',
            'tag9',
            'tag10',
            'name',
            'description',
            'marker_map',
            'progress',
            ]

    def __init__(self, *args, **kwargs):
        super(GadgetForm, self).__init__(*args, **kwargs)

        img_begin = '{% load staticfiles %}<img src="{% static "'
        img_end = '" %}" />'

        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        #self.helper.form_action = 'submit_survey'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.layout = Layout(

            ButtonHolder(
                Submit('submit', 'Save', css_class='btn btn-default')
            ),
            Div(
                Div(HTML(img_begin + 'app/img/G/tag/Requisite.png' + img_end), Field('tag0', css_class='', ), style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(HTML(img_begin + 'app/img/G/tag/Costume.png' + img_end),   Field('tag1', css_class='', ), style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(HTML(img_begin + 'app/img/G/tag/MakeUp.png' + img_end),    Field('tag2', css_class='', ), style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(HTML(img_begin + 'app/img/G/tag/Camera.png' + img_end),    Field('tag3', css_class='', ), style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(HTML(img_begin + 'app/img/G/tag/Gaffer.png' + img_end),    Field('tag4', css_class='', ), style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(HTML(img_begin + 'app/img/G/tag/Grip.png' + img_end),      Field('tag5', css_class='', ), style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(HTML(img_begin + 'app/img/G/tag/Audio.png' + img_end),     Field('tag6', css_class='', ), style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(HTML(img_begin + 'app/img/G/tag/Special.png' + img_end),   Field('tag7', css_class='', ), style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(HTML(img_begin + 'app/img/G/tag/Tool.png' + img_end),      Field('tag8', css_class='', ), style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(HTML(img_begin + 'app/img/G/tag/Phyro.png' + img_end),     Field('tag9', css_class='', ), style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(HTML(img_begin + 'app/img/G/tag/Catering.png' + img_end),  Field('tag10',css_class='', ), style="padding:0; margin:0;", css_class='checkbox-inline'),
                css_class='col-sm-offset-2', style="margin-top:-30px;", 
            ),
            #Fieldset(
                #'first arg is the legend of the fieldset',
                'name',
                Field('description', style="max-width:98%; min-width:98%;", rows=4),

                #InlineCheckboxes('tag0', 'tag1'),
                #Div( 
                #    Field('tag0', css_class="btn"),
                #    Field('tag1', css_class="btn"),
                #    css_class='checkbox-inline',
                #),
                #Div(
                #    Div(Field('tag0', css_class='span12 input-large',), css_class='span2'),
                #    Div(Field('tag1', css_class='span12 input-large',), css_class='span2'),
                #    css_class='checkbox-inline',
                #),
                #Div(
                #    InlineCheckboxes('tag0'),
                #    InlineCheckboxes('tag1'),
                #    css_class='checkbox-inline',
                #),
                #Field('tag1'),
                Field('marker_map'),
                Field('progress'),
                #TODO : http://django-floppyforms.readthedocs.org/en/latest/examples.html#a-slider
                #TODO : https://github.com/seiyria/bootstrap-slider
            #),
            
            #InlineCheckboxes('tag0','tag1',),
            #StrictButton('Sign in', css_class='btn-default'),
        )
        #self.helper[1:3].wrap_together(Div, inline=True, css_class="checkbox-inline")

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
