from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class VatCalculationFieldsDisplayTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_vat_calculation_period_and_overplus_fields(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get("/dashboard/vat-simulation/vat-calculation/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Okres rozliczeniowy")
        self.assertContains(response, "<select")
        self.assertContains(response, "Nadwyżka z poprzedniej deklaracji")
        self.assertContains(response, 'name="overplus"')
