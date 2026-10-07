"""App smoke tests: login, seed, project list."""
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings


@override_settings(ALLOWED_HOSTS=['*'], HTML_MINIFY=False)
class SmokeTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser('smokeadmin', 'smoke@example.com', 'smokeadmin')
        self.client = Client()

    def test_login_page(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log in')

    def test_login_succeeds(self):
        logged_in = self.client.login(username='smokeadmin', password='smokeadmin')
        self.assertTrue(logged_in)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_seed_and_project_list(self):
        assert self.client.login(username='smokeadmin', password='smokeadmin')
        response = self.client.get('/seed', follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/project/')
        self.assertEqual(response.status_code, 200)
        # Seeded sample project is named "Movie"
        self.assertContains(response, 'Movie')

    def test_new_project_form_loads(self):
        """GET /project/0 must not 500 on unsaved Project related filters."""
        assert self.client.login(username='smokeadmin', password='smokeadmin')
        response = self.client.get('/project/0')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'btn_save')

    def test_new_project_can_save(self):
        assert self.client.login(username='smokeadmin', password='smokeadmin')
        response = self.client.post('/project/0', {
            'name': 'Fresh Project',
            'owner': self.user.id,
            'users': [],
            'guests': [],
            'btn_save': 'x',
        })
        self.assertEqual(response.status_code, 302)
        from X.models import Project
        project = Project.objects.get(name='Fresh Project')
        self.assertEqual(project.owner_id, self.user.id)
        self.assertEqual(response['Location'], '/project/%s' % project.id)

    def test_empty_script_new_scene_form(self):
        """GET /script/0/<order> must render the new-scene form (not 404 on /script/0/None)."""
        from X.models import Project, Script
        assert self.client.login(username='smokeadmin', password='smokeadmin')
        project = Project.objects.create(name='Empty Script Proj', owner=self.user)
        script = Script.objects.create(name='Empty Script', project=project)
        session = self.client.session
        session['ProjectID'] = project.id
        session['ScriptID'] = script.id
        session.save()

        response = self.client.get('/script/0/65536')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'btn_save')
        # Prefill + banner so New is visibly actionable
        self.assertContains(response, 'New Scene')
        self.assertContains(response, 'New scene')
        # Unsaved new-scene form must not emit /script/new/None/…
        self.assertNotContains(response, '/script/new/None/')
        self.assertContains(response, 'href="/script/0/65536"')

        # Save creates the scene and redirects to its edit URL
        response = self.client.post('/script/0/65536', {
            'name': 'INT. SAVED FROM NEW - DAY',
            'abstract': '',
            'short': '',
            'description': '',
            'indentation': 0,
            'color': '#FFFFFF',
            'duration': 0,
            'progress_script': 0,
            'progress_pre': 0,
            'progress_shot': 0,
            'progress_post': 0,
            'tag1': True,
            'tag2': True,
            'tag3': True,
            'tag4': True,
            'tag5': True,
            'btn_save': 'x',
        })
        self.assertEqual(response.status_code, 302)
        from X.models import Scene
        scene = Scene.objects.get(script=script, name='INT. SAVED FROM NEW - DAY')
        self.assertEqual(response['Location'], '/script/%s' % scene.id)

        # New relative to first scene must not redirect to /script/0/None
        from X.common import ORDER_STEP, getOrderNumber
        self.assertIsNotNone(getOrderNumber([scene], scene.id, 1))
        self.assertNotEqual(str(getOrderNumber([scene], scene.id, 1)), 'None')
        response = self.client.get('/script/new/%s/1' % scene.id)
        self.assertEqual(response.status_code, 302)
        self.assertRegex(response['Location'], r'^/script/0/\d+$')
        self.assertNotIn('None', response['Location'])

        # Scoped new-scene URL must resolve
        response = self.client.get('/p/%s/s/%s/script/0/65536' % (project.id, script.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'btn_save')

"""
Tests for writer import (F4), breakdown (F5), role bible (F6), revisions (F7).
"""
from django.contrib.auth.models import User
from django.test import Client, TestCase

from X.common import Env
from X.importer import ImporterBase, detect_format
from X.models import Gadget, Project, Role, Scene, SceneItem, Script, ScriptRevision, SFX
from X.view_scene import apply_breakdown


FOUNTAIN_SAMPLE = """Title: Sample Short
Author: Test

INT. KITCHEN - DAY

Sunlight hits a cracked mug on the counter.

JULES
(whispering)
Did you hear that?

A sudden BANG echoes from the hallway.

EXT. ALLEY - NIGHT

JULES runs past a dumpster.
"""

FDX_SAMPLE = """<?xml version="1.0" encoding="UTF-8"?>
<FinalDraft DocumentType="Script" Version="1">
  <Content>
    <Paragraph Type="Scene Heading"><Text>INT. LAB - NIGHT</Text></Paragraph>
    <Paragraph Type="Action"><Text>Beakers bubble.</Text></Paragraph>
    <Paragraph Type="Character"><Text>ADA</Text></Paragraph>
    <Paragraph Type="Parenthetical"><Text>excited</Text></Paragraph>
    <Paragraph Type="Dialogue"><Text>It works!</Text></Paragraph>
  </Content>
</FinalDraft>
"""

PLAIN_SAMPLE = """INT. OFFICE - DAY

The clock ticks.

BOSS
Get me that report.

INT. HALLWAY - CONTINUOUS

Footsteps fade.
"""


class WriterFeatureTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('writer', password='pass')
        self.project = Project.objects.create(name='Test Project', owner=self.user)
        from X.access import ROLE_PRODUCER, ensure_membership
        ensure_membership(self.project, self.user, ROLE_PRODUCER)
        self.client = Client()
        self.client.login(username='writer', password='pass')
        session = self.client.session
        session['ProjectID'] = self.project.id
        session.save()

    def _env(self):
        request = type('R', (), {})()
        request.user = self.user
        request.session = {'ProjectID': self.project.id, 'ScriptID': 0, 'SceneID': 0}

        class FakeRequest:
            def __init__(self, user, project_id):
                self.user = user
                self.session = {'ProjectID': project_id, 'ScriptID': 0, 'SceneID': 0}

        return Env(FakeRequest(self.user, self.project.id))


class DetectFormatTests(TestCase):
    def test_detect_fountain_extension(self):
        self.assertEqual(detect_format('a.fountain', b'Title: X\n'), 'fountain')

    def test_detect_fdx_content(self):
        self.assertEqual(detect_format('script.xml', FDX_SAMPLE.encode()), 'fdx')

    def test_detect_celtx_zip_magic(self):
        self.assertEqual(detect_format('x.celtx', b'PK\x03\x04rest'), 'celtx')


class FountainImportTests(WriterFeatureTestCase):
    def test_fountain_import_creates_scenes_and_dialogue(self):
        env = self._env()
        imp = ImporterBase(env)
        script = imp.doImport('sample.fountain', data=FOUNTAIN_SAMPLE.encode('utf-8'), fmt='fountain')
        scenes = list(Scene.objects.filter(script=script).order_by('order'))
        self.assertGreaterEqual(len(scenes), 2)
        self.assertTrue(any('KITCHEN' in s.name.upper() for s in scenes))
        items = SceneItem.objects.filter(scene__script=script)
        self.assertTrue(items.filter(type='D', role__name__iexact='JULES').exists())
        self.assertTrue(items.filter(type='A').exists())
        self.assertTrue(Role.objects.filter(project=self.project, name__iexact='JULES').exists())


class FDXImportTests(WriterFeatureTestCase):
    def test_fdx_import(self):
        env = self._env()
        imp = ImporterBase(env)
        script = imp.doImport('sample.fdx', data=FDX_SAMPLE.encode('utf-8'), fmt='fdx')
        scenes = Scene.objects.filter(script=script)
        self.assertEqual(scenes.count(), 1)
        self.assertIn('LAB', scenes.first().name.upper())
        dialog = SceneItem.objects.get(scene__script=script, type='D')
        self.assertEqual(dialog.role.name.upper(), 'ADA')
        self.assertIn('works', dialog.text.lower())
        self.assertEqual(dialog.parenthetical, 'excited')


class PlainImportTests(WriterFeatureTestCase):
    def test_plain_text_import(self):
        env = self._env()
        imp = ImporterBase(env)
        script = imp.doImport('sample.txt', data=PLAIN_SAMPLE.encode('utf-8'), fmt='plain')
        self.assertGreaterEqual(Scene.objects.filter(script=script).count(), 2)
        self.assertTrue(
            SceneItem.objects.filter(scene__script=script, type='D', role__name__iexact='BOSS').exists()
        )


class ImportUploadViewTests(WriterFeatureTestCase):
    def test_import_page_renders(self):
        response = self.client.get('/project/%s/import' % self.project.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fountain')
        self.assertContains(response, 'Final Draft')
        self.assertContains(response, 'Celtx')

    def test_upload_fountain(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        upload = SimpleUploadedFile('demo.fountain', FOUNTAIN_SAMPLE.encode('utf-8'))
        response = self.client.post(
            '/project/%s/import' % self.project.id,
            {'script_file': upload, 'format': 'fountain', 'script_name': 'Demo Script'},
        )
        self.assertEqual(response.status_code, 302)
        script = Script.objects.get(project=self.project, name='Demo Script')
        self.assertGreaterEqual(Scene.objects.filter(script=script).count(), 2)


class BreakdownTests(WriterFeatureTestCase):
    def setUp(self):
        super().setUp()
        self.script = Script.objects.create(name='S', project=self.project)
        self.scene = Scene.objects.create(
            name='INT. ROOM', project=self.project, script=self.script, order=1
        )
        self.scene.setAllTags(True)
        self.scene.save()

    def test_break_to_prop(self):
        item = SceneItem.objects.create(
            scene=self.scene, type='A', order=1, text='She grabs the RED KEY.'
        )
        env = self._env()
        env.setScript(self.script)
        env.setScene(self.scene)
        gadget = apply_breakdown(env, item, 'prop')
        item.refresh_from_db()
        self.assertEqual(item.gadget_id, gadget.id)
        self.assertIn(gadget, self.scene.gadgets.all())

    def test_break_to_sfx(self):
        item = SceneItem.objects.create(
            scene=self.scene, type='A', order=2, text='A thunderclap shakes the walls.'
        )
        env = self._env()
        sfx = apply_breakdown(env, item, 'sfx')
        item.refresh_from_db()
        self.assertEqual(item.sfx_id, sfx.id)
        self.assertIn(sfx, self.scene.sfxs.all())

    def test_break_to_role(self):
        item = SceneItem.objects.create(
            scene=self.scene, type='A', order=3, text='MARA'
        )
        env = self._env()
        role = apply_breakdown(env, item, 'role')
        item.refresh_from_db()
        self.assertEqual(item.role_id, role.id)
        self.assertEqual(item.type, 'R')


class RoleBibleTests(WriterFeatureTestCase):
    def test_bible_page(self):
        person = __import__('X.models', fromlist=['Person']).Person.objects.create(
            name='Actor One', project=self.project
        )
        role = Role.objects.create(
            name='Hero',
            project=self.project,
            actor=person,
            wardrobe='Leather jacket',
            arc_notes='Starts cynical, ends hopeful.',
        )
        response = self.client.get('/role/bible')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hero')
        self.assertContains(response, 'Actor One')
        self.assertContains(response, 'Leather jacket')
        self.assertContains(response, 'cynical')


class RevisionTests(WriterFeatureTestCase):
    def test_stamp_revision(self):
        script = Script.objects.create(
            name='Draft',
            project=self.project,
            revision_label='Blue',
            revision_color='#ADD8E6',
        )
        response = self.client.post(
            '/project/%s/%s' % (self.project.id, script.id),
            {
                'name': script.name,
                'abstract': '',
                'description': '',
                'author': '',
                'version': '',
                'copyright': '',
                'revision_label': 'Blue',
                'revision_color': '#ADD8E6',
                'revision_notes': 'Camera dept notes',
                'btn_stamp_revision': 'x',
            },
        )
        self.assertEqual(response.status_code, 302)
        rev = ScriptRevision.objects.get(script=script)
        self.assertEqual(rev.label, 'Blue')
        self.assertEqual(rev.notes, 'Camera dept notes')

    def test_revision_preset(self):
        script = Script.objects.create(name='Draft2', project=self.project)
        response = self.client.post(
            '/project/%s/%s' % (self.project.id, script.id),
            {
                'name': script.name,
                'abstract': '',
                'description': '',
                'author': '',
                'version': '',
                'copyright': '',
                'revision_label': 'White',
                'revision_color': '#FFFFFF',
                'btn_revision_preset': '#FFC0CB',
            },
        )
        self.assertEqual(response.status_code, 302)
        script.refresh_from_db()
        self.assertEqual(script.revision_label, 'Pink')
        self.assertEqual(script.revision_color.lower(), '#ffc0cb')
