"""PDF export smoke tests."""
from django.test import Client, TestCase, override_settings
from django.contrib.auth import get_user_model


@override_settings(ALLOWED_HOSTS=['*'], HTML_MINIFY=False)
class ScriptPdfExportTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser('pdfadmin', 'pdf@example.com', 'pdfadmin')
        self.client = Client()
        assert self.client.login(username='pdfadmin', password='pdfadmin')
        # Seed sample project/script/scenes (redirects to / when done)
        response = self.client.get('/seed', follow=True)
        self.assertEqual(response.status_code, 200)

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
