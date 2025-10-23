from django.contrib.auth import get_user_model
from django.test import TestCase
from vat_simulation.models import SaleInvoice

User = get_user_model()


class VatRegisterFilterBySalesDateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        SaleInvoice.objects.create(
            user=self.user, nr_faktury="FV001", data_sprzedazy="2025-09-15"
        )
        SaleInvoice.objects.create(
            user=self.user, nr_faktury="FV002", data_sprzedazy="2025-09-25"
        )

    def test_vat_register_filters_sales_by_date_range(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            "/dashboard/vat-simulation/rejestr-vat/",
            {"date_from": "2025-09-20", "date_to": "2025-09-26"},
        )
        self.assertContains(response, "FV002")
        self.assertNotContains(response, "FV001")
