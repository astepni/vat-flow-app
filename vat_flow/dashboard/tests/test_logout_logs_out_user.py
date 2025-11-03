from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_logout_logs_out_user(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("logout"))

        response = self.client.get(reverse("home"))
        expected_url = "/users/login/?next=/dashboard/"
        self.assertRedirects(response, expected_url)
