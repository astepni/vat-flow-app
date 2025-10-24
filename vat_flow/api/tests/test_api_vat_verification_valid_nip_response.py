from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class VatVerificationValidNipResponseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_vat_verification_valid_nip_shows_result(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post("/api/vat-verification/", {"nip": "1234563218"})
        self.assertContains(response, "NIP znajduje się na białej liście")
