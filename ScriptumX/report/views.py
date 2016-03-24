#from io import StringIO
#from xhtml2pdf import pisa
#from django.template.loader import get_template
#from django.template import Context
#from django.http import HttpResponse
#from cgi import escape


from report.models import *
from X.models import *
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.template import RequestContext
from django.utils import timezone
from django.views.generic import ListView, DetailView
from os import path
from django.core.exceptions import ObjectDoesNotExist
from crispy_forms.utils import render_crispy_form
from django.db.models import Q
from django.db.models.functions import Lower

from X.common import *
from X.tags import FormSymbol, gadget_tag_list, handleTagRequest, getTagRequestList

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



from wkhtmltopdf.views import PDFTemplateView

def test2(request):
    """Handles home page"""

    env = Env(request)
    
    tag_list = getTagRequestList(request, 'gadget')
    gadgets = Gadget.objects.filter( project=env.project_id ).order_by(Lower('name'))

    return render(request, 'report/test.html', {
        'pagesize':'A4',
        'title': 'TEST',
        'tag_list': tag_list,
        'gadgets': gadgets,
        'datetime': datetime.now(),
    })

class MyPDF(PDFTemplateView):
    filename = 'my_pdf.pdf'
    template_name = 'report/test2.html'
    cmd_options = {
        'pagesize':'A4',
        'title': 'TEST',
    }

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
