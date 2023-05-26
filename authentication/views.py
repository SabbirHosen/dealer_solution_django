from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import View
from . import forms
from .models import CustomUser


# Create your views here.
class UserLogin(View):
    template_name = 'login.html'

    def get(self, request):
        login_form = forms.UserLogin()
        return render(request, template_name=self.template_name, context={'login_form': login_form})

    def post(self, request):
        input_login_form = forms.UserLogin(request.POST)
        if input_login_form.is_valid():
            phone = input_login_form.cleaned_data.get('phone')
            password = input_login_form.cleaned_data.get('password')
            user = authenticate(request, phone=phone, password=password)
            if user:
                login(request, user=user)
                return redirect('dashboard:home')
            else:
                return render(request, template_name=self.template_name,
                              context={'login_form': input_login_form, 'msg': 'invalid'})
        else:
            return render(request, template_name=self.template_name, context={'login_form': input_login_form})


def user_logout(request):
    logout(request)
    return redirect('authentication:login')
