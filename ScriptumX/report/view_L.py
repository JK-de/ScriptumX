from os import path
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.template import RequestContext
from django.utils import timezone
from django.views.generic import View, ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.functions import Lower
from django.views.generic.base import TemplateView
from django import forms

from crispy_forms.utils import render_crispy_form
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, ButtonHolder, Div, Field, HTML, Submit
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineCheckboxes

from report.models import *
from X.models import *
from X.common import *
from X.tags import FormSymbol, gadget_tag_list, handleTagRequest, getTagRequestList
from .M import *

###############################################################################

class ExampleForm(forms.Form):
    favorite_food = forms.CharField(
        label = "What is your favorite food?",
        max_length = 80,
        required = False,
    )

    favorite_color = forms.CharField(
        label = "What is your favorite color?",
        max_length = 80,
        required = False,
    )

    favorite_number = forms.IntegerField(
        label = "Favorite number",
        required = False,
    )

    tag0  = forms.BooleanField( label = "", required = False, )
    tag1  = forms.BooleanField( label = "", required = False, )
    tag2  = forms.BooleanField( label = "", required = False, )
    tag3  = forms.BooleanField( label = "", required = False, )
    tag4  = forms.BooleanField( label = "", required = False, )
    tag5  = forms.BooleanField( label = "", required = False, )
    tag6  = forms.BooleanField( label = "", required = False, )
    tag7  = forms.BooleanField( label = "", required = False, )
    tag8  = forms.BooleanField( label = "", required = False, )
    tag9  = forms.BooleanField( label = "", required = False, )
    tag10 = forms.BooleanField( label = "", required = False, )
    tag11 = forms.BooleanField( label = "", required = False, )

    def __init__(self, *args, **kwargs):
        super(ExampleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        #self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-5'
        #self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(

            #ButtonHolder(
                #Submit('submit', '<i class="fa fa-floppy-o fa-2x"/> Save', css_class='btn btn-default')
                #Submit('submit', 'Save', css_class='btn btn-primary'),
                #Submit('delete', 'Del', css_class='btn btn-danger'),
            #),
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
                Div(FormSymbol(gadget_tag_list[11]['img']), Field('tag11'), style="padding:0; margin:0;", css_class='checkbox-inline'),
                css_class='col-sm-offset-2', style="margin-top:0px;", 
            ),
        )

###############################################################################

class L_GadgetViewXXX(TemplateView):
    template_name = "report/test.html"

    def get_context_data(self, **kwargs):
        context = super(L_GadgetView, self).get_context_data(**kwargs)
        
        env = Env(context['view'].request)
        tag_list = getTagRequestList(env.request, 'gadget')
        gadgets = Gadget.objects.filter( project=env.project_id ).order_by(Lower('name'))

        context['title'] = 'Gadget List'
        context['tag_list'] = tag_list
        context['gadgets'] = gadgets
        context['form'] = ExampleForm()

        return context

###############################################################################


class L_GadgetView(View):
    form_class = ExampleForm
    x_group = 'gadget'
    initial = {'favorite_color': 'abc', 'favorite_food': 'xyz', 'favorite_number': 1}
    template_name = "report/test.html"
    title = 'Gadget List'

    def render_form(self, request, form):
        return render(request, self.template_name, {
            'title': self.title,
            'form': form,
        })

    def render_list(self, request, form, tag_list):
        #color = form.cleaned_data['favorite_color']

        env = Env(request)
        query = getTagQuery(tag_list)
        items = Gadget.objects.filter( project=env.project_id ).filter(query).order_by(Lower('name'))

        item = items[0]
        l = item.getActiveTagImages

        return render(request, self.template_name, {
            'title': self.title,
            'tag_list': tag_list,
            'items': items,
        })

    def get(self, request, *args, **kwargs):
        #env = Env(request)
        tag_list = getTagRequestList(request, self.x_group)
        for tag in tag_list:
            self.initial['tag'+str(tag['idx'])] = tag['active']
        form = self.form_class(initial=self.initial)
        return self.render_form(request, form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            tag_list = getTagRequestList(request, self.x_group)
            for tag in tag_list:
                tag['active'] = form.cleaned_data['tag'+str(tag['idx'])]
            return self.render_list(request, form, tag_list)

        return self.render_form(request, form)
