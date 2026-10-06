# -*- coding: utf-8 -*-
"""HTML → PDF helpers using xhtml2pdf."""
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import logging
import os

from .pdf_fonts import pdf_font_face_css, resolve_pdf_font_family

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
    Absolute paths under PROJECT_ROOT (bundled @font-face TTFs) are returned
    as-is when the file exists.
    """
    if not uri:
        return None

    if uri.startswith(('http://', 'https://', 'data:')):
        return None

    # Absolute filesystem path (bundled PDF fonts)
    if os.path.isabs(uri) and os.path.exists(uri):
        project_root = getattr(settings, 'PROJECT_ROOT', None)
        if project_root:
            try:
                abs_uri = os.path.abspath(uri)
                abs_root = os.path.abspath(project_root)
                if os.path.commonpath([abs_uri, abs_root]) == abs_root:
                    return uri
            except ValueError:
                pass
        else:
            return uri

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


def prepare_pdf_context(context, font_stack=None, google_link=None):
    """
    Enrich a template context for PDF: embed Unicode @font-face CSS and map
    Google/system font choices to DejaVu families (H8/H9).
    """
    ctx = dict(context or {})
    ctx['PDF'] = True
    stack = font_stack if font_stack is not None else ctx.get('font', '')
    g_link = google_link if google_link is not None else ctx.get('google_link', '')
    family = resolve_pdf_font_family(stack or '', g_link or '')
    ctx['font'] = '"%s"' % family
    ctx['pdf_font_family'] = family
    ctx['pdf_font_face_css'] = pdf_font_face_css(settings.STATIC_URL or '/static/')
    # Avoid tofu from Mathematical Script 𝓧 in PDF titles/branding
    ctx['brand_name'] = 'ScriptumX'
    return ctx


def generate_pdf_template_object(template_object, file_object, context):
    html = template_object.render(context)
    # Strip UTF-8 BOM that some templates/editors inject; it shows as tofu in PDF.
    if isinstance(html, str) and html.startswith('\ufeff'):
        html = html.lstrip('\ufeff')
    project_root = getattr(settings, 'PROJECT_ROOT', None)
    result = pisa.CreatePDF(
        html,
        dest=file_object,
        encoding='UTF-8',
        link_callback=fetch_resources,
        path=project_root or os.getcwd(),
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
    """
    Render template to a PDF HttpResponse.
    Raises PdfGenerationError on failure so callers can flash a UI message (H10).
    """
    buffer = BytesIO()
    generate_pdf(template_name, buffer, context)
    pdf = buffer.getvalue()
    buffer.close()

    if not pdf.startswith(b'%PDF'):
        logger.error(
            'PDF generation produced non-PDF output for %s (%s bytes)',
            template_name,
            len(pdf),
        )
        raise PdfGenerationError('PDF generation produced invalid output')

    response = HttpResponse(pdf, content_type='application/pdf')
    if not pdfname:
        pdfname = '%s.pdf' % os.path.splitext(os.path.basename(template_name))[0]
    response['Content-Disposition'] = 'attachment; filename="%s"' % pdfname
    return response


PDF_ERROR_MESSAGE = (
    'PDF export failed. Try another layout, or show the report in the browser and print.'
)


def respond_html_or_pdf(
    request,
    form,
    template_name,
    context,
    *,
    want_pdf,
    pdfname=None,
    form_template=None,
    form_extra=None,
):
    """
    Shared HTML vs PDF response for report views.
    On PDF failure: flash error and re-render the filter form (H10).
    """
    if not want_pdf:
        context = dict(context or {})
        context['PDF'] = False
        return render(request, template_name, context)

    pdf_context = prepare_pdf_context(context)
    try:
        return render_to_pdf_response(template_name, pdf_context, pdfname=pdfname)
    except PdfGenerationError:
        logger.exception('PDF export failed for %s', template_name)
        messages.error(request, PDF_ERROR_MESSAGE)
        form_ctx = {'title': context.get('title', 'Report'), 'form': form}
        if form_extra:
            form_ctx.update(form_extra)
        if form_template:
            return render(request, form_template, form_ctx)
        return render(request, template_name, form_ctx)
