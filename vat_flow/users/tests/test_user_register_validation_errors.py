from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserRegistrationValidationTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="existinguser", password="testpass123")

    def test_empty_registration_form_shows_errors(self):
        response = self.client.post(reverse("register"), {})
        self.assertFormError(response, "form", "username", "To pole jest wymagane.")
        self.assertFormError(response, "form", "password1", "To pole jest wymagane.")
        self.assertFormError(response, "form", "password2", "To pole jest wymagane.")

    def test_invalid_password_shows_error(self):
        response = self.client.post(
            reverse("register"),
            {"username": "newuser", "password1": "123", "password2": "123"},
        )
        self.assertFormError(
            response,
            "form",
            "password2",
            "Hasło jest za krótkie lub nie spełnia wymagań.",
        )  # lub dokładny komunikat własny

    def test_duplicate_username_shows_error(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "existinguser",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )
        self.assertFormError(
            response, "form", "username", "Użytkownik o tej nazwie już istnieje."
        )
