from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from authentication.forms import UserEditForm, UserInfoForm, PinChangeForm
from authentication.models import UserInformation
from phonenumber_field.validators import validate_international_phonenumber
from super_admin.forms import HelpSupportFormUser
from .models import Sell, Expense, CashCollection
from super_admin.models import ExpenseName, HelpSupport
from authentication.mixins import CustomUserPassesTestMixin


# Create your views here.
class RetailerIndex(CustomUserPassesTestMixin, View):
    template_name = "retailer.html"
    user_type = "is_retailer"

    def get(self, request):
        return render(request, self.template_name)


class BuySell(CustomUserPassesTestMixin, View):
    user_type = "is_retailer"
    template_name = "buy-sell.html"

    def get(self, request):
        return render(request, template_name=self.template_name)

    def post(self, request):
        date_input = request.POST.get("datePicker")
        payable_amount_input = request.POST.get("totalPrice")
        paid_amount_input = request.POST.get("cashReceived")
        customer_name_input = request.POST.get("customerName")
        customer_phone_input = request.POST.get("mobileNumber")

        # print('-' * 100)
        # print()
        print(
            date_input,
            paid_amount_input,
            payable_amount_input,
            customer_name_input,
            customer_phone_input,
        )
        data = {
            "date_input": date_input,
            "paid_amount_input": paid_amount_input,
            "payable_amount_input": payable_amount_input,
            "customer_name_input": customer_name_input,
            "customer_phone_input": customer_phone_input,
        }

        try:
            if customer_phone_input and customer_name_input:
                if "+88" not in customer_phone_input:
                    customer_phone_input = "+88" + customer_phone_input
                validate_international_phonenumber(customer_phone_input)
        except:
            messages.error(request, "%s সঠিক নাম্বার দিন" % customer_phone_input)
            return render(request, template_name=self.template_name, context=data)
        if int(paid_amount_input) > int(payable_amount_input):
            messages.error(request, "নগদ গ্রহণ পণ্যের মোট মূল্যের থেকে বেশি")
            return render(request, template_name=self.template_name, context=data)
        if int(payable_amount_input) < 0:
            messages.error(request, "পণ্যের মোট মূল্যের টাকা শূন্য এর থেকে কম")
            return render(request, template_name=self.template_name, context=data)
        if int(paid_amount_input) < 0:
            messages.error(request, "নগদ গ্রহণ টাকা শূন্য এর থেকে কম")
            return render(request, template_name=self.template_name, context=data)
        if customer_phone_input and customer_name_input:
            obj = Sell.objects.create(
                date=date_input,
                payable_amount=payable_amount_input,
                paid_amount=paid_amount_input,
                customer_name=customer_name_input,
                customer_number=customer_phone_input,
                retailer=request.user,
            )
            obj.save()
        else:
            obj = Sell.objects.create(
                date=date_input,
                payable_amount=payable_amount_input,
                paid_amount=paid_amount_input,
                retailer=request.user,
            )
            obj.save()
        # print(obj)
        messages.success(request, "বিক্রি সফল হয়েছে !")

        return redirect("retailer:retailer-home")


class RetailerExpense(CustomUserPassesTestMixin, View):
    user_type = "is_retailer"
    template_name = "expenses.html"
    expenses_obj = ExpenseName.objects.all()

    def get(self, request):
        return render(
            request,
            template_name=self.template_name,
            context={"expanses_name": self.expenses_obj},
        )

    def post(self, request):
        image_input = request.FILES.get("expenseImage")
        type_of_expense = request.POST.get("productSelected")
        paid_amount_input = request.POST.get("paidAmount")
        date_input = request.POST.get("datePicker")
        comments_input = request.POST.get("comment")
        expense_obj = ExpenseName.objects.filter(id=type_of_expense).first()
        # print("-" * 19, "from retailer expense")
        # print(image_input)
        # print(type_of_expense)
        # print(expense_obj)
        # print(date_input)
        if type_of_expense is None or expense_obj is None:
            print("test")
            messages.error(request, "খরচের ধরণ সিলেক্ট করুন !")
            data = {
                "expanses_name": self.expenses_obj,
                "expenseImage": image_input,
                "paidAmount": paid_amount_input,
                "comment": comments_input,
                "datePicker": date_input,
            }
            return render(request, template_name=self.template_name, context=data)
        if image_input:
            obj = Expense.objects.create(
                image=image_input,
                name=expense_obj,
                paid_amount=paid_amount_input,
                date=date_input,
                comments=comments_input,
                retailer=request.user,
            )
        else:
            obj = Expense.objects.create(
                name=expense_obj,
                paid_amount=paid_amount_input,
                date=date_input,
                comments=comments_input,
                retailer=request.user,
            )
        obj.save()
        # print(obj)
        messages.success(request, "খরচ সফলভাবে অ্যাড হয়েছে !")
        return redirect("retailer:retailer-home")


class RetailerDues(CustomUserPassesTestMixin, View):
    user_type = "is_retailer"
    template_name = "due-note.html"

    def get(self, request):
        dues_obj = Sell.objects.filter(retailer=request.user)
        unique_numbers = (
            Sell.objects.filter(retailer=request.user)
            .values("customer_number", "customer_name")
            .distinct()
        )
        # dues_objs_greater_zero = [due for due in dues_obj if due.get_due > 0]
        data = []
        key = 1
        # print(distinct_phone)
        for phone in unique_numbers:
            # print(phone)
            if phone.get("customer_number") != "":
                due = 0
                sell_obj = Sell.objects.filter(
                    retailer=request.user, customer_number=phone.get("customer_number")
                )
                for obj in sell_obj:
                    due += obj.get_due
                if due > 0:
                    temp = {
                        "name": str(phone.get("customer_name")),
                        "phone": str(phone.get("customer_number")),
                        "due_amount": due,
                    }
                    data.append(temp)
                # print(temp)
                key += 1

        # print(data)
        return render(
            request=request, template_name=self.template_name, context={"data": data}
        )


class CustomerDuesDetails(CustomUserPassesTestMixin, View):
    user_type = "is_retailer"
    template_name = "due-profile.html"

    def get(self, request, phone):
        sell_obj = Sell.objects.filter(
            customer_number=phone, retailer=request.user
        ).first()
        all_sell_obj = Sell.objects.filter(customer_number=phone, retailer=request.user)
        total_due = 0
        individual_dues = [due for due in all_sell_obj if due.get_due > 0]
        collection_info = CashCollection.objects.filter(
            customer_number=phone, retailer=request.user
        )

        for due in individual_dues:
            total_due += due.get_due
        total_collection = 0
        for c in collection_info:
            total_collection += c.paid_amount
        data = {
            # 'phone': sell_obj.customer_number,
            "name": sell_obj.customer_name,
            "number": sell_obj.customer_number,
            "dues": individual_dues,
            "collections": collection_info,
            "total_due": total_due,
            "total_collection": total_collection,
        }

        return render(request=request, template_name=self.template_name, context=data)


def api_customer_info(request):
    distinct_phone = (
        Sell.objects.filter(retailer=request.user)
        .values("customer_number", "customer_name")
        .distinct()
    )
    data = []
    key = 1
    # print(distinct_phone)
    for phone in distinct_phone:
        # print(phone)
        if phone.get("customer_number") != "":
            due = 0
            sell_obj = Sell.objects.filter(
                retailer=request.user, customer_number=phone.get("customer_number")
            )
            for obj in sell_obj:
                due += obj.get_due
            temp = {
                "key": key,
                "name": str(phone.get("customer_name")),
                "phone": str(phone.get("customer_number")),
                "dueAmount": due,
            }
            # print(temp)
            key += 1
            data.append(temp)
    # print(data)
    return JsonResponse(data, safe=False, status=200)


class RetailerCollection(CustomUserPassesTestMixin, View):
    user_type = "is_retailer"
    template_name = "collection.html"

    def get(self, request):
        data = {
            "show_suggestions": True,
        }
        return render(request=request, template_name=self.template_name, context=data)

    def post(self, request):
        date_input = request.POST.get("datePicker")
        phone_input = request.POST.get("mobileNumber")
        paid_amount_input = request.POST.get("cashReceived")
        customer_name_input = request.POST.get("customerName")
        due_amount_input = request.POST.get("cashDue")
        data = {
            "date_input": date_input,
            "customer_phone": phone_input,
            "cash_received": paid_amount_input,
            "customer_name": customer_name_input,
            "cash_due": due_amount_input,
            "show_suggestions": True,
        }
        if int(due_amount_input) <= 0:
            messages.error(request, f"{customer_name_input} এর কোনো বাকি নেই!")
            return render(request, template_name=self.template_name, context=data)
        elif int(paid_amount_input) > int(due_amount_input):
            messages.error(request, f"বাকির থেকে বেশি টাকা জমা দেয়া হয়েছে!")
            return render(request, template_name=self.template_name, context=data)
        sell_objs = Sell.objects.filter(
            retailer=request.user, customer_number=phone_input
        )
        if sell_objs:
            paid_amount = int(paid_amount_input)
            # print(sell_objs, paid_amount)
            for obj in sell_objs:
                # print('p', obj.get_due)
                if paid_amount == 0:
                    break
                if obj.get_due > 0:
                    if paid_amount - obj.get_due >= 0:
                        paid_amount = paid_amount - int(obj.get_due)
                        obj.paid_amount += obj.get_due
                        # print('amount', paid_amount)
                    else:
                        obj.paid_amount += paid_amount
                        paid_amount = paid_amount - paid_amount
                obj.save()
            collection_obj = CashCollection.objects.create(
                date=date_input,
                customer_number=phone_input,
                customer_name=customer_name_input,
                due_amount=due_amount_input,
                paid_amount=paid_amount_input,
                retailer=request.user,
            )
            collection_obj.save()
            messages.success(request, "কালেকশন সফল হয়েছে !")
        else:
            messages.error(request, "কোনো কাস্টমার পাওয়া যায়নি, সঠিক তথ্য দিন।")
            return render(
                request=request, template_name=self.template_name, context=data
            )

        return redirect("retailer:retailer-home")


class RetailerBusinessStatus(CustomUserPassesTestMixin, View):
    user_type = "is_retailer"
    template_name = "business-status.html"

    def get(self, request):
        return render(request, template_name=self.template_name)


class RetailerBusinessStatusData(CustomUserPassesTestMixin, View):
    user_type = "is_retailer"
    login_url = reverse_lazy("authentication:login")

    def get(self, request, status, time_period):
        model_map = {
            "buy-sell": Sell,
            "collection": CashCollection,
            "expences": Expense,
            "due-summary": Sell,
        }
        model_of = model_map.get(status)
        # print(model_of)
        if time_period == "day":
            objects = model_of.objects.filter(
                retailer=request.user, date=datetime.now().date()
            )
        elif time_period == "week":
            objects = model_of.objects.filter(
                retailer=request.user, date__gte=datetime.now() - timedelta(days=7)
            )
        elif time_period == "month":
            objects = model_of.objects.filter(
                retailer=request.user, date__gte=datetime.now() - timedelta(days=30)
            )
        elif time_period == "halfYear":
            objects = model_of.objects.filter(
                retailer=request.user, date__gte=datetime.now() - timedelta(days=183)
            )
        elif time_period == "year":
            objects = model_of.objects.filter(
                retailer=request.user, date__gte=datetime.now() - timedelta(days=365)
            )
        else:
            objects = model_of.objects.filter(retailer=request.user)
        data = []
        if status == "buy-sell":
            data = []
            key = 1
            total = 0
            for obj in objects:
                temp = {"key": key, "date": obj.date, "amount": obj.payable_amount}
                data.append(temp)
                total += obj.payable_amount
                key += 1
            # data.append({'total': total})
        elif status == "collection" or status == "expences":
            data = []
            key = 1
            total = 0
            for obj in objects:
                temp = {"key": key, "date": obj.date, "amount": obj.paid_amount}
                data.append(temp)
                total += obj.paid_amount
                key += 1
            # data.append({'total': total})
        elif status == "due-summary":
            data = []
            key = 1
            total = 0
            for obj in objects:
                if obj.get_due > 0:
                    temp = {"key": key, "date": obj.date, "amount": obj.get_due}
                    data.append(temp)
                    total += obj.get_due
                    key += 1
            # data.append({'total': total})
        # print('-'*100)
        # print(status, time_period)
        # print(data)
        # print(objects)
        return JsonResponse(status=200, data=data, safe=False)


class RetailerTraining(CustomUserPassesTestMixin, View):
    user_type = "is_retailer"
    template_name = "training.html"

    def get(self, request):
        return render(request, template_name=self.template_name)


class RetailerPrivacyPolicy(CustomUserPassesTestMixin, View):
    user_type = "is_retailer"
    template_name = "privacy-policy.html"

    def get(self, request):
        return render(request, template_name=self.template_name)


class RetailerCollectionFromDues(CustomUserPassesTestMixin, View):
    user_type = "is_retailer"
    template_name = "collection.html"

    def get(self, request, phone):
        due = 0
        sell_obj = Sell.objects.filter(retailer=request.user, customer_number=phone)
        name = sell_obj.first().customer_name
        for obj in sell_obj:
            due += obj.get_due
        # temp = {
        #     "key": key,
        #     "name": str(phone.get('customer_name')),
        #     "phone": str(phone.get('customer_number')),
        #     "dueAmount": due
        # }
        data = {
            "customer_phone": phone,
            "customer_name": name,
            "cash_due": due,
            "show_suggestions": False,
        }
        # print(data)
        return render(request=request, template_name=self.template_name, context=data)

    def post(self, request, phone):
        return RetailerCollection().post(request)


class HelpSupportView(CustomUserPassesTestMixin, View):
    user_type = "is_retailer"
    template_name = "retailer_support.html"

    def get(self, request):
        help_form = HelpSupportFormUser()
        request.session["previous_page"] = request.META.get("HTTP_REFERER", "/")
        # print(request.session['previous'])
        data = {"form": help_form}
        return render(request, template_name=self.template_name, context=data)

    def post(self, request):
        help_form = HelpSupportFormUser(request.POST)
        if help_form.is_valid():
            obj = help_form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, "সাপোর্ট তৈরি হয়েছে।")
            return HttpResponseRedirect(request.session["previous_page"])
        else:
            data = {"form": help_form}
            messages.error(request, "সঠিক তথ্য দিন।")
            return render(request, template_name=self.template_name, context=data)


class HelpSupportListView(CustomUserPassesTestMixin, View):
    user_type = "is_retailer"
    template_name = "retailer_support-list.html"

    def get(self, request):
        request.session["previous_page"] = request.META.get("HTTP_REFERER", "/")
        support_obj = HelpSupport.objects.filter(user=request.user).order_by(
            "-created_at"
        )
        data = {"supports": support_obj}
        return render(request=request, template_name=self.template_name, context=data)


class EditUserProfile(CustomUserPassesTestMixin, View):
    user_type = "is_retailer"
    template_name = "edit_profile.html"

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
            # print('-' * 100)
            # print(model_to_dict(user_save))
            # print(model_to_dict(user_info_save))
            messages.success(request, "প্রোফাইল আপডেট হয়েছে।")
            return HttpResponseRedirect(request.session["previous_page"])
            # if user.is_retailer:
            #     redirect('retailer:retailer-home')
            # else:
            #     return redirect('dashboard:home')

        else:
            data = {"forms": [user_form, user_info_form]}
            messages.error(request, "সঠিক তথ্য দিন।")
            return render(request, template_name=self.template_name, context=data)


class ResetPin(CustomUserPassesTestMixin, View):
    user_type = "is_retailer"
    template_name = "retailer_reset_pin.html"

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
            if user:
                if pin_change_form.cleaned_data.get(
                    "new_password"
                ) == pin_change_form.cleaned_data.get("retype_new_password"):
                    user.set_password(pin_change_form.cleaned_data.get("new_password"))
                    user.save()
                    logout(request)
                    messages.info(request, "পাসওয়ার্ড পরিবর্তন সফল হয়েছে!")
                    return redirect("authentication:login")
                else:
                    messages.error(request, "নতুন পাসওয়ার্ড দুইটি মিল নেই!")
            else:
                messages.error(request, "পুরাতন পাসওয়ার্ড সঠিক নয়!")

        data = {
            "pin_change_form": pin_change_form,
        }
        return render(request, template_name=self.template_name, context=data)
