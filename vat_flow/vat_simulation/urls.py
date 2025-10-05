from django.urls import path
from django.views.generic import TemplateView

from .views import (
    ApproveInvoiceView,
    DeleteInvoiceView,
    ExportExcelView,
    ImportInvoicesView,
    InvoiceListView,
    VATViewRegister,
    VatViewSimulation,
)

app_name = "vat_simulation"

urlpatterns = [
    path("", VatViewSimulation.as_view(), name="symulacja_vat"),
    path("rejestr-vat/", VATViewRegister.as_view(), name="rejestr_vat"),
    path("import-faktury/", ImportInvoicesView.as_view(), name="import_faktury"),
    path(
        "import-success/",
        TemplateView.as_view(template_name="vat_simulation/import_success.html"),
        name="import_success",
    ),
    path(
        "dashboard/vat-simulation/zatwierdz_fakture/<int:pk>/",
        ApproveInvoiceView.as_view(),
        name="zatwierdz_fakture",
    ),
    path("invoices/", InvoiceListView.as_view(), name="invoices"),
    path("usun-fakture/<int:pk>/", DeleteInvoiceView.as_view(), name="usun_fakture"),
    path("export-excel/", ExportExcelView.as_view(), name="export_excel"),
]
