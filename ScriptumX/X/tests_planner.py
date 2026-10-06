"""Production planner tests (F9–F12)."""

from datetime import datetime, time, timedelta

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings

from X.models import (
    Appointment,
    Appointment2Scene,
    Location,
    Person,
    Project,
    Role,
    Scene,
    SceneItem,
    Script,
)
from X.planner import (
    build_cast_availability,
    build_dood,
    build_location_groups,
    build_progress_dashboard,
    build_stripboard,
)


@override_settings(ALLOWED_HOSTS=['*'], HTML_MINIFY=False)
class PlannerViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser('planadmin', 'plan@example.com', 'planadmin')
        self.client = Client()
        assert self.client.login(username='planadmin', password='planadmin')

        self.project = Project.objects.create(name='Planner Film', owner=self.user)
        self.project.users.add(self.user)
        self.script = Script.objects.create(project=self.project, name='Main Script')

        session = self.client.session
        session['ProjectID'] = self.project.id
        session['ScriptID'] = self.script.id
        session.save()

        self.loc_int = Location.objects.create(
            project=self.project, name='Kitchen', tag1=True
        )
        self.loc_ext = Location.objects.create(
            project=self.project, name='Street', tag2=True
        )

        self.alice = Person.objects.create(project=self.project, name='Alice Actor')
        self.bob = Person.objects.create(project=self.project, name='Bob Extra')

        self.role_hero = Role.objects.create(
            project=self.project, name='Hero', actor=self.alice, color='#ff0000'
        )
        self.role_extra = Role.objects.create(
            project=self.project, name='Passerby', actor=self.bob, color='#00ff00'
        )

        self.scene1 = Scene.objects.create(
            project=self.project,
            script=self.script,
            name='Hero wakes',
            short='1',
            order=100,
            story_location=self.loc_int,
            progress_script=80,
            progress_pre=40,
            progress_shot=20,
            progress_post=0,
        )
        self.scene2 = Scene.objects.create(
            project=self.project,
            script=self.script,
            name='Street chase',
            short='2',
            order=200,
            story_location=self.loc_ext,
            progress_script=50,
            progress_pre=50,
            progress_shot=50,
            progress_post=50,
        )
        self.scene3 = Scene.objects.create(
            project=self.project,
            script=self.script,
            name='Kitchen again',
            short='3',
            order=300,
            story_location=self.loc_int,
            progress_script=10,
            progress_pre=0,
            progress_shot=0,
            progress_post=0,
        )

        SceneItem.objects.create(
            scene=self.scene1, type='D', text='Hello', role=self.role_hero, order=1
        )
        SceneItem.objects.create(
            scene=self.scene2, type='D', text='Run!', role=self.role_hero, order=1
        )
        SceneItem.objects.create(
            scene=self.scene2, type='D', text='Excuse me', role=self.role_extra, order=2
        )
        SceneItem.objects.create(
            scene=self.scene3, type='D', text='Back home', role=self.role_hero, order=1
        )

        day1 = datetime(2026, 6, 1, 8, 0, 0)
        day2 = datetime(2026, 6, 2, 8, 0, 0)

        self.appt1 = Appointment.objects.create(
            project=self.project,
            name='Day 1 INT',
            time_all=day1,
            meeting_point=self.loc_int,
        )
        self.appt1.persons.add(self.alice)  # missing Bob intentionally on day with only hero

        self.appt2 = Appointment.objects.create(
            project=self.project,
            name='Day 2 EXT',
            time_all=day2,
            meeting_point=self.loc_ext,
        )
        self.appt2.persons.add(self.alice)  # Bob needed but missing → cast conflict

        Appointment2Scene.objects.create(
            appointment=self.appt1, scene=self.scene1, time=time(9, 0)
        )
        Appointment2Scene.objects.create(
            appointment=self.appt2, scene=self.scene2, time=time(10, 0)
        )
        # scene3 left unscheduled

    def test_planner_hub_ok(self):
        response = self.client.get('/planner/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Production planner')
        self.assertContains(response, 'Stripboard')

    def test_stripboard_shows_scheduled_and_unscheduled(self):
        response = self.client.get('/planner/stripboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Day 1 INT')
        self.assertContains(response, 'Hero wakes')
        self.assertContains(response, 'Unscheduled')
        self.assertContains(response, 'Kitchen again')

    def test_dood_matrix(self):
        response = self.client.get('/planner/dood/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hero')
        self.assertContains(response, 'SW')  # start work codes present

    def test_cast_conflict_missing_actor(self):
        response = self.client.get('/planner/cast/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bob Extra')
        self.assertContains(response, 'needed')

    def test_location_grouping(self):
        response = self.client.get('/planner/locations/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kitchen')
        self.assertContains(response, 'Street')
        self.assertContains(response, 'INT')
        self.assertContains(response, 'EXT')

    def test_progress_dashboard_averages(self):
        response = self.client.get('/planner/progress/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Progress dashboard')
        self.assertContains(response, 'Main Script')
        # script avg of 80,50,10 = 47
        data = build_progress_dashboard(self.project)
        self.assertEqual(data['scripts'][0]['progress_script'], 47)
        self.assertEqual(data['scripts'][0]['progress_shot'], 23)

    def test_helpers_stripboard_and_dood(self):
        board = build_stripboard(self.project, self.script)
        self.assertEqual(len(board['days']), 2)
        self.assertEqual(len(board['unscheduled']), 1)
        dood = build_dood(self.project, self.script)
        self.assertEqual(dood['day_count'], 2)
        hero_row = next(r for r in dood['rows'] if r['role'].id == self.role_hero.id)
        self.assertEqual(hero_row['cells'], ['SW', 'WF'])
        self.assertEqual(hero_row['work_days'], 2)

    def test_cast_and_location_helpers(self):
        cast = build_cast_availability(self.project, self.script)
        day2 = next(r for r in cast['reports'] if r['day']['appointment'].id == self.appt2.id)
        missing_names = [m['person'].name for m in day2['missing']]
        self.assertIn('Bob Extra', missing_names)

        locs = build_location_groups(self.project, self.script)
        # scene1 INT Kitchen, scene2 EXT Street, scene3 INT Kitchen → 3 suggestion clusters
        self.assertEqual(len(locs['suggestions']), 3)
        self.assertTrue(any(g['ie'] == 'INT' for g in locs['groups']))

    def test_planner_requires_login(self):
        client = Client()
        response = client.get('/planner/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)
