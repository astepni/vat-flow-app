from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import InvoiceForm
from .models import Invoice


def accounting_home(request):
    return render(request, "invoices/accounting_home.html")


@login_required
def upload_invoice(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST, request.FILES)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.save()
            return redirect("invoice_list")
    else:
        form = InvoiceForm()
    return render(request, "upload_invoice.html", {"form": form})


@login_required
def invoice_list(request):
    invoices = Invoice.objects.filter(user=request.user)
    return render(request, "invoice_list.html", {"invoices": invoices})


@login_required
def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    invoice.delete()
    return HttpResponseRedirect(reverse("invoice_list"))
