"""Tests for F1/F2/F3 data-safety features."""
import json
import zipfile
from io import BytesIO

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings

from X.backup import dumps_project, export_project, load_backup_bytes, restore_project, zip_project
from X.conflict import is_stale, token_for
from X.models import Project, Scene, SceneItem, Script


@override_settings(ALLOWED_HOSTS=['*'], HTML_MINIFY=False)
class DataSafetyTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('safety', 'safety@example.com', 'safety')
        self.client = Client()
        assert self.client.login(username='safety', password='safety')

        self.project = Project.objects.create(name='Safety Project', owner=self.user)
        self.script = Script.objects.create(name='Safety Script', project=self.project)
        session = self.client.session
        session['ProjectID'] = self.project.id
        session['ScriptID'] = self.script.id
        session.save()

        self.scene_a = Scene.objects.create(
            name='Scene A', project=self.project, script=self.script, order=65536
        )
        self.scene_a.setAllTags(True)
        self.scene_a.save()
        self.scene_b = Scene.objects.create(
            name='Scene B', project=self.project, script=self.script, order=131072
        )
        self.scene_b.setAllTags(True)
        self.scene_b.save()
        self.scene_c = Scene.objects.create(
            name='Scene C', project=self.project, script=self.script, order=196608
        )
        self.scene_c.setAllTags(True)
        self.scene_c.save()

        session = self.client.session
        session['SceneID'] = self.scene_b.id
        session.save()

        self.item_a = SceneItem.objects.create(scene=self.scene_b, type='A', text='Action A', order=65536)
        self.item_b = SceneItem.objects.create(scene=self.scene_b, type='A', text='Action B', order=131072)
        self.item_c = SceneItem.objects.create(scene=self.scene_b, type='D', text='Dialog C', order=196608)

    def test_script_move_get_is_noop(self):
        before = self.scene_b.order
        response = self.client.get(f'/script/move/{self.scene_b.id}/-1')
        self.assertEqual(response.status_code, 302)
        self.scene_b.refresh_from_db()
        self.assertEqual(self.scene_b.order, before)

    def test_script_move_post_and_undo(self):
        old_orders = {
            self.scene_a.id: self.scene_a.order,
            self.scene_b.id: self.scene_b.order,
            self.scene_c.id: self.scene_c.order,
        }
        response = self.client.post(f'/script/move/{self.scene_b.id}/1')
        self.assertEqual(response.status_code, 302)
        self.scene_b.refresh_from_db()
        self.assertNotEqual(self.scene_b.order, old_orders[self.scene_b.id])

        response = self.client.post('/script/undo-move')
        self.assertEqual(response.status_code, 302)
        for scene in (self.scene_a, self.scene_b, self.scene_c):
            scene.refresh_from_db()
            self.assertEqual(scene.order, old_orders[scene.id])

    def test_sceneitem_move_post_and_undo(self):
        old_orders = {
            self.item_a.id: self.item_a.order,
            self.item_b.id: self.item_b.order,
            self.item_c.id: self.item_c.order,
        }
        response = self.client.post(f'/scene/move/{self.item_b.id}/-1')
        self.assertEqual(response.status_code, 302)
        self.item_b.refresh_from_db()
        self.assertNotEqual(self.item_b.order, old_orders[self.item_b.id])

        response = self.client.post('/scene/undo-move')
        self.assertEqual(response.status_code, 302)
        for item in (self.item_a, self.item_b, self.item_c):
            item.refresh_from_db()
            self.assertEqual(item.order, old_orders[item.id])

    def test_scene_autosave_and_conflict(self):
        self.scene_b.refresh_from_db()
        token = token_for(self.scene_b)
        response = self.client.post(f'/script/autosave/{self.scene_b.id}', {
            'name': 'Scene B renamed',
            'abstract': '',
            'short': '',
            'description': 'autosaved',
            'indentation': 0,
            'color': '#FFFFFF',
            'progress_script': 0,
            'progress_pre': 0,
            'progress_shot': 0,
            'progress_post': 0,
            'expected_updated_at': token,
            'tag1': 'on',
            'tag2': 'on',
            'tag3': 'on',
            'tag4': 'on',
            'tag5': 'on',
        })
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['status'], 'ok')
        self.scene_b.refresh_from_db()
        self.assertEqual(self.scene_b.name, 'Scene B renamed')
        self.assertTrue(payload['updated_at'])

        # Stale token must conflict
        response = self.client.post(f'/script/autosave/{self.scene_b.id}', {
            'name': 'Should fail',
            'abstract': '',
            'short': '',
            'description': 'conflict',
            'indentation': 0,
            'color': '#FFFFFF',
            'progress_script': 0,
            'progress_pre': 0,
            'progress_shot': 0,
            'progress_post': 0,
            'expected_updated_at': token,
            'tag1': 'on',
            'tag2': 'on',
            'tag3': 'on',
            'tag4': 'on',
            'tag5': 'on',
        })
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()['status'], 'conflict')

    def test_sceneitem_autosave(self):
        self.item_b.refresh_from_db()
        token = token_for(self.item_b)
        response = self.client.post(f'/scene/autosave/{self.item_b.id}', {
            'text': 'Action B autosaved',
            'parenthetical': '',
            'expected_updated_at': token,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')
        self.item_b.refresh_from_db()
        self.assertEqual(self.item_b.text, 'Action B autosaved')

    def test_conflict_helper(self):
        self.scene_a.refresh_from_db()
        token = token_for(self.scene_a)
        self.assertFalse(is_stale(self.scene_a, token))
        self.assertTrue(is_stale(self.scene_a, '2000-01-01T00:00:00+00:00'))

    def test_project_export_json_and_zip(self):
        response = self.client.get(f'/project/{self.project.id}/export.json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['format'], 'scriptumx-backup')
        self.assertEqual(data['project']['name'], 'Safety Project')
        self.assertEqual(len(data['scripts']), 1)
        self.assertEqual(len(data['scripts'][0]['scenes']), 3)

        response = self.client.get(f'/project/{self.project.id}/export.zip')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/zip')
        self.assertTrue(response.content[:2] == b'PK')

    def test_project_restore_from_json(self):
        raw = dumps_project(self.project).encode('utf-8')
        response = self.client.post('/project/restore', {
            'backup_file': self._upload('backup.json', raw),
        })
        self.assertEqual(response.status_code, 302)
        restored = Project.objects.exclude(pk=self.project.id).latest('id')
        self.assertIn('restored', restored.name.lower())
        self.assertEqual(Script.objects.filter(project=restored).count(), 1)
        self.assertEqual(Scene.objects.filter(project=restored).count(), 3)
        restored_scene = Scene.objects.filter(project=restored, name='Scene B').first()
        self.assertIsNotNone(restored_scene)
        self.assertEqual(SceneItem.objects.filter(scene=restored_scene).count(), 3)

    def test_project_restore_from_zip(self):
        zipped = zip_project(self.project)
        response = self.client.post('/project/restore', {
            'backup_file': self._upload('backup.zip', zipped),
        })
        self.assertEqual(response.status_code, 302)
        self.assertGreaterEqual(Project.objects.filter(owner=self.user).count(), 2)

    def test_backup_roundtrip_helpers(self):
        data = export_project(self.project)
        raw = json.dumps(data).encode('utf-8')
        loaded = load_backup_bytes(raw, filename='x.json')
        project = restore_project(loaded, owner=self.user, name_suffix=' (copy)')
        self.assertTrue(project.name.endswith('(copy)'))

    def _upload(self, name, content):
        from django.core.files.uploadedfile import SimpleUploadedFile
        return SimpleUploadedFile(name, content)
