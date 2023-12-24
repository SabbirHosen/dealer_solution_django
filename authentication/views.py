from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.views import View
from . import forms
from .models import CustomUser, UserInformation
from .forms import UserInfoForm, UserSignupForm, UserEditForm, PinChangeForm
from django.contrib import messages


# Create your views here.
class UserLogin(View):
    template_name = "login.html"

    def get(self, request):
        if request.user.is_authenticated:
            if request.session.get("home_url"):
                return redirect(request.session.get("home_url"))
            else:
                return redirect("dashboard:home")
        login_form = forms.UserLogin()
        return render(
            request,
            template_name=self.template_name,
            context={"login_form": login_form},
        )

    def post(self, request):
        input_login_form = forms.UserLogin(request.POST)
        if input_login_form.is_valid():
            phone = input_login_form.cleaned_data.get("phone")
            password = input_login_form.cleaned_data.get("password")
            user = authenticate(request, phone=phone, password=password)
            if user:
                login(request, user=user)
                if user.is_retailer:
                    home_url = reverse("retailer:retailer-home")
                    request.session["home_url"] = home_url
                    return redirect("retailer:retailer-home")
                elif user.is_dealer:
                    home_url = reverse("dealer:home")
                    request.session["home_url"] = home_url
                    return redirect(home_url)
                return redirect("dashboard:home")
            else:
                messages.error(request, "সঠিক ফোন/পাসওয়ার্ড দিন।")
                return render(
                    request,
                    template_name=self.template_name,
                    context={"login_form": input_login_form},
                )
        else:
            return render(
                request,
                template_name=self.template_name,
                context={"login_form": input_login_form},
            )


def user_logout(request):
    logout(request)
    messages.success(request, "লগআউট সফল হয়েছে।")
    return redirect("authentication:login")


class CreateUser(LoginRequiredMixin, View):
    login_url = reverse_lazy("authentication:login")
    template_name = "profile.html"

    def get(self, request):
        user_form = UserSignupForm()
        user_info_form = UserInfoForm()
        data = {"forms": [user_form, user_info_form]}
        return render(request, template_name=self.template_name, context=data)

    def post(self, request):
        user_form = UserSignupForm(request.POST)
        user_info_form = UserInfoForm(request.POST, request.FILES)
        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save(commit=False)
            if user_form.cleaned_data.get("user_role") == "DE":
                user.is_dealer = True
            elif user_form.cleaned_data.get("user_role") == "RE":
                user.is_retailer = True
            elif user_form.cleaned_data.get("user_role") == "DSR":
                user.is_delivery_sales_representative = True
            else:
                pass
            user.save()
            user_info_form.instance.user = user  # No need to save UserInfo here
            user_info_form.save()  # Save UserInfo separately
            messages.success(request, "নতুন ইউজার তৈরি হয়েছে।")
            return redirect("dashboard:home")
        else:
            data = {"forms": [user_form, user_info_form]}
            for field, errors in user_form.errors.items():
                error_messages = ", ".join(errors)
                messages.error(request, f"{error_messages}")
            for field, errors in user_info_form.errors.items():
                error_messages = ", ".join(errors)
                messages.error(request, f"{error_messages}")
            return render(request, template_name=self.template_name, context=data)


class EditUserProfile(LoginRequiredMixin, View):
    login_url = reverse_lazy("authentication:login")
    template_name = "profile.html"

    def get(self, request):
        request.session["previous_page"] = request.META.get("HTTP_REFERER", "/")
        user = request.user
        user_info = UserInformation.objects.filter(user=user).first()
        user_form = UserEditForm(instance=user)
        user_info_form = UserInfoForm(instance=user_info)
        data = {"forms": [user_form, user_info_form]}
        return render(request, template_name=self.template_name, context=data)

    def post(self, request):
        user = request.user
        user_info = UserInformation.objects.filter(user=user).first()
        user_form = UserEditForm(request.POST, instance=user)
        user_info_form = UserInfoForm(request.POST, request.FILES, instance=user_info)
        if user_form.is_valid() and user_info_form.is_valid():
            user_save = user_form.save()
            user_info_save = user_info_form.save()
            messages.success(request, "প্রোফাইল আপডেট হয়েছে।")
            return HttpResponseRedirect(request.session["previous_page"])

        else:
            data = {"forms": [user_form, user_info_form]}
            messages.error(request, "সঠিক তথ্য দিন।")
            return render(request, template_name=self.template_name, context=data)


class ResetPin(LoginRequiredMixin, View):
    login_url = reverse_lazy("authentication:login")
    template_name = "reset-pin.html"

    def get(self, request):
        request.session["previous_page"] = request.META.get("HTTP_REFERER", "/")
        pin_change_form = PinChangeForm()
        data = {"pin_change_form": pin_change_form}
        return render(request, template_name=self.template_name, context=data)

    def post(self, request):
        pin_change_form = PinChangeForm(request.POST)
        if pin_change_form.is_valid():
            user = authenticate(
                request,
                phone=request.user.phone,
                password=pin_change_form.cleaned_data.get("old_password"),
            )
            print("", user)
            if user:
                if pin_change_form.cleaned_data.get(
                    "new_password"
                ) == pin_change_form.cleaned_data.get("retype_new_password"):
                    user.set_password(pin_change_form.cleaned_data.get("new_password"))
                    user.save()
                    logout(request)
                    messages.success(request, "পাসওয়ার্ড পরিবর্তন সফল হয়েছে!")
                    return redirect("authentication:login")
                else:
                    messages.error(request, "নতুন পাসওয়ার্ড দুইটি মিল নেই!")

            else:
                messages.error(request, "পুরাতন পাসওয়ার্ড সঠিক নয়!")

        data = {
            "pin_change_form": pin_change_form,
        }
        return render(request, template_name=self.template_name, context=data)
