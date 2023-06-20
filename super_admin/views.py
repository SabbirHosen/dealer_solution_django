from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from .models import HelpSupport, RequestNewUser
from .forms import HelpSupportFormUser
from authentication.strings import SET_ROLE_CHOICES


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


class RequestToJoin(View):
    template_name = 'new_user.html'

    def get(self, request):
        data = {
            'role': SET_ROLE_CHOICES
        }
        return render(request=request, template_name=self.template_name, context=data)

    def post(self, request):
        division_dict = {
            "1": 'চট্টগ্রাম',
            "2": 'রাজশাহী',
            "3": 'খুলনা',
            "4": 'বরিশাল',
            "5": 'সিলেট',
            "6": 'ঢাকা',
            "7": 'রংপুর',
            "8": 'ময়মনসিংহ'
        }
        shop_name_input = request.POST.get('shopName')
        owner_name_input = request.POST.get('ownerName')
        phone_input = request.POST.get('phone')
        business_type_input = request.POST.get('businessType')
        division_input = request.POST.get('division')
        district_input = request.POST.get('district')
        if '+88' not in phone_input:
            phone_input = '+88' + phone_input

        # print(shop_name_input, owner_name_input, phone_input, business_type_input, division_dict.get(division_input), district_input)
        obj = RequestNewUser.objects.create(shop_name=shop_name_input,
                                            user_name=owner_name_input,
                                            user_number=phone_input,
                                            business_type=business_type_input,
                                            division=division_dict.get(division_input),
                                            district=district_input
                                            )
        # print(obj)
        return render(request=request, template_name='success.html')
