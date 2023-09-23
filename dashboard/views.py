from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy


# Create your views here.


class Dashboard(LoginRequiredMixin, View):
    login_url = reverse_lazy("authentication:login")
    template_name = "index.html"

    def get(self, request):
        return redirect("retailer:retailer-home")
