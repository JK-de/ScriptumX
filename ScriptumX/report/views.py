#from io import StringIO
#from xhtml2pdf import pisa
#from django.template.loader import get_template
#from django.template import Context
#from django.http import HttpResponse
#from cgi import escape


from os import path
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.template import RequestContext
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.functions import Lower
from django.views.generic.base import TemplateView

from crispy_forms.utils import render_crispy_form

from report.models import *
from X.models import *
from X.common import *
from X.tags import FormSymbol, gadget_tag_list, handleTagRequest, getTagRequestList
from .M import *

#django-wkhtmltopdf

###############################################################################
#pip install reportlab
#http://stackoverflow.com/questions/1377446/render-html-to-pdf-in-django-site


#def render_to_pdf(request, template_src, context_dict):
#    template = get_template(template_src)
#    context = Context(context_dict)
#    html  = template.render(context)
#    result = StringIO.StringIO()

#    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
#    if not pdf.err:
#        return HttpResponse(result.getvalue(), content_type='application/pdf')
#    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

###############################################################################

#def test2(request):
#    """Handles home page"""

#    env = Env(request)
    
#    tag_list = getTagRequestList(request, 'gadget')
#    gadgets = Gadget.objects.filter( project=env.project_id ).order_by(Lower('name'))

#    return render_to_pdf(request, 'report/test.html', {
#        'pagesize':'A4',
#        'title': 'TEST',
#        'tag_list': tag_list,
#        'gadgets': gadgets,
#        'datetime': datetime.now(),
#    })

###############################################################################


#django-easy-pdf



#from easy_pdf.views import PDFTemplateView

def test2(request):
    """Handles home page"""

    env = Env(request)
    
    tag_list = getTagRequestList(request, 'gadget')
    gadgets = Gadget.objects.filter( project=env.project_id ).order_by(Lower('name'))

    return render(request, 'report/test2.html', {
        'title': 'TEST',
        'tag_list': tag_list,
        'gadgets': gadgets,
        'datetime': datetime.now(),
    })


#class MyPDF(PDFTemplateView):
#    filename = 'my_pdf.pdf'
#    template_name = 'report/test2.html'
#    cmd_options = {
#        'pagesize':'A4',
#        'title': 'TEST',
#    }

#    def get_context_data(self, **kwargs):
#        return super(HelloPDFView, self).get_context_data(
#            pagesize="A4",
#            title="Hi there!",
#            **kwargs
#        )

###############################################################################

def test1(request):
    """Handles home page"""

    env = Env(request)
    
    tag_list = getTagRequestList(request, 'gadget')
    gadgets = Gadget.objects.filter( project=env.project_id ).order_by(Lower('name'))

    return render(request, 'report/test.html', {
        'title': 'TEST',
        'tag_list': tag_list,
        'gadgets': gadgets,
        'datetime': datetime.now(),
    })

###############################################################################

class Test3View(TemplateView):
    template_name = "report/test.html"

    def get_context_data(self, **kwargs):
        context = super(Test3View, self).get_context_data(**kwargs)
        
        env = Env(context['view'].request)
        tag_list = getTagRequestList(env.request, 'gadget')
        gadgets = Gadget.objects.filter( project=env.project_id ).order_by(Lower('name'))

        context['title'] = 'TEST'
        context['tag_list'] = tag_list
        context['gadgets'] = gadgets
        context['datetime'] = datetime.now()

        return context

class TestM1View(TemplateView):
    template_name = "report/testM1.html"

    def get_context_data(self, **kwargs):
        context = super(TestM1View, self).get_context_data(**kwargs)
        
        env = Env(context['view'].request)
        tag_list = getTagRequestList(env.request, 'gadget')
        gadgets = Gadget.objects.filter( project=env.project_id ).order_by(Lower('name'))
        scenes = Scene.objects.filter( project=env.project_id, script=env.script_id ).order_by('order')

        m = M(gadgets, scenes)

        for scene in scenes:
            row = m.getRowIndex(scene)

            linked_gadgets = scene.gadgets.all()
            for g in linked_gadgets:
                col = m.getColIndex(g)
                m.cells[row][col].text = "&#x26AB;"


        context['env'] = env
        context['title'] = 'TEST'
        context['tag_list'] = tag_list
        context['M'] = m
        context['datetime'] = datetime.now()

        return context

class TestM2View(TemplateView):
    template_name = "report/testM1.html"

    def get_context_data(self, **kwargs):
        context = super(TestM2View, self).get_context_data(**kwargs)
        
        env = Env(context['view'].request)
        tag_list = getTagRequestList(env.request, 'role')
        roles = Role.objects.filter( project=env.project_id ).order_by(Lower('name'))
        scenes = Scene.objects.filter( project=env.project_id, script=env.script_id ).order_by('order')

        m = M(roles, scenes)

        for role in roles:
            col = m.getColIndex(role)
            m.cells[0][col].background_color = role.color

        for scene in scenes:
            row = m.getRowIndex(scene)

            sceneitems = SceneItem.objects.filter( scene=scene )
            for sceneitem in sceneitems:
                if sceneitem.role:
                    col = m.getColIndex(sceneitem.role)
                    m.cells[row][col].text = "&#x26AB;"


        context['env'] = env
        context['title'] = 'TEST'
        context['tag_list'] = tag_list
        context['M'] = m
        context['datetime'] = datetime.now()

        return context