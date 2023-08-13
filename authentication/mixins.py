# mixins.py
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


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
        # if self.request.user.is_authenticated:
        #     return reverse_lazy('retailer:retailer-home')
        # Replace 'custom_template_for_retailer.html' with the path to your custom template
        return render(self.request, 'layout/anonymous_base.html', status=403)


class CustomUserPassesTestMixin(UserPassesTestMixin):
    login_url = reverse_lazy('authentication:login')
    raise_exception = True
    permission_denied_message = "You do not have permission to access this page."

    def test_func(self):
        # Check if user is authenticated
        if not self.request.user.is_authenticated:
            return False  # Redirects to the login page
        if self.user_type is None:
            raise 'Add user_type on the view function'

        return getattr(self.request.user, self.user_type)

    def handle_no_permission(self):
        # Handle the case when user doesn't have permission
        # You can raise a PermissionDenied exception or display a custom message
        messages.error(self.request, self.permission_denied_message)

        if self.request.session.get('home_url'):
            return redirect(self.request.session.get('home_url'))
        else:
            return redirect('dashboard:home')