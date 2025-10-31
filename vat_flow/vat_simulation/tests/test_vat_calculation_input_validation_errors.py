from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class VatCalculationInputValidationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_vat_calculation_invalid_inputs_show_error(self):
        self.client.login(username="testuser", password="testpass")
        response1 = self.client.post(
            "/dashboard/vat-simulation/vat-calculation/",
            {
                "period": "",
                "overplus": 0,
            },
        )
        self.assertContains(response1, "To pole jest wymagane")

        response2 = self.client.post(
            "/dashboard/vat-simulation/vat-calculation/",
            {
                "period": "2025-10",
                "overplus": "abc",
            },
        )
        self.assertContains(response2, "Podaj prawidłową liczbę")
