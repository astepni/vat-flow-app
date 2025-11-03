from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserRegistrationTests(TestCase):
    def test_successful_registration_creates_user_and_logs_in(self):
        registration_url = reverse("register")
        response = self.client.post(
            registration_url,
            {
                "username": "newuser",
                "password1": "strongpassword123",
                "password2": "strongpassword123",
            },
        )

        self.assertRedirects(response, reverse("home"))

        self.assertTrue(User.objects.filter(username="newuser").exists())

        user = User.objects.get(username="newuser")
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)
