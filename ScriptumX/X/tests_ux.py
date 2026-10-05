"""UX P2 tests: checklist, presence, language, theme."""
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from X.models import Project, Scene, Script
from X.ux import THEME_COOKIE, presence_heartbeat, project_has_multi_users


@override_settings(ALLOWED_HOSTS=['*'], HTML_MINIFY=False, LANGUAGE_CODE='en')
class UxPolishTests(TestCase):
    def setUp(self):
        cache.clear()
        User = get_user_model()
        self.owner = User.objects.create_user('owner', 'owner@example.com', 'ownerpass')
        self.collab = User.objects.create_user('collab', 'collab@example.com', 'collabpass')
        self.solo = User.objects.create_user('solo', 'solo@example.com', 'solopass')

        self.project = Project.objects.create(name='UX Proj', owner=self.owner)
        self.project.users.add(self.owner, self.collab)
        self.script = Script.objects.create(name='UX Script', project=self.project)
        self.scene = Scene.objects.create(
            name='Opening',
            short='1A',
            project=self.project,
            script=self.script,
            order=65536,
            progress_shot=0,
        )

        self.client = Client()
        assert self.client.login(username='owner', password='ownerpass')
        session = self.client.session
        session['ProjectID'] = self.project.id
        session['ScriptID'] = self.script.id
        session['SceneID'] = self.scene.id
        session.save()

    def test_project_has_multi_users(self):
        self.assertTrue(project_has_multi_users(self.project))
        solo_project = Project.objects.create(name='Solo', owner=self.solo)
        solo_project.users.add(self.solo)
        self.assertFalse(project_has_multi_users(solo_project))

    def test_shot_checklist_page(self):
        response = self.client.get('/shot/checklist')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Opening')
        self.assertContains(response, 'ux-shot-checklist')
        self.assertContains(response, '/shot/checklist/%s/progress' % self.scene.id)

    def test_shot_checklist_progress_cycles(self):
        url = '/shot/checklist/%s/progress' % self.scene.id
        r1 = self.client.post(url, content_type='application/json', data='{}')
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r1.json()['progress_shot'], 50)
        self.scene.refresh_from_db()
        self.assertEqual(self.scene.progress_shot, 50)

        r2 = self.client.post(url, content_type='application/json', data='{}')
        self.assertEqual(r2.json()['progress_shot'], 100)
        self.assertTrue(r2.json()['done'])

        r3 = self.client.post(url, content_type='application/json', data='{}')
        self.assertEqual(r3.json()['progress_shot'], 0)

    def test_presence_disabled_for_single_user_project(self):
        solo_project = Project.objects.create(name='Solo2', owner=self.solo)
        solo_project.users.add(self.solo)
        c = Client()
        assert c.login(username='solo', password='solopass')
        session = c.session
        session['ProjectID'] = solo_project.id
        session.save()
        response = c.post(
            '/ux/presence',
            data='{"label":"editing"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['enabled'])

    def test_presence_shows_other_user(self):
        presence_heartbeat(
            self.project,
            self.collab,
            label='editing Scene 1A',
            scene_id=self.scene.id,
            path='/scene/',
        )
        response = self.client.post(
            '/ux/presence',
            data='{"label":"editing Scene 1A","scene_id":%s}' % self.scene.id,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['enabled'])
        usernames = [o['username'] for o in data['others']]
        self.assertIn('collab', usernames)

    def test_language_toggle_sets_cookie(self):
        response = self.client.post('/ux/language', {'language': 'de', 'next': '/shot/checklist'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.cookies['django_language'].value, 'de')

    def test_theme_toggle_sets_cookie(self):
        response = self.client.post('/ux/theme', {'theme': 'dark', 'next': '/script'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.cookies[THEME_COOKIE].value, 'dark')

    def test_layout_includes_ux_chrome(self):
        response = self.client.get('/shot/checklist')
        self.assertContains(response, 'ux-theme-toggle')
        self.assertContains(response, 'ux-keyboard.js')
        self.assertContains(response, 'ux-stage.css')
        self.assertContains(response, 'name="language"')
