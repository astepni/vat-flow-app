from django.urls import path

from .views import (
    AccountingHomeView,
    DeleteInvoiceView,
    InvoiceListView,
    UploadInvoiceView,
)

urlpatterns = [
    path("", AccountingHomeView.as_view(), name="accounting_home"),
    path("upload/", UploadInvoiceView.as_view(), name="upload_invoice"),
    path("list/", InvoiceListView.as_view(), name="invoice_list"),
    path("delete/<int:pk>/", DeleteInvoiceView.as_view(), name="delete_invoice"),
]
