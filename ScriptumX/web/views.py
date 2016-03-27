"""
Definition of views.
"""

from os import path
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.template import RequestContext
from django.utils import timezone
from django.views.generic import ListView, DetailView
#from django.views.decorators import clickjacking
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from crispy_forms.utils import render_crispy_form

from web.models import *
from X.common import *

###############################################################################

###############################################################################
###############################################################################
###############################################################################


#@require_save
def home(request):
    """Handles home page"""
    
    return render(request, 'web/home.html', {
        'title': 'Home',
        'datetime': datetime.now(),
    })

###############################################################################

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'web/contact.html',
        context_instance = RequestContext(request,
        {
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        })
    )

###############################################################################

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'web/about.html',
        context_instance = RequestContext(request,
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        })
    )

###############################################################################

def impressum(request):
    """Renders the impressum page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'web/impressum.html',
        context_instance = RequestContext(request,
        {
            'title': 'Impressum',
        })
    )

###############################################################################

