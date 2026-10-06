"""PDF export tests — fonts, script/L/M PDFs, error UI, optional Playwright."""
from unittest import skipUnless
from unittest.mock import patch

from django.test import Client, TestCase, override_settings
from django.contrib.auth import get_user_model

from X.models import Project, Script, Scene, SceneItem, Role
from report.pdf_fonts import (
    bundled_font_paths,
    resolve_pdf_font_family,
    pdf_font_face_css,
)
from report.pdf_utils import PdfGenerationError, prepare_pdf_context


def _pdf_text(content: bytes) -> str:
    from io import BytesIO
    from pypdf import PdfReader
    reader = PdfReader(BytesIO(content))
    return '\n'.join((page.extract_text() or '') for page in reader.pages)


def _seed_minimal(user):
    """Deterministic project/script/scene for PDF tests (avoids flaky /seed Markov)."""
    project = Project.objects.create(name='Movie', owner=user)
    script = Script.objects.create(name='Long Story - Short', project=project)
    role = Role.objects.create(name='Elizabeth', project=project, color='#ffcccc')
    scene = Scene.objects.create(
        name='OPENING', short='1', project=project, script=script, order=65536,
    )
    SceneItem.objects.create(
        scene=scene, type='A', text='A carriage arrives.', order=65536,
    )
    SceneItem.objects.create(
        scene=scene, type='D', role=role,
        text='Good evening.', order=131072,
    )
    return project, script, scene


def _login_with_project(client, username, password, user):
    assert client.login(username=username, password=password)
    project, script, scene = _seed_minimal(user)
    session = client.session
    session['ProjectID'] = project.id
    session['ScriptID'] = script.id
    session['SceneID'] = scene.id
    session.save()
    return project, script, scene


@override_settings(ALLOWED_HOSTS=['*'], HTML_MINIFY=False)
class PdfFontMappingTests(TestCase):
    def test_bundled_fonts_exist(self):
        paths = bundled_font_paths()
        self.assertGreaterEqual(len(paths), 6)
        for path in paths:
            self.assertTrue(path.endswith('.ttf'), path)
            import os
            self.assertTrue(os.path.isfile(path), 'missing %s' % path)

    def test_google_open_sans_maps_to_dejavu_sans(self):
        self.assertEqual(
            resolve_pdf_font_family('"Open Sans", sans-serif', 'Open+Sans:400,700'),
            'DejaVu Sans',
        )

    def test_source_code_maps_to_mono(self):
        self.assertEqual(
            resolve_pdf_font_family('"Source Code Pro"', 'Source+Code+Pro:400'),
            'DejaVu Sans Mono',
        )

    def test_times_maps_to_serif(self):
        self.assertEqual(
            resolve_pdf_font_family('"Times New Roman", Times, serif', ''),
            'DejaVu Serif',
        )

    def test_font_face_css_references_static_ttfs(self):
        css = pdf_font_face_css('/static/')
        self.assertIn('DejaVu Sans', css)
        self.assertIn('DejaVuSans.ttf', css)
        self.assertIn('report/static/report/fonts', css.replace('\\', '/'))

    def test_prepare_pdf_context_sets_embedded_font(self):
        ctx = prepare_pdf_context(
            {'title': 'T', 'font': 'Arial, Helvetica, sans-serif', 'google_link': ''},
        )
        self.assertTrue(ctx['PDF'])
        self.assertIn('DejaVu Sans', ctx['font'])
        self.assertIn('@font-face', ctx['pdf_font_face_css'])
        self.assertEqual(ctx['brand_name'], 'ScriptumX')


@override_settings(ALLOWED_HOSTS=['*'], HTML_MINIFY=False)
class ScriptPdfExportTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser('pdfadmin', 'pdf@example.com', 'pdfadmin')
        self.client = Client()
        _login_with_project(self.client, 'pdfadmin', 'pdfadmin', self.user)

    def test_script_pdf_post_returns_pdf(self):
        response = self.client.post('/report/S/readpdf/', {
            'show_notes': 'on',
            'layout': 'legacy|"Courier New", Courier, monospace|',
            'pdf': 'Download PDF',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.content.startswith(b'%PDF'))
        self.assertGreater(len(response.content), 1000)

    def test_script_read_pdf_button_returns_pdf(self):
        response = self.client.post('/report/S/read/', {
            'show_notes': 'on',
            'show_links': 'on',
            'layout': 'modern|Arial, Helvetica, sans-serif|',
            'pdf': 'Download PDF',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.content.startswith(b'%PDF'))

    def test_google_font_layout_embeds_and_returns_pdf(self):
        response = self.client.post('/report/S/read/', {
            'show_notes': 'on',
            'show_links': 'on',
            'layout': 'modern|"Open Sans", sans-serif|Open+Sans:400,700,400italic,700italic',
            'pdf': 'Download PDF',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.content.startswith(b'%PDF'))
        text = _pdf_text(response.content)
        upper = text.upper()
        # Call-sheet header (F8) + ASCII brand (H8 tofu fix)
        self.assertIn('PROJECT', upper)
        self.assertIn('UNIT', upper)
        self.assertIn('CONTINUITY', upper)
        self.assertIn('SCRIPTUMX', upper)
        self.assertIn('MOVIE', upper)

    def test_pdf_error_surfaces_flash_message(self):
        with patch(
            'report.view_S.render_to_pdf_response',
            side_effect=PdfGenerationError('boom'),
        ):
            response = self.client.post('/report/S/readpdf/', {
                'show_notes': 'on',
                'layout': 'legacy|"Courier New", Courier, monospace|',
                'pdf': 'Download PDF',
            })
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.get('Content-Type', ''), 'application/pdf')
        self.assertContains(response, 'PDF export failed')
        self.assertContains(response, 'Download PDF')


@override_settings(ALLOWED_HOSTS=['*'], HTML_MINIFY=False)
class ListAndMatrixPdfExportTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser('pdfadmin2', 'pdf2@example.com', 'pdfadmin2')
        self.client = Client()
        _login_with_project(self.client, 'pdfadmin2', 'pdfadmin2', self.user)

    def test_role_list_pdf(self):
        response = self.client.post('/report/L/simple_role', {
            'show_notes': 'on',
            'tag1': 'on',
            'tag2': 'on',
            'tag3': 'on',
            'tag4': 'on',
            'tag5': 'on',
            'pdf': 'Download PDF',
        })
        self.assertEqual(response.status_code, 200, response.content[:500])
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.content.startswith(b'%PDF'))
        self.assertGreater(len(response.content), 500)

    def test_scene_role_matrix_pdf(self):
        response = self.client.post('/report/M/scene_role', {
            'show_notes': 'on',
            'tag1': 'on',
            'tag2': 'on',
            'tag3': 'on',
            'tag4': 'on',
            'tag5': 'on',
            'pdf': 'Download PDF',
        })
        self.assertEqual(response.status_code, 200, response.content[:500])
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.content.startswith(b'%PDF'))


try:
    from playwright.sync_api import sync_playwright  # noqa: F401
    HAS_PLAYWRIGHT = True
except Exception:
    HAS_PLAYWRIGHT = False


@skipUnless(HAS_PLAYWRIGHT, 'playwright not installed')
@override_settings(ALLOWED_HOSTS=['*'], HTML_MINIFY=False)
class ScriptPdfPlaywrightSmoke(TestCase):
    """Optional UI smoke (H11): Download PDF form when Playwright is available."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser('pwadmin', 'pw@example.com', 'pwadmin')
        self.client = Client()
        _login_with_project(self.client, 'pwadmin', 'pwadmin', self.user)

    def test_download_pdf_button_present_and_posts(self):
        # Form page smoke via Django client (full browser click needs chromium).
        response = self.client.get('/report/S/readpdf/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Download PDF')
        self.assertContains(response, 'name="pdf"')


@override_settings(ALLOWED_HOSTS=['*'], HTML_MINIFY=False)
class ReportListAndMatrixTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser('reportadmin', 'report@example.com', 'reportadmin')
        self.client = Client()
        assert self.client.login(username='reportadmin', password='reportadmin')
        response = self.client.get('/seed', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_l_report_simple_role(self):
        response = self.client.get('/report/L/simple_role')
        self.assertEqual(response.status_code, 200)

    def test_m_report_scene_role(self):
        response = self.client.get('/report/M/scene_role')
        self.assertEqual(response.status_code, 200)
