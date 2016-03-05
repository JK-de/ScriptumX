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

        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        #self.helper.form_action = 'submit_survey'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.form_tag = False
        self.helper.layout = Layout(

            ButtonHolder(
                #Submit('submit', '<i class="fa fa-floppy-o fa-2x"/> Save', css_class='btn btn-default')
                #Submit('submit', 'Save', css_class='btn btn-primary'),
                #Submit('delete', 'Del', css_class='btn btn-danger'),
            ),
            Div(
                Div(FormSymbol(gadget_tag_list[0]['img']),  Field('tag0'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(gadget_tag_list[1]['img']),  Field('tag1'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(gadget_tag_list[2]['img']),  Field('tag2'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(gadget_tag_list[3]['img']),  Field('tag3'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(gadget_tag_list[4]['img']),  Field('tag4'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(gadget_tag_list[5]['img']),  Field('tag5'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(gadget_tag_list[6]['img']),  Field('tag6'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(gadget_tag_list[7]['img']),  Field('tag7'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(gadget_tag_list[8]['img']),  Field('tag8'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(gadget_tag_list[9]['img']),  Field('tag9'),  style="padding:0; margin:0;", css_class='checkbox-inline'),
                Div(FormSymbol(gadget_tag_list[10]['img']), Field('tag10'), style="padding:0; margin:0;", css_class='checkbox-inline'),
                css_class='col-sm-offset-2', style="margin-top:10px;", 
            ),
            #Fieldset(
                #'first arg is the legend of the fieldset',
                Field('name'),
                Field('description', style="max-width:100%; min-width:100%;", rows=10),

                Field('marker_map'),
#Div(  data-provide="slider", data-slider-min="0", data-slider-max="100", data-slider-step="1"
#                Field('progress',  data-provide="slider", data-slider-min="0", data-slider-max="100", data-slider-step="1" ),
#),
                ###Field('progress'),

                ###Field('progress',  css_class='jk' ),

#                HTML(
#'<div class="form-group">'
#'	<label for="inputName" class="col-sm-2 control-label">My-Progress</label>                                                          '
#'	<div class="col-sm-10">                                                                                                              '
#'		<input type="number" class="form-control" id="inputName" name="progress" placeholder="Lorem" value="{{form.progress.value}}"     '
#'            data-provide="slider"                                                                                                       '
#'            data-slider-min="1"                                                                                                         '
#'            data-slider-max="100"                                                                                                       '
#'            data-slider-step="1"                                                                                                        '
#'            data-slider-value="{{form.progress.value}}"                                                                                 '
#'            data-slider-tooltip="hide"                                                                                                  '
#'            >                                                                                                                           '
#'	</div>                                                                                                                               '
#'</div>                                                                                                                                  '
#                ),

                #Field('progress'),

                #Field('progress', template="./templates/app/tmpl_slider_progress.html"),
                Field('progress', template="D:/X/ScriptumX/app/templates/app/tmpl_slider_progress.html"),

                #Div(
                #    'progress',
                #    template="./templates/app/tmpl_slider_progress.html"
                #),

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

###############################################################################
