from datetime import datetime, timedelta

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer

from .forms import ProfileForm
from .models import Profile


class UserRegisterView(CreateView):
    template_name = "users/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


class UserLoginView(LoginView):
    template_name = "users/login.html"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class UsersListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class ProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


class InvoiceListView(TemplateView):
    template_name = "users/invoices.html"


class VatSimulationView(TemplateView):
    template_name = "vat_simulation/vat_simulation.html"


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"


class LandingPageView(TemplateView):
    template_name = "vat_flow/landing.html"


class DashboardView(TemplateView):
    template_name = "dashboard_home.html"

    PUBLIC_HOLIDAYS = [
        (12, 25),
        (12, 26),
    ]

    def _is_holiday(self, date):
        return date.weekday() >= 5 or (date.month, date.day) in self.PUBLIC_HOLIDAYS

    def _get_next_workday(self, date):
        while self._is_holiday(date):
            date += timedelta(days=1)
        return date

    def _calculate_vat_deadline(self, today):
        if today.month == 1:
            vat_month = 12
            vat_year = today.year - 1
            pay_month = 1
            pay_year = today.year
        else:
            vat_month = today.month - 1
            vat_year = today.year
            pay_month = today.month
            pay_year = today.year

        deadline = datetime(pay_year, pay_month, 25)
        if self._is_holiday(deadline):
            deadline = self._get_next_workday(deadline)

        days_left = (deadline.date() - today.date()).days
        return days_left, deadline.strftime("%Y-%m-%d"), vat_month, vat_year, deadline

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.now()
        (
            days_left,
            deadline_str,
            vat_month,
            vat_year,
            deadline_dt,
        ) = self._calculate_vat_deadline(today)
        MONTHS = [
            "",
            "styczeń",
            "luty",
            "marzec",
            "kwiecień",
            "maj",
            "czerwiec",
            "lipiec",
            "sierpień",
            "wrzesień",
            "październik",
            "listopad",
            "grudzień",
        ]
        okres_str = f"{MONTHS[vat_month]} {vat_year}"
        deadline_pretty = deadline_dt.strftime("%d.%m.%Y")
        context["days_left"] = days_left
        context["deadline_date"] = deadline_pretty
        context["vat_period"] = okres_str
        return context
