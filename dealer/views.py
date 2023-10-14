from django.shortcuts import render
from django.views import View
from authentication.mixins import CustomUserPassesTestMixin

# Create your views here.
class DealerHome(CustomUserPassesTestMixin, View):
    template_name = "dealer_home.html"
    user_type = "is_dealer"

    def get(self, request):
        return render(request, self.template_name)


class DealerTraining(CustomUserPassesTestMixin, View):
    user_type = "is_dealer"
    template_name = "training.html"

    def get(self, request):
        return render(request, template_name=self.template_name)


# class RetailerPrivacyPolicy(CustomUserPassesTestMixin, View):
#     user_type = "is_retailer"
#     template_name = "privacy-policy.html"
#
#     def get(self, request):
#         return render(request, template_name=self.template_name)
#
#
# class RetailerCollectionFromDues(CustomUserPassesTestMixin, View):
#     user_type = "is_retailer"
#     template_name = "collection.html"
#
#     def get(self, request, phone):
#         due = 0
#         sell_obj = Sell.objects.filter(retailer=request.user, customer_number=phone)
#         name = sell_obj.first().customer_name
#         for obj in sell_obj:
#             due += obj.get_due
#         # temp = {
#         #     "key": key,
#         #     "name": str(phone.get('customer_name')),
#         #     "phone": str(phone.get('customer_number')),
#         #     "dueAmount": due
#         # }
#         data = {
#             "customer_phone": phone,
#             "customer_name": name,
#             "cash_due": due,
#             "show_suggestions": False,
#         }
#         # print(data)
#         return render(request=request, template_name=self.template_name, context=data)
#
#     def post(self, request, phone):
#         return RetailerCollection().post(request)
#
#
# class HelpSupportView(CustomUserPassesTestMixin, View):
#     user_type = "is_retailer"
#     template_name = "retailer_support.html"
#
#     def get(self, request):
#         help_form = HelpSupportFormUser()
#         request.session["previous_page"] = request.META.get("HTTP_REFERER", "/")
#         # print(request.session['previous'])
#         data = {"form": help_form}
#         return render(request, template_name=self.template_name, context=data)
#
#     def post(self, request):
#         help_form = HelpSupportFormUser(request.POST)
#         if help_form.is_valid():
#             obj = help_form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             messages.success(request, "সাপোর্ট তৈরি হয়েছে।")
#             return HttpResponseRedirect(request.session["previous_page"])
#         else:
#             data = {"form": help_form}
#             messages.error(request, "সঠিক তথ্য দিন।")
#             return render(request, template_name=self.template_name, context=data)
#
#
# class HelpSupportListView(CustomUserPassesTestMixin, View):
#     user_type = "is_retailer"
#     template_name = "retailer_support-list.html"
#
#     def get(self, request):
#         request.session["previous_page"] = request.META.get("HTTP_REFERER", "/")
#         support_obj = HelpSupport.objects.filter(user=request.user).order_by(
#             "-created_at"
#         )
#         data = {"supports": support_obj}
#         return render(request=request, template_name=self.template_name, context=data)
#
#
# class EditUserProfile(CustomUserPassesTestMixin, View):
#     user_type = "is_retailer"
#     template_name = "edit_profile.html"
#
#     def get(self, request):
#         request.session["previous_page"] = request.META.get("HTTP_REFERER", "/")
#         user = request.user
#         user_info = UserInformation.objects.filter(user=user).first()
#         user_form = UserEditForm(instance=user)
#         user_info_form = UserInfoForm(instance=user_info)
#         data = {"forms": [user_form, user_info_form]}
#         return render(request, template_name=self.template_name, context=data)
#
#     def post(self, request):
#         user = request.user
#         user_info = UserInformation.objects.filter(user=user).first()
#         user_form = UserEditForm(request.POST, instance=user)
#         user_info_form = UserInfoForm(request.POST, request.FILES, instance=user_info)
#         if user_form.is_valid() and user_info_form.is_valid():
#             # print(user_form.instance.phone)
#             # print(user_form.cleaned_data.get('user_role'))
#             # user = user_form.save(commit=False)
#             # if user_form.cleaned_data.get('user_role') == 'DE':
#             #     user.is_dealer = True
#             # else:
#             #     pass
#             # user.save()
#             # info = user_info_form.save(commit=False)
#             # info.user = user
#             # info.save()
#             user_save = user_form.save()
#             user_info_save = user_info_form.save()
#             # print('-' * 100)
#             # print(model_to_dict(user_save))
#             # print(model_to_dict(user_info_save))
#             messages.success(request, "প্রোফাইল আপডেট হয়েছে।")
#             return HttpResponseRedirect(request.session["previous_page"])
#             # if user.is_retailer:
#             #     redirect('retailer:retailer-home')
#             # else:
#             #     return redirect('dashboard:home')
#
#         else:
#             data = {"forms": [user_form, user_info_form]}
#             messages.error(request, "সঠিক তথ্য দিন।")
#             return render(request, template_name=self.template_name, context=data)
#
#
# class ResetPin(CustomUserPassesTestMixin, View):
#     user_type = "is_retailer"
#     template_name = "retailer_reset_pin.html"
#
#     def get(self, request):
#         request.session["previous_page"] = request.META.get("HTTP_REFERER", "/")
#         pin_change_form = PinChangeForm()
#         data = {"pin_change_form": pin_change_form}
#         return render(request, template_name=self.template_name, context=data)
#
#     def post(self, request):
#         pin_change_form = PinChangeForm(request.POST)
#         if pin_change_form.is_valid():
#             user = authenticate(
#                 request,
#                 phone=request.user.phone,
#                 password=pin_change_form.cleaned_data.get("old_password"),
#             )
#             if user:
#                 if pin_change_form.cleaned_data.get(
#                     "new_password"
#                 ) == pin_change_form.cleaned_data.get("retype_new_password"):
#                     user.set_password(pin_change_form.cleaned_data.get("new_password"))
#                     user.save()
#                     logout(request)
#                     messages.info(request, "পাসওয়ার্ড পরিবর্তন সফল হয়েছে!")
#                     return redirect("authentication:login")
#                 else:
#                     messages.error(request, "নতুন পাসওয়ার্ড দুইটি মিল নেই!")
#             else:
#                 messages.error(request, "পুরাতন পাসওয়ার্ড সঠিক নয়!")
#
#         data = {
#             "pin_change_form": pin_change_form,
#         }
#         return render(request, template_name=self.template_name, context=data)
