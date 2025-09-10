from django.urls import path

from .views import (
    InvoiceListView,
    ProfileView,
    UserLoginView,
    UserLogoutView,
    UserRegisterView,
    UsersListAPIView,
    VatSimulationView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("api/users/", UsersListAPIView.as_view(), name="users_api"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("invoices/", InvoiceListView.as_view(), name="invoices"),
    path("vat-simulation/", VatSimulationView.as_view(), name="vat_simulation"),
]
