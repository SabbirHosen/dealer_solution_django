from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import View
from . import forms
from .models import CustomUser
from .forms import UserInfoForm, UserSignupForm


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


class CreateUser(View, LoginRequiredMixin):
    login_url = reverse_lazy('authentication:login')
    template_name = 'user_creation.html'

    def get(self, request):
        user_form = UserSignupForm()
        user_info_form = UserInfoForm()
        data = {
            'forms': [user_form, user_info_form]
        }
        return render(request, template_name=self.template_name, context=data)

    def post(self, request):
        user_form = UserSignupForm(request.POST)
        user_info_form = UserInfoForm(request.POST, request.FILES)
        if user_form.is_valid() and user_info_form.is_valid():
            print(user_form.instance.phone)
            print(user_form.cleaned_data.get('user_role'))
            user = user_form.save(commit=False)
            if user_form.cleaned_data.get('user_role') == 'DE':
                user.is_dealer = True
            else:
                pass
            user.save()
            info = user_info_form.save(commit=False)
            info.user = user
            info.save()
            print('-'*100)
            print(model_to_dict(user))
            print(model_to_dict(info))
            return redirect('dashboard:home')
        else:
            data = {
                'forms': [user_form, user_info_form]
            }
            return render(request, template_name=self.template_name, context=data)
