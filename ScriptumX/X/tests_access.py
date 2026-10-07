"""Tests for ProjectMembership, can(), and role enforcement."""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from X.access import (
    ROLE_ACTOR,
    ROLE_PRODUCER,
    can,
    ensure_membership,
    projects_for_user,
)
from X.common import Env, get_tab_list
from X.models import Project, Script

User = get_user_model()


class MembershipAccessTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        self.producer = User.objects.create_user('producer', 'p@example.com', 'prodpass')
        self.actor = User.objects.create_user('actor', 'a@example.com', 'actorpass')
        self.outsider = User.objects.create_user('outsider', 'o@example.com', 'outpass')
        self.project = Project.objects.create(name='Access Film', owner=self.producer)
        ensure_membership(self.project, self.producer, ROLE_PRODUCER)
        ensure_membership(self.project, self.actor, ROLE_ACTOR)
        self.other = Project.objects.create(name='Other Film', owner=self.admin)
        ensure_membership(self.other, self.admin, ROLE_PRODUCER)
        self.script = Script.objects.create(project=self.project, name='Main')

    def test_actor_tabs_script_scene_only(self):
        client = Client()
        assert client.login(username='actor', password='actorpass')
        session = client.session
        session['ProjectID'] = self.project.id
        session['ScriptID'] = self.script.id
        session.save()
        request = client.get('/script/').wsgi_request
        # Rebuild env via a request with session
        from django.test import RequestFactory
        rf = RequestFactory()
        req = rf.get('/script/')
        req.user = self.actor
        req.session = client.session
        env = Env(req, project_id=self.project.id, script_id=self.script.id)
        tabs = get_tab_list(env)
        ids = {t['id'] for t in tabs}
        self.assertEqual(ids, {'C', 'S'})
        self.assertTrue(can(self.actor, self.project, 'script', write=False))
        self.assertFalse(can(self.actor, self.project, 'script', write=True))
        self.assertFalse(can(self.actor, self.project, 'person', write=False))
        self.assertFalse(can(self.actor, self.project, 'plan', write=False))

    def test_actor_can_request_pdf(self):
        client = Client()
        assert client.login(username='actor', password='actorpass')
        session = client.session
        session['ProjectID'] = self.project.id
        session['ScriptID'] = self.script.id
        session.save()
        # Script read → PDF route allowed (GET)
        resp = client.get('/report/S/readpdf/')
        self.assertIn(resp.status_code, (200, 302))
        self.assertNotEqual(resp.status_code, 403)

    def test_actor_403_on_person_and_plan(self):
        client = Client()
        assert client.login(username='actor', password='actorpass')
        session = client.session
        session['ProjectID'] = self.project.id
        session['ScriptID'] = self.script.id
        session.save()
        self.assertEqual(client.get('/person/').status_code, 403)
        self.assertEqual(client.get('/planner/').status_code, 403)

    def test_unassigned_project_hidden_and_direct_url_denied(self):
        client = Client()
        assert client.login(username='outsider', password='outpass')
        resp = client.get('/project/')
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, 'Access Film')
        denied = client.get('/project/%s/' % self.project.id)
        self.assertIn(denied.status_code, (403, 404))

    def test_producer_can_add_actor_not_site_admin(self):
        client = Client()
        assert client.login(username='producer', password='prodpass')
        newbie = User.objects.create_user('newactor', 'n@example.com', 'pass')
        resp = client.post('/access/assign/', {
            'project_id': self.project.id,
            'user_id': newbie.id,
            'role': 'actor',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(
            self.project.memberships.filter(user=newbie, role=ROLE_ACTOR).exists()
        )
        # Cannot grant producer / elevate to site admin via assign
        resp2 = client.post('/access/assign/', {
            'project_id': self.project.id,
            'user_id': newbie.id,
            'role': 'producer',
        })
        self.assertEqual(resp2.status_code, 302)
        m = self.project.memberships.get(user=newbie)
        self.assertNotEqual(m.role, ROLE_PRODUCER)
        newbie.refresh_from_db()
        self.assertFalse(newbie.is_superuser)

    def test_staff_not_all_projects(self):
        staff = User.objects.create_user('staffy', 's@example.com', 'staffpass', is_staff=True)
        self.assertFalse(projects_for_user(staff).filter(pk=self.project.id).exists())
        self.assertFalse(can(staff, self.project, 'script', write=False))
