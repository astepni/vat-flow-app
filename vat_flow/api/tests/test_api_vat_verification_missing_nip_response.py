from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class VatVerificationNonexistentInactiveNipTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_vat_verification_nonexistent_or_inactive_nip_shows_message(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post("/api/vat-verification/", {"nip": "9999999999"})
        self.assertContains(response, "NIP nie znajduje się na białej liście")
