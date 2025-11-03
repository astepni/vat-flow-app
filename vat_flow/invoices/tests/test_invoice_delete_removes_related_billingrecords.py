from django.contrib.auth import get_user_model
from django.test import TestCase
from invoices.models import Invoice
from vat_simulation.models import BillingRecord

User = get_user_model()


class InvoiceDeleteCascadeBillingRecordTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.invoice = Invoice.objects.create(
            user=self.user, pdf="invoices/test.pdf", invoice_type="income"
        )
        BillingRecord.objects.create(invoice=self.invoice, amount=100.00)

    def test_delete_invoice_removes_billingrecords(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(f"/invoices/{self.invoice.id}/delete/")
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BillingRecord.objects.filter(invoice=self.invoice).exists())
