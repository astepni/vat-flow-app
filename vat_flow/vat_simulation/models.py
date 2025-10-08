from datetime import date

from django.contrib.auth.models import User
from django.db import models
from invoices.models import Invoice


class Faktura(models.Model):
    TYP_FAKTURY = (
        ("sprzedazowa", "Sprzedażowa"),
        ("kosztowa", "Kosztowa"),
    )
    typ = models.CharField(max_length=20, choices=TYP_FAKTURY)
    plik_pdf = models.FileField(upload_to="faktury_pdfs/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice = models.ForeignKey(
        Invoice, null=True, blank=True, on_delete=models.SET_NULL
    )
    numer = models.CharField(max_length=50)
    data_wystawienia = models.DateField()
    data_sprzedazy = models.DateField(default=date.today)
    kontrahent = models.CharField(max_length=200, blank=True, null=True)
    adres_siedziba = models.CharField(max_length=250, blank=True, null=True)
    wart_brutto_23 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat_23 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    netto_23 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    wart_brutto_8 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat_8 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    netto_8 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    suma_netto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    suma_vat = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    suma_brutto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    rodzaj = models.CharField(max_length=20, choices=TYP_FAKTURY)

    def __str__(self):
        return f"{self.numer} ({self.rodzaj})"
