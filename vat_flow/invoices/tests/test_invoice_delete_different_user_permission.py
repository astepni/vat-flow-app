from django.contrib.auth import get_user_model
from django.test import TestCase
from invoices.models import Invoice

User = get_user_model()


class InvoiceDeletePermissionTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="haslo123")
        self.other_user = User.objects.create_user(
            username="otheruser", password="innehacko"
        )
        self.invoice = Invoice.objects.create(
            user=self.owner, pdf="invoices/test.pdf", invoice_type="income"
        )

    def test_user_cannot_delete_other_user_invoice(self):
        self.client.login(username="otheruser", password="innehacko")
        response = self.client.post(f"/invoices/{self.invoice.id}/delete/")
        self.assertIn(response.status_code, [403, 404])
        self.assertTrue(Invoice.objects.filter(pk=self.invoice.id).exists())
