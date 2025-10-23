from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class VatCalculationComputeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_vat_calculation_computes_correct_amounts(self):
        self.client.login(username="testuser", password="testpass")

        response = self.client.post(
            "/dashboard/vat-simulation/vat-calculation/",
            {
                "period": "2025-10",
                "overplus": 0,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Łączna wysokość podstawy opodatkowania")
        self.assertContains(response, "0")

        response2 = self.client.post(
            "/dashboard/vat-simulation/vat-calculation/",
            {
                "period": "2025-10",
                "overplus": 1000,
            },
        )
        self.assertContains(response2, "1000")
