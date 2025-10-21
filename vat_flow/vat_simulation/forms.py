from datetime import datetime

from django import forms


class PeriodForm(forms.Form):
    okres = forms.ChoiceField(
        choices=[
            (f"{y}-{m:02d}", f"{y}-{m:02d}")
            for y in range(datetime.now().year - 1, datetime.now().year + 1)
            for m in range(1, 13)
        ],
        label="Okres rozliczeniowy",
    )
    nadwyzka_z_poprzedniej = forms.DecimalField(
        label="Nadwyżka z poprzedniej deklaracji", initial=0, required=False
    )
