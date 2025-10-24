from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class VatVerificationEmptyFieldValidationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_vat_verification_empty_nip_shows_error(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post("/api/vat-verification/", {"nip": ""})
        self.assertContains(response, "To pole jest wymagane")
