from django.contrib.auth.models import User
from django.db import models


class Invoice(models.Model):
    INVOICE_TYPE_CHOICES = [
        ("income", "Przychodowa"),
        ("expense", "Kosztowa"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to="invoices/")
    invoice_type = models.CharField(max_length=10, choices=INVOICE_TYPE_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_invoice_type_display()} - {self.pdf.name}"
