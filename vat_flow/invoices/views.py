from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView

from .forms import InvoiceForm
from .models import Invoice


class AccountingHomeView(TemplateView):
    template_name = "invoices/accounting_home.html"


class UploadInvoiceView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "upload_invoice.html"
    success_url = reverse_lazy("invoice_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = "invoice_list.html"
    context_object_name = "invoices"

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)


class DeleteInvoiceView(LoginRequiredMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy("invoice_list")

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)
