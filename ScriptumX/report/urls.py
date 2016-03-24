"""
Definition of urls for polls viewing and voting.
"""
import report
from report.views import test1, test2, MyPDF
from wkhtmltopdf.views import PDFTemplateView

from django.conf.urls import patterns, url

urlpatterns = [

    url(r'^test1$', report.views.test1, name='test1'),
    url(r'^test2$', report.views.test2, name='test2'),

    url(r'^pdf2/$', MyPDF.as_view(), name='pdf2'),
    url(r'^pdf1/$', PDFTemplateView.as_view(template_name='report/test2.html',
                                           filename='my_pdf.pdf'), name='pdf1'),
    ]
