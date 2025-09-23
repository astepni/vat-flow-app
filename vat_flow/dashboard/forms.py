from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "company_name",
            "nip",
            "address",
            "legal_form",
            "start_date",
            "regon",
            "vat_registered",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "vat_registered": forms.CheckboxInput(),
        }
