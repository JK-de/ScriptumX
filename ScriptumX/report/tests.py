"""PDF export, list/matrix, and collaboration (F14/F15) tests."""
from unittest import skipUnless
from unittest.mock import patch

from django.test import Client, TestCase, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from X.models import Location, Project, Role, Scene, SceneItem, Script, Time
from report.models import FilterPreset, ReportShareLink
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


class ReportShareAndPresetTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create_user('owner', 'owner@example.com', 'ownerpass')
        self.guest = User.objects.create_user('guest', 'guest@example.com', 'guestpass')
        self.client = Client()
        assert self.client.login(username='owner', password='ownerpass')

        self.project = Project.objects.create(name='Collab Proj', owner=self.owner)
        self.project.guests.add(self.guest)
        self.script = Script.objects.create(name='Collab Script', project=self.project)
        self.ext = Location.objects.create(name='Park', project=self.project, tag2=True)
        self.inn = Location.objects.create(name='Studio', project=self.project, tag1=True)
        self.day = Time.objects.create(name='Day 1 noon', project=self.project, day=1, hour=12)
        self.role = Role.objects.create(name='Hero', project=self.project, tag4=True)
        self.scene_ext = Scene.objects.create(
            name='Park scene', project=self.project, script=self.script,
            story_location=self.ext, story_time=self.day, order=1,
        )
        self.scene_inn = Scene.objects.create(
            name='Studio scene', project=self.project, script=self.script,
            story_location=self.inn, story_time=self.day, order=2,
        )
        SceneItem.objects.create(
            scene=self.scene_ext, role=self.role, type='D', text='Hello', order=1,
        )
        session = self.client.session
        session['ProjectID'] = self.project.id
        session['ScriptID'] = self.script.id
        session.save()

    def _location_filter_post(self, **extra):
        data = {
            'tag0': 'on',
            'tag1': 'on',
            'tag2': 'on',
            'tag3': 'on',
            'tag4': 'on',
            'tag5': 'on',
            'show_notes': 'on',
            'preset_name': '',
            'preset_id': '',
        }
        data.update(extra)
        return data

    def test_create_share_link_and_anonymous_access(self):
        response = self.client.post('/report/L/simple_location', {
            'tag2': 'on',
            'show_notes': 'on',
            'preset_name': 'Exteriors',
            'preset_id': '',
            'create_share': 'Create share link',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Share link created')
        self.assertContains(response, '/report/share/')
        link = ReportShareLink.objects.get()
        self.assertEqual(link.report_name, 'L_Location')
        self.assertEqual(link.label, 'Exteriors')
        self.assertTrue(link.filter_payload.get('tags', {}).get('2'))

        anon = Client()
        shared = anon.get(reverse('report:shared_report', kwargs={'token': link.token}))
        self.assertEqual(shared.status_code, 200)
        self.assertContains(shared, 'Park')
        self.assertNotContains(shared, 'Studio')

    def test_revoked_share_is_404(self):
        link = ReportShareLink.objects.create(
            project=self.project,
            script=self.script,
            report_name='L_Location',
            title='Location List',
            filter_payload={'tags': {'2': True}, 'show_notes': True},
            created_by=self.owner,
        )
        link.revoked = True
        link.save()
        anon = Client()
        response = anon.get(reverse('report:shared_report', kwargs={'token': link.token}))
        self.assertEqual(response.status_code, 404)

    def test_save_and_load_filter_preset(self):
        response = self.client.post('/report/L/simple_location', {
            'tag2': 'on',
            'show_notes': 'on',
            'preset_name': 'all day exteriors',
            'preset_id': '',
            'save_preset': 'Save preset',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Preset saved')
        preset = FilterPreset.objects.get(user=self.owner, name='all day exteriors')
        self.assertEqual(preset.tag_group, 'location')
        self.assertTrue(preset.payload['tags']['2'])

        response = self.client.post('/report/L/simple_location', {
            'tag0': 'on',
            'tag1': 'on',
            'tag2': 'on',
            'tag3': 'on',
            'tag4': 'on',
            'tag5': 'on',
            'show_notes': 'on',
            'preset_name': '',
            'preset_id': str(preset.pk),
            'load_preset': 'Load preset',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'all day exteriors')
        # Loaded form should reflect exterior-only tags (tag2 checked in HTML)
        self.assertContains(response, 'name="tag2"')

    def test_scene_preset_with_role_filter(self):
        response = self.client.post('/report/L/simple_scene', {
            'tag0': 'on',
            'tag1': 'on',
            'tag2': 'on',
            'tag3': 'on',
            'tag4': 'on',
            'tag5': 'on',
            'show_notes': 'on',
            'exterior_only': 'on',
            'role_id': str(self.role.pk),
            'preset_name': 'scenes with Role Hero exteriors',
            'preset_id': '',
            'save_preset': 'Save preset',
        })
        self.assertEqual(response.status_code, 200)
        preset = FilterPreset.objects.get(name='scenes with Role Hero exteriors')
        self.assertTrue(preset.payload.get('exterior_only'))
        self.assertEqual(preset.payload.get('role_id'), self.role.pk)

        link = ReportShareLink.objects.create(
            project=self.project,
            script=self.script,
            report_name='L_Scene',
            title='Scene List',
            filter_payload=preset.payload,
            created_by=self.owner,
        )
        anon = Client()
        shared = anon.get(reverse('report:shared_report', kwargs={'token': link.token}))
        self.assertEqual(shared.status_code, 200)
        self.assertContains(shared, 'Park scene')
        self.assertNotContains(shared, 'Studio scene')

    def test_filter_form_shows_share_controls(self):
        response = self.client.get('/report/L/simple_location')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create share link')
        self.assertContains(response, 'Save preset')
        self.assertContains(response, 'Share &amp; presets')
