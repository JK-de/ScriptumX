"""
Definition of urls for polls viewing and voting.
"""
import report
from report.views import *
from report.view_L import *
#from wkhtmltopdf.views import PDFTemplateView

from django.conf.urls import patterns, url

urlpatterns = [

    url(r'^test1$', report.views.test1, name='test1'),
    url(r'^test2$', report.views.test2, name='test2'),
    url(r'^test3$', Test3View.as_view(), name='test3'),
    url(r'^testM1$', TestM1View.as_view(), name='testM1'),
    url(r'^testM2$', TestM2View.as_view(), name='testM2'),

    url(r'^L$', L_GadgetView.as_view(), name='L_'),

    url(r'^report/L/simple_role$', L_GadgetView.as_view(), name='L_'),
    url(r'^report/M/scene_role$', TestM2View.as_view(), name='testM2'),

    #url(r'^pdf2/$', MyPDF.as_view(), name='pdf2'),
    #url(r'^pdf1/$', PDFTemplateView.as_view(template_name='report/test2.html', filename='my_pdf.pdf'), name='pdf1'),
    ]
