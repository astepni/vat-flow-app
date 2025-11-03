from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class VatVerificationViewTests(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "haslotest1234"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    def test_vat_verification_navigation(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get("/api/vat-verification/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Weryfikacja kontrahenta")
        self.assertContains(response, "Sprawdź kontrahenta")
        self.assertContains(response, "NIP kontrahenta")
