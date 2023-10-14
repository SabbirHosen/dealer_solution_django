from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from authentication.forms import UserEditForm, UserInfoForm
from authentication.mixins import CustomUserPassesTestMixin
from authentication.models import UserInformation


# Create your views here.
class DealerHome(CustomUserPassesTestMixin, View):
    template_name = "dealer_home.html"
    user_type = "is_dealer"

    def get(self, request):
        return render(request, self.template_name)


class DealerTraining(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"
    template_name = "training_dealer.html"

    def get(self, request):
        return render(request, template_name=self.template_name)


class DealerPrivacyPolicy(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"
    template_name = "privacy_policy_dealer.html"

    def get(self, request):
        return render(request, template_name=self.template_name)
