from datetime import datetime

import requests
from django import forms
from django.shortcuts import render
from django.views import View


class NIPForm(forms.Form):
    nip = forms.CharField(
        max_length=10,
        min_length=10,
        label="NIP",
        required=True,
        help_text="Wprowadź 10-cyfrowy NIP",
    )

    def clean_nip(self):
        nip = self.cleaned_data["nip"]
        if not nip.isdigit():
            raise forms.ValidationError("NIP może zawierać tylko cyfry.")
        return nip


class NIPVerificationView(View):
    template_name = "vat_verification.html"

    def get(self, request):
        form = NIPForm()
        return render(request, self.template_name, {"form": form, "result": None})

    def post(self, request):
        form = NIPForm(request.POST)
        result = {}
        if form.is_valid():
            nip = form.cleaned_data["nip"]
            current_date = datetime.now().strftime("%Y-%m-%d")
            try:
                resp = requests.get(
                    f"https://wl-api.mf.gov.pl/api/search/nip/{nip}?date={current_date}",
                    timeout=5,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    subject = data.get("result", {}).get("subject")
                    if subject:
                        name = subject.get("name")
                        statusvat = subject.get("statusVat")
                        result = {
                            "status": "success",
                            "message": f"Nazwa: {name}, Status VAT: {statusvat}",
                        }
                    else:
                        result = {
                            "status": "danger",
                            "message": data.get(
                                "message", "Brak firmy o podanym NIP w bazie MF."
                            ),
                        }
                elif resp.status_code == 400:
                    result = {
                        "status": "danger",
                        "message": "Brak firmy o podanym NIP w bazie MF.",
                    }
                else:
                    result = {
                        "status": "danger",
                        "message": f"Błąd API: {resp.status_code}",
                    }
            except requests.RequestException:
                result = {
                    "status": "danger",
                    "message": "Błąd komunikacji z usługą MF. Spróbuj później.",
                }
        else:
            result = {"status": "danger", "message": "Nieprawidłowy format NIP!"}

        return render(request, self.template_name, {"form": form, "result": result})
