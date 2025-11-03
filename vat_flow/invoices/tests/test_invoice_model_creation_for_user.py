from django.contrib.auth import get_user_model
from django.test import TestCase
from invoices.models import Invoice

User = get_user_model()


class InvoiceModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_invoice_creation_for_user(self):
        invoice = Invoice.objects.create(
            user=self.user, pdf="invoices/test.pdf", invoice_type="income"
        )
        self.assertEqual(invoice.user, self.user)
        self.assertEqual(invoice.pdf.name, "invoices/test.pdf")
        self.assertEqual(invoice.invoice_type, "income")
        self.assertIsNotNone(invoice.uploaded_at)
        self.assertEqual(str(invoice), "Przychodowa - invoices/test.pdf")
