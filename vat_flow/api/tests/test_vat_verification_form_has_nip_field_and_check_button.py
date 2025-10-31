from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class VatVerificationFormElementsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_vat_verification_page_has_nip_field_and_button(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get("/api/vat-verification/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="nip"')
        self.assertContains(response, "Sprawdź kontrahenta")
