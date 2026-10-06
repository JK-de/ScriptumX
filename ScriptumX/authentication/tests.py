"""Authentication smoke tests."""
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings


@override_settings(ALLOWED_HOSTS=['*'], HTML_MINIFY=False)
class LoginTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('loginuser', 'login@example.com', 'loginpass')
        self.client = Client()

    def test_login_get(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_login_post(self):
        response = self.client.post('/login/', {
            'username': 'loginuser',
            'password': 'loginpass',
            'next': '/',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].endswith('/') or response.url == '/')
