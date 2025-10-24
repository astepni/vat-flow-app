from django.contrib.auth import get_user_model
from django.test import TestCase
from vat_simulation.models import SaleInvoice

User = get_user_model()


class VatRegisterExportExcelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.invoice = SaleInvoice.objects.create(
            user=self.user,
            nr_faktury="FV/01/10/2025",
            data_wystawienia="2025-10-01",
            kontrahent="Firma Demo",
            adres="ul. Przykładowa 1, 00-001 Miasto",
            netto=1000,
            brutto=1230,
            vat_kwota=230,
        )

    def test_export_to_excel_contains_invoice_data(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get("/dashboard/vat-simulation/rejestr-vat/export/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.assertIn(b"FV/01/10/2025", response.content)
        self.assertIn(b"Firma Demo", response.content)
