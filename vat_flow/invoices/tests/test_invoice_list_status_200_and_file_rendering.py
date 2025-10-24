from django.contrib.auth import get_user_model
from django.test import TestCase
from invoices.models import Invoice

User = get_user_model()


class InvoiceListLinksAndDescriptionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.invoice = Invoice.objects.create(
            user=self.user, pdf="invoices/test1.pdf", invoice_type="income"
        )

    def test_invoice_list_status_and_file_links(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get("/invoices/list/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test1.pdf")
        self.assertContains(response, "Przychodowa")
