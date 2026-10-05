# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import os


class UnsupportedMediaPathException(Exception):
    pass


def fetch_resources(uri, rel):
    """
    Callback to allow xhtml2pdf/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.
    """
    if settings.MEDIA_URL and uri.startswith(settings.MEDIA_URL):
        path = os.path.join(
            settings.MEDIA_ROOT,
            uri.replace(settings.MEDIA_URL, ""),
        )
    elif settings.STATIC_URL and uri.startswith(settings.STATIC_URL):
        path = os.path.join(
            settings.STATIC_ROOT,
            uri.replace(settings.STATIC_URL, ""),
        )
        # Fall back to app static dirs during DEBUG when collectstatic wasn't run
        if not os.path.exists(path):
            for app_static in (
                os.path.join(settings.PROJECT_ROOT, 'X', 'static') if hasattr(settings, 'PROJECT_ROOT') else None,
            ):
                if app_static:
                    candidate = os.path.join(app_static, uri.replace(settings.STATIC_URL, ""))
                    if os.path.exists(candidate):
                        return candidate
    else:
        raise UnsupportedMediaPathException(
            'media urls must start with %s or %s' % (
                settings.MEDIA_URL, settings.STATIC_URL))
    return path


def generate_pdf_template_object(template_object, file_object, context):
    """
    Inner function to pass template objects directly instead of passing a filename
    """
    html = template_object.render(context)
    pisa.CreatePDF(
        html,
        dest=file_object,
        encoding='UTF-8',
        link_callback=fetch_resources,
    )
    return file_object


def generate_pdf(template_name, file_object=None, context=None):  # pragma: no cover
    """
    Uses the xhtml2pdf library to render a PDF to the passed file_object, from the
    given template name.
    """
    if not file_object:
        file_object = BytesIO()
    if not context:
        context = {}
    tmpl = get_template(template_name)
    generate_pdf_template_object(tmpl, file_object, context)
    return file_object


def render_to_pdf_response(template_name, context=None, pdfname=None):
    buffer = BytesIO()
    generate_pdf(template_name, buffer, context)
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type='application/pdf')
    if not pdfname:
        pdfname = '%s.pdf' % os.path.splitext(os.path.basename(template_name))[0]
    response['Content-Disposition'] = 'attachment; filename=%s' % pdfname
    return response
