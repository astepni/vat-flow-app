from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
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


class UserSerializer(ModelSerializer):  # TODO: move out to serializers.py
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
