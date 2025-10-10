from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):  # TODO: remove
    template_name = "home.html"  # TODO: remove whole template
    login_url = "/users/login/"
