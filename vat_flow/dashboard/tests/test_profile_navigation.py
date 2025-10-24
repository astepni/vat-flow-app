from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class DashboardProfileTests(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "haslotest1234"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    def test_profile_navigation_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get("/dashboard/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Podaj dane swojej firmy, jeśli chcesz je wygodnie przechowywać w jednym miejscu.",
        )
