from django.test import TestCase
from django.urls import reverse


class AuthTests(TestCase):
    def test_git_hub_login_redirect(self):
        response = self.client.get(reverse('social:begin', args=['github']))
        self.assertEqual(response.status_code, 302)

    def test_google_login_redirect(self):
        response = self.client.get(reverse('social:begin', args=['google-oauth2']))
        self.assertEqual(response.status_code, 302)
