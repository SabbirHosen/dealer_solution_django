from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import View
from . import forms
from .models import CustomUser, UserInformation
from .forms import UserInfoForm, UserSignupForm, UserEditForm, PinChangeForm


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
                if user.is_retailer:
                    return redirect('retailer:retailer-home')
                return redirect('dashboard:home')
            else:
                return render(request, template_name=self.template_name,
                              context={'login_form': input_login_form, 'msg': 'invalid'})
        else:
            return render(request, template_name=self.template_name, context={'login_form': input_login_form})


def user_logout(request):
    logout(request)
    return redirect('authentication:login')


class CreateUser(LoginRequiredMixin, View):
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
            elif user_form.cleaned_data.get('user_role') == 'RE':
                user.is_retailer = True
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


class EditUserProfile(LoginRequiredMixin, View):
    login_url = reverse_lazy('authentication:login')
    template_name = 'profile.html'

    def get(self, request):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', '/')
        user = request.user
        user_info = UserInformation.objects.filter(user=user).first()
        user_form = UserEditForm(instance=user)
        user_info_form = UserInfoForm(instance=user_info)
        data = {
            'forms': [user_form, user_info_form]
        }
        return render(request, template_name=self.template_name, context=data)

    def post(self, request):
        user = request.user
        user_info = UserInformation.objects.filter(user=user).first()
        user_form = UserEditForm(request.POST, instance=user)
        user_info_form = UserInfoForm(request.POST, request.FILES, instance=user_info)
        if user_form.is_valid() and user_info_form.is_valid():
            # print(user_form.instance.phone)
            # print(user_form.cleaned_data.get('user_role'))
            # user = user_form.save(commit=False)
            # if user_form.cleaned_data.get('user_role') == 'DE':
            #     user.is_dealer = True
            # else:
            #     pass
            # user.save()
            # info = user_info_form.save(commit=False)
            # info.user = user
            # info.save()
            user_save = user_form.save()
            user_info_save = user_info_form.save()
            print('-'*100)
            print(model_to_dict(user_save))
            print(model_to_dict(user_info_save))
            return HttpResponseRedirect(request.session['previous_page'])
            # if user.is_retailer:
            #     redirect('retailer:retailer-home')
            # else:
            #     return redirect('dashboard:home')
        else:
            data = {
                'forms': [user_form, user_info_form]
            }
            return render(request, template_name=self.template_name, context=data)


class ResetPin(LoginRequiredMixin, View):
    login_url = reverse_lazy('authentication:login')
    template_name = 'reset-pin.html'

    def get(self, request):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', '/')
        pin_change_form = PinChangeForm()
        data = {
            'pin_change_form': pin_change_form
        }
        return render(request, template_name=self.template_name, context=data)

    def post(self, request):
        pin_change_form = PinChangeForm(request.POST)
        message = []
        if pin_change_form.is_valid():
            user = authenticate(request, phone=request.user.phone, password=pin_change_form.cleaned_data.get('old_password'))
            print(user)
            if user:
                if pin_change_form.cleaned_data.get('new_password') == pin_change_form.cleaned_data.get('retype_new_password'):
                    user.set_password(pin_change_form.cleaned_data.get('new_password'))
                    user.save()
                    logout(request)
                    return redirect('authentication:login')
                else:
                    message.append('নতুন পাসওয়ার্ড দুইটি মিল নেই!')
            else:
                message.append('পুরাতন পাসওয়ার্ড সঠিক নয়!')

        else:
            data = {
                'pin_change_form': pin_change_form,
                'messages': message
            }
            return render(request, template_name=self.template_name, context=data)
        if len(message) != 0:
            data = {
                'pin_change_form': pin_change_form,
                'messages': message
            }
            return render(request, template_name=self.template_name, context=data)
        else:
            return redirect('dashboard:home')
