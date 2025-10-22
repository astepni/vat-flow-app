from datetime import datetime
from decimal import Decimal, InvalidOperation

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic import TemplateView

from .models import BillingRecord


class OkresForm(forms.Form):
    okres = forms.ChoiceField(
        choices=[
            (f"{y}-{m:02d}", f"{y}-{m:02d}")
            for y in range(datetime.now().year - 1, datetime.now().year + 1)
            for m in range(1, 13)
        ],
        label="Okres rozliczeniowy",
    )
    nadwyzka_z_poprzedniej = forms.IntegerField(
        label="Nadwyżka z poprzedniej deklaracji",
        initial=0,
        required=False,
        min_value=0,
        error_messages={"min_value": "Nie można wskazać liczby mniejszej niż 1 zł."},
        help_text="Podaj całą kwotę (w zł), bez groszy. Pole może być puste.",
    )


class VatCalculationView(LoginRequiredMixin, TemplateView):
    template_name = "vat_simulation/vat_calculation.html"

    def get(self, request, *args, **kwargs):
        okres = request.GET.get("okres", datetime.now().strftime("%Y-%m"))

        nadwyzka_param = request.GET.get("nadwyzka_z_poprzedniej", "")
        try:
            nadwyzka = int(float(nadwyzka_param)) if nadwyzka_param else 0
        except (ValueError, InvalidOperation, TypeError):
            nadwyzka = 0

        if nadwyzka < 0:
            nadwyzka = 0

        try:
            year, month = map(int, okres.split("-"))
        except Exception:
            year, month = datetime.now().year, datetime.now().month

        sprzedaz = BillingRecord.objects.filter(
            user=request.user,
            typ="sprzedazowa",
            data_sprzedazy__year=year,
            data_sprzedazy__month=month,
        )
        suma_netto_sprzedaz = (
            sprzedaz.aggregate(Sum("suma_netto"))["suma_netto__sum"] or 0
        )
        suma_vat_sprzedaz = sprzedaz.aggregate(Sum("suma_vat"))["suma_vat__sum"] or 0

        zakup = BillingRecord.objects.filter(
            user=request.user,
            typ="kosztowa",
            data_sprzedazy__year=year,
            data_sprzedazy__month=month,
        )
        suma_vat_zakup = zakup.aggregate(Sum("suma_vat"))["suma_vat__sum"] or 0

        saldo = suma_vat_sprzedaz - suma_vat_zakup - nadwyzka
        do_zaplaty = saldo if saldo > 0 else 0
        nadwyzka_kw = abs(saldo) if saldo < 0 else 0

        form = OkresForm(initial={"okres": okres, "nadwyzka_z_poprzedniej": nadwyzka})

        ctx = {
            "form": form,
            "okres": okres,
            "suma_netto_sprzedaz": suma_netto_sprzedaz,
            "suma_vat_sprzedaz": suma_vat_sprzedaz,
            "suma_vat_zakup": suma_vat_zakup,
            "do_zaplaty": do_zaplaty,
            "nadwyzka": nadwyzka_kw,
        }
        return self.render_to_response(ctx)
