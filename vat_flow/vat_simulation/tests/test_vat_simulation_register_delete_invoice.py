from django.contrib.auth import get_user_model
from django.test import TestCase
from vat_simulation.models import SaleInvoice

User = get_user_model()


class VatRegisterInvoiceDeleteTests(TestCase):
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

    def test_delete_invoice_removes_record_and_refreshes_view(self):
        self.client.login(username="testuser", password="testpass")
        delete_url = f"/dashboard/vat-simulation/rejestr-vat/{self.invoice.pk}/delete/"
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        response_list = self.client.get("/dashboard/vat-simulation/rejestr-vat/")
        self.assertNotContains(response_list, "FV/01/10/2025")
        self.assertFalse(SaleInvoice.objects.filter(pk=self.invoice.pk).exists())
