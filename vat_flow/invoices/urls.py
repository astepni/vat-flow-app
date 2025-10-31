from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import InvoiceViewSet
from .views import (
    AccountingHomeView,
    DeleteInvoiceView,
    InvoiceListView,
    UploadInvoiceView,
)

router = DefaultRouter()
router.register(r"api/invoices", InvoiceViewSet, basename="invoice")

urlpatterns = [
    path("", AccountingHomeView.as_view(), name="accounting_home"),
    path("upload/", UploadInvoiceView.as_view(), name="upload_invoice"),
    path("list/", InvoiceListView.as_view(), name="invoice_list"),
    path("delete/<int:pk>/", DeleteInvoiceView.as_view(), name="delete_invoice"),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
