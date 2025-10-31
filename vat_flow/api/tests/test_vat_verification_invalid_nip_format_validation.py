from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class VatVerificationInvalidNipValidationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_vat_verification_invalid_nip_format_shows_error(self):
        self.client.login(username="testuser", password="testpass")
        response_short = self.client.post("/api/vat-verification/", {"nip": "123"})
        self.assertContains(response_short, "Nieprawidłowy format NIP")

        response_long = self.client.post(
            "/api/vat-verification/", {"nip": "12345678901234"}
        )
        self.assertContains(response_long, "Nieprawidłowy format NIP")

        response_letter = self.client.post(
            "/api/vat-verification/", {"nip": "12ab56789"}
        )
        self.assertContains(response_letter, "Nieprawidłowy format NIP")
