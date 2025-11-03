from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class LoginViewTests(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "haslotest1234"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    def test_login_success(self):
        response = self.client.post(
            "/dashboard/login/", {"username": self.username, "password": self.password}
        )
        self.assertEqual(response.status_code, 302)

    def test_login_fail(self):
        response = self.client.post(
            "/dashboard/login/", {"username": self.username, "password": "zly_haslo"}
        )
        self.assertContains(response, "correct username and password", status_code=200)
