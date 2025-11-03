from django.contrib.auth import get_user_model
from django.test import TestCase
from invoices.models import Invoice

User = get_user_model()


class InvoiceListSplitTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        Invoice.objects.create(
            user=self.user, pdf="invoices/test1.pdf", invoice_type="income"
        )
        Invoice.objects.create(
            user=self.user, pdf="invoices/test2.pdf", invoice_type="expense"
        )

    def test_invoice_list_contains_types_headings(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get("/invoices/list/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Faktury przychodowe")
        self.assertContains(response, "Dokumenty księgowe kosztowe")
