"""
URL configuration for vat_flow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("", TemplateView.as_view(template_name="landing.html"), name="landing"),
    path("dashboard/", include("dashboard.urls")),
    path(
        "dashboard/",
        login_required(TemplateView.as_view(template_name="home.html")),
        name="home",
    ),
    path("invoices/", include("invoices.urls")),
    path(
        "dashboard/vat-simulation/",
        include(("vat_simulation.urls", "vat_simulation"), namespace="vat_simulation"),
    ),
    path("api/", include(("api.urls", "api"), namespace="api")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
