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
