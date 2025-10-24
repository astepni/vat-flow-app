from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class VatRegisterViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_vat_register_view_status_and_filter_form(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get("/dashboard/vat-simulation/rejestr-vat/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rejestr VAT")
        self.assertContains(response, 'name="date_from"')
        self.assertContains(response, 'name="date_to"')
        self.assertContains(response, "Filtruj")
