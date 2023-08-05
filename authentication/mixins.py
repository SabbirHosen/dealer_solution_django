# mixins.py

from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class RegularUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and not self.request.user.is_superuser


class RetailerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_retailer

    def handle_no_permission(self):
        # Replace 'custom_template_for_retailer.html' with the path to your custom template
        return render(self.request, 'layout/anonymous_base.html', status=403)