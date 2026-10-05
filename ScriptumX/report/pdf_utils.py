# -*- coding: utf-8 -*-
"""HTML → PDF helpers using xhtml2pdf."""
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import logging
import os

logger = logging.getLogger(__name__)


class UnsupportedMediaPathException(Exception):
    pass


class PdfGenerationError(Exception):
    pass


def fetch_resources(uri, rel):
    """
    Callback so xhtml2pdf/reportlab can resolve Images/Stylesheets.
    Local STATIC/MEDIA paths are mapped to filesystem paths. Remote http(s)
    URIs are ignored (return None) so PDF generation does not hard-fail on
    CDN fonts/CSS that are already excluded when PDF=True in templates.
    """
    if not uri:
        return None

    if uri.startswith(('http://', 'https://', 'data:')):
        return None

    static_url = settings.STATIC_URL or '/static/'
    media_url = settings.MEDIA_URL or ''

    if media_url and uri.startswith(media_url):
        path = os.path.join(settings.MEDIA_ROOT or '', uri.replace(media_url, '', 1))
        return path if os.path.exists(path) else None

    if uri.startswith(static_url):
        rel_path = uri.replace(static_url, '', 1)
        candidates = []
        if settings.STATIC_ROOT:
            candidates.append(os.path.join(settings.STATIC_ROOT, rel_path))
        project_root = getattr(settings, 'PROJECT_ROOT', None)
        if project_root:
            candidates.append(os.path.join(project_root, 'X', 'static', rel_path))
            candidates.append(os.path.join(project_root, 'report', 'static', rel_path))
            candidates.append(os.path.join(project_root, 'web', 'static', rel_path))
        for candidate in candidates:
            if candidate and os.path.exists(candidate):
                return candidate
        return None

    logger.warning('pdf fetch_resources: unresolved uri=%r', uri)
    return None


def generate_pdf_template_object(template_object, file_object, context):
    html = template_object.render(context)
    # Strip UTF-8 BOM that some templates/editors inject; it shows as tofu in PDF.
    if isinstance(html, str) and html.startswith('\ufeff'):
        html = html.lstrip('\ufeff')
    result = pisa.CreatePDF(
        html,
        dest=file_object,
        encoding='UTF-8',
        link_callback=fetch_resources,
    )
    if result.err:
        raise PdfGenerationError('xhtml2pdf reported %s error(s)' % result.err)
    return file_object


def generate_pdf(template_name, file_object=None, context=None):
    if not file_object:
        file_object = BytesIO()
    if not context:
        context = {}
    tmpl = get_template(template_name)
    generate_pdf_template_object(tmpl, file_object, context)
    return file_object


def render_to_pdf_response(template_name, context=None, pdfname=None):
    buffer = BytesIO()
    try:
        generate_pdf(template_name, buffer, context)
    except PdfGenerationError as exc:
        logger.exception('PDF generation failed for %s', template_name)
        return HttpResponseServerError('PDF generation failed: %s' % exc)

    pdf = buffer.getvalue()
    buffer.close()

    if not pdf.startswith(b'%PDF'):
        logger.error('PDF generation produced non-PDF output for %s (%s bytes)', template_name, len(pdf))
        return HttpResponseServerError('PDF generation produced invalid output')

    response = HttpResponse(pdf, content_type='application/pdf')
    if not pdfname:
        pdfname = '%s.pdf' % os.path.splitext(os.path.basename(template_name))[0]
    response['Content-Disposition'] = 'attachment; filename="%s"' % pdfname
    return response
