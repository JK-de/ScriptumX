"""
Definition of views.
"""

from datetime import datetime

from django.http import HttpRequest
from django.shortcuts import render


def home(request):
    """Handles home page"""
    return render(request, 'web/home.html', {
        'title': 'Home',
        'datetime': datetime.now(),
    })


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request, 'web/contact.html', {
        'title': 'Contact',
        'message': 'Your contact page.',
        'year': datetime.now().year,
    })


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request, 'web/about.html', {
        'title': 'About',
        'message': 'Your application description page.',
        'year': datetime.now().year,
    })


def impressum(request):
    """Renders the impressum page."""
    assert isinstance(request, HttpRequest)
    return render(request, 'web/impressum.html', {
        'title': 'Impressum',
    })


def datenschutz(request):
    """Renders the German privacy policy page."""
    assert isinstance(request, HttpRequest)
    return render(request, 'web/datenschutz.html', {
        'title': 'Datenschutzerklärung',
    })
