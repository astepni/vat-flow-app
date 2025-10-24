from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from .views import NIPVerificationView

urlpatterns = [
    path(
        "vat-verification/",
        login_required(NIPVerificationView.as_view()),
        name="vat_verification",
    ),
    path(
        "vat-verification-info/",
        login_required(
            TemplateView.as_view(template_name="vat_verification_info.html")
        ),
        name="vat_verification_info",
    ),
]
