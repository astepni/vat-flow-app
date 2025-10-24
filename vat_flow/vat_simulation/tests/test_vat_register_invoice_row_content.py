from django.contrib.auth import get_user_model
from django.test import TestCase
from vat_simulation.models import SaleInvoice

User = get_user_model()


class VatRegisterInvoiceRecordDisplayTests(TestCase):
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

    def test_invoice_record_includes_key_fields_and_actions(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get("/dashboard/vat-simulation/rejestr-vat/")
        self.assertContains(response, "FV/01/10/2025")
        self.assertContains(response, "2025-10-01")
        self.assertContains(response, "Firma Demo")
        self.assertContains(response, "ul. Przykładowa 1, 00-001 Miasto")
        self.assertContains(response, "1&nbsp;000,00")
        self.assertContains(response, "1&nbsp;230,00")
        self.assertContains(response, "230,00")
        self.assertContains(response, "Usuń")
