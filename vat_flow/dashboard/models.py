from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    VAT_PERIOD_CHOICES = [
        ("monthly", "Miesięczny"),
        ("quarterly", "Kwartalny"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField("Nazwa firmy", max_length=255, blank=True)
    nip = models.CharField("NIP", max_length=20, blank=True)
    address = models.TextField("Adres siedziby firmy", blank=True)
    legal_form = models.CharField("Forma prawna firmy", max_length=100, blank=True)
    start_date = models.DateField(
        "Data rozpoczęcia działalności", blank=True, null=True
    )
    regon = models.CharField("Numer REGON", max_length=20, blank=True, null=True)
    vat_registered = models.BooleanField("Rejestracja na VAT", default=False)
    vat_period = models.CharField(
        "Okres rozliczeniowy VAT",
        max_length=20,
        choices=VAT_PERIOD_CHOICES,
        default="monthly",
    )

    def __str__(self):
        return f"Profil {self.company_name} ({self.user.username})"
