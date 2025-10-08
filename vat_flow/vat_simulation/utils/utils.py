from django import forms
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .utils import import_faktury_z_csv


class UploadCSVForm(forms.Form):
    csv_file = forms.FileField(label="Wybierz plik CSV")


class ImportInvoicesView(FormView):
    template_name = "vat_simulation/import_faktury.html"
    form_class = UploadCSVForm
    success_url = reverse_lazy("import_success")

    def form_valid(self, form):
        csv_file = form.cleaned_data["csv_file"]
        with open("temp.csv", "wb+") as temp_file:
            for chunk in csv_file.chunks():
                temp_file.write(chunk)

        import_faktury_z_csv("temp.csv")
        return super().form_valid(form)
