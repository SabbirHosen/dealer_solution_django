from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from .models import HelpSupport
from .forms import HelpSupportFormUser


# Create your views here.
class HelpSupportView(LoginRequiredMixin, View):
    login_url = reverse_lazy('authentication:login')
    template_name = 'support.html'

    def get(self, request):
        help_form = HelpSupportFormUser()
        request.session['previous_page'] = request.META.get('HTTP_REFERER', '/')
        # print(request.session['previous'])
        data = {
            'form': help_form
        }
        return render(request, template_name=self.template_name, context=data)

    def post(self, request):
        help_form = HelpSupportFormUser(request.POST)
        if help_form.is_valid():
            obj = help_form.save(commit=False)
            obj.user = request.user
            obj.save()
            return HttpResponseRedirect(request.session['previous_page'])
        else:
            data = {
                'form': help_form
            }
            return render(request, template_name=self.template_name, context=data)


class HelpSupportListView(LoginRequiredMixin, View):
    login_url = reverse_lazy('authentication:login')
    template_name = 'support-list.html'

    def get(self, request):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', '/')
        support_obj = HelpSupport.objects.filter(user=request.user).order_by('-created_at')
        data = {
            'supports': support_obj
        }
        return render(request=request, template_name=self.template_name, context=data)
