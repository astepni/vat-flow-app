from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.accounting_home, name="accounting_home"),
    path("upload/", views.upload_invoice, name="upload_invoice"),
    path("list/", views.invoice_list, name="invoice_list"),
    path("delete/<int:pk>/", views.delete_invoice, name="delete_invoice"),
]
