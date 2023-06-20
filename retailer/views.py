from datetime import datetime, timedelta

from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import CustomUser, UserInformation
from phonenumber_field.validators import validate_international_phonenumber
from .models import Sell, Expense, CashCollection
from super_admin.models import ExpenseName


# Create your views here.
class RetailerIndex(LoginRequiredMixin, View):
    login_url = reverse_lazy('authentication:login')
    template_name = 'retailer.html'

    def get(self, request):
        # print(request.user)
        user_info = UserInformation.objects.filter(user=request.user).first()
        # print(user_info)
        # print(datetime.now().date())
        sell_objs_today = Sell.objects.filter(date=datetime.now().date(), retailer=request.user)
        total_sell = 0
        total_due = 0
        for obj in sell_objs_today:
            total_sell += obj.payable_amount
            total_due += obj.get_due

        data = {
            'name': user_info.user.get_full_name(),
            'shop_name': user_info.shop_name,
            'phone': user_info.user.phone,
            'image': user_info.photo.url,
            'account': 'Retailer',
            'total_sell': total_sell,
            'total_due': total_due,
        }
        expenses_obj = Expense.objects.filter(date=datetime.now().date(), retailer=request.user).aggregate(
            Sum('paid_amount'))
        if expenses_obj.get('paid_amount__sum') is None:
            expenses_obj['paid_amount__sum'] = 0
        data.update(expenses_obj)
        # print(expenses_obj)
        sell_objs_all = Sell.objects.filter(retailer=request.user)
        total_sell_all = 0
        total_due_all = 0
        for obj in sell_objs_all:
            total_sell_all += obj.payable_amount
            total_due_all += obj.get_due
        expenses_obj_all = Expense.objects.filter(retailer=request.user).aggregate(
            Sum('paid_amount'))
        if expenses_obj_all.get('paid_amount__sum') is None:
            expenses_obj_all['paid_amount__sum'] = 0
        my_cash = total_sell_all - (total_due_all + expenses_obj_all['paid_amount__sum'])
        data.update({'my_cash': my_cash})
        # print(my_cash, total_sell_all, total_due_all, expenses_obj_all['paid_amount__sum'])
        return render(request, self.template_name, context=data)


class BuySell(View):
    template_name = 'buy-sell.html'

    def get(self, request):
        return render(request, template_name=self.template_name)

    def post(self, request):
        date_input = request.POST.get('datePicker')
        payable_amount_input = request.POST.get('totalPrice')
        paid_amount_input = request.POST.get('cashReceived')
        customer_name_input = request.POST.get('customerName')
        customer_phone_input = request.POST.get('mobileNumber')

        print('-' * 100)
        print()
        print(date_input, paid_amount_input, payable_amount_input, customer_name_input, customer_phone_input)
        try:
            validate_international_phonenumber(customer_phone_input)
            obj = Sell.objects.create(date=date_input,
                                      payable_amount=payable_amount_input,
                                      paid_amount=paid_amount_input,
                                      customer_name=customer_name_input,
                                      customer_number=customer_phone_input,
                                      retailer=request.user)
            obj.save()
            print(obj)
        except:
            data = {
                'Phone': 'Enter a valid phone number'
            }
            print(data)
            return render(request, template_name=self.template_name, context=data)

        return redirect('retailer:retailer-home')


class RetailerExpense(View):
    template_name = 'expenses.html'

    def get(self, request):
        expenxes_obj = ExpenseName.objects.all()
        return render(request, template_name=self.template_name, context={'expanses_name': expenxes_obj})

    def post(self, request):
        image_input = request.FILES.get('expenseImage')
        type_of_expense = request.POST.get('productSelected')
        paid_amount_input = request.POST.get('paidAmount')
        date_input = request.POST.get('datePicker')
        comments_input = request.POST.get('comment')
        expense_obj = ExpenseName.objects.filter(id=type_of_expense).first()
        print(image_input)
        obj = Expense.objects.create(image=image_input,
                                     name=expense_obj,
                                     paid_amount=paid_amount_input,
                                     date=date_input,
                                     comments=comments_input,
                                     retailer=request.user)
        obj.save()
        print(obj)
        return redirect('retailer:retailer-home')


class RetailerDues(View):
    template_name = 'due-note.html'

    def get(self, request):
        dues_obj = Sell.objects.filter(retailer=request.user)
        unique_numbers = Sell.objects.filter(retailer=request.user).values('customer_number',
                                                                           'customer_name').distinct()
        dues_objs_greater_zero = [due for due in dues_obj if due.get_due > 0]
        data = []
        key = 1
        # print(distinct_phone)
        for phone in unique_numbers:
            # print(phone)
            if phone.get('customer_number') != '':
                due = 0
                sell_obj = Sell.objects.filter(retailer=request.user, customer_number=phone.get('customer_number'))
                for obj in sell_obj:
                    due += obj.get_due
                if due > 0:
                    temp = {
                        "name": str(phone.get('customer_name')),
                        "phone": str(phone.get('customer_number')),
                        "due_amount": due
                    }
                    data.append(temp)
                # print(temp)
                key += 1

        # print(data)
        return render(request=request, template_name=self.template_name, context={'data': data})


class CustomerDuesDetails(View):
    template_name = 'due-profile.html'

    def get(self, request, phone):
        sell_obj = Sell.objects.filter(customer_number=phone).first()
        all_sell_obj = Sell.objects.filter(customer_number=phone)
        total = 0
        individual_dues = [due for due in all_sell_obj if due.get_due > 0]
        for due in individual_dues:
            total += due.get_due
        data = {
            'phone': sell_obj.customer_number,
            'name': sell_obj.customer_name,
            'number': sell_obj.customer_number,
            'dues': individual_dues,
            'total': total
        }

        return render(request=request, template_name=self.template_name, context=data)


def api_customer_info(request):
    distinct_phone = Sell.objects.filter(retailer=request.user).values('customer_number', 'customer_name').distinct()
    data = []
    key = 1
    # print(distinct_phone)
    for phone in distinct_phone:
        # print(phone)
        if phone.get('customer_number') != '':
            due = 0
            sell_obj = Sell.objects.filter(retailer=request.user, customer_number=phone.get('customer_number'))
            for obj in sell_obj:
                due += obj.get_due
            temp = {
                "key": key,
                "name": str(phone.get('customer_name')),
                "phone": str(phone.get('customer_number')),
                "dueAmount": due
            }
            # print(temp)
            key += 1
            data.append(temp)
    # print(data)
    return JsonResponse(data, safe=False, status=200)


class RetailerCollection(LoginRequiredMixin, View):
    login_url = reverse_lazy('authentication:login')
    template_name = 'collection.html'

    def get(self, request):
        data = {
            'show_suggestions': True,
        }
        return render(request=request, template_name=self.template_name, context=data)

    def post(self, request):
        date_input = request.POST.get('datePicker')
        phone_input = request.POST.get('mobileNumber')
        paid_amount_input = request.POST.get('cashReceived')
        customer_name_input = request.POST.get('customerName')
        due_amount_input = request.POST.get('cashDue')
        collection_obj = CashCollection.objects.create(date=date_input,
                                                       customer_number=phone_input,
                                                       customer_name=customer_name_input,
                                                       due_amount=due_amount_input,
                                                       paid_amount=paid_amount_input,
                                                       retailer=request.user
                                                       )
        sell_objs = Sell.objects.filter(retailer=request.user, customer_number=phone_input)
        if sell_objs:
            paid_amount = int(collection_obj.paid_amount)
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
                        # print('amount', paid_amount)
                # print('a', obj.get_due, paid_amount)
                obj.save()

            # print(collection_obj)
            collection_obj.save()
        else:
            data = {
                'date': date_input,
                'phone': phone_input,
                'name': customer_name_input,
                'cash_due': due_amount_input,
                'cash_received': paid_amount_input,
                'message': 'Customer is not exist on the phone number',
            }
            return render(request=request, template_name=self.template_name, context=data)

        return redirect('retailer:retailer-home')


class RetailerBusinessStatus(LoginRequiredMixin, View):
    login_url = reverse_lazy('authentication:login')
    template_name = 'business-status.html'

    def get(self, request):
        return render(request, template_name=self.template_name)


class RetailerBusinessStatusData(LoginRequiredMixin, View):
    login_url = reverse_lazy('authentication:login')

    def get(self, request, status, time_period):
        model_map = {
            'buy-sell': Sell,
            'collection': CashCollection,
            'expences': Expense,
            'due-summary': Sell

        }
        model_of = model_map.get(status)
        print(model_of)
        if time_period == 'day':
            objects = model_of.objects.filter(retailer=request.user, date=datetime.now().date())
        elif time_period == 'week':
            objects = model_of.objects.filter(retailer=request.user, date__gte=datetime.now() - timedelta(days=7))
        elif time_period == 'month':
            objects = model_of.objects.filter(retailer=request.user, date__gte=datetime.now() - timedelta(days=30))
        elif time_period == 'halfYear':
            objects = model_of.objects.filter(retailer=request.user, date__gte=datetime.now() - timedelta(days=183))
        elif time_period == 'year':
            objects = model_of.objects.filter(retailer=request.user, date__gte=datetime.now() - timedelta(days=365))
        else:
            objects = model_of.objects.filter(retailer=request.user)
        data = []
        if status == 'buy-sell':
            data = []
            key = 1
            total = 0
            for obj in objects:
                temp = {
                    'key': key,
                    'date': obj.date,
                    'amount': obj.payable_amount
                }
                data.append(temp)
                total += obj.payable_amount
                key += 1
            # data.append({'total': total})
        elif status == 'collection' or status == 'expences':
            data = []
            key = 1
            total = 0
            for obj in objects:
                temp = {
                    'key': key,
                    'date': obj.date,
                    'amount': obj.paid_amount
                }
                data.append(temp)
                total += obj.paid_amount
                key += 1
            # data.append({'total': total})
        elif status == 'due-summary':
            data = []
            key = 1
            total = 0
            for obj in objects:
                if obj.get_due > 0:
                    temp = {
                        'key': key,
                        'date': obj.date,
                        'amount': obj.get_due
                    }
                    data.append(temp)
                    total += obj.get_due
                    key += 1
            # data.append({'total': total})
        # print('-'*100)
        # print(status, time_period)
        # print(data)
        # print(objects)
        return JsonResponse(status=200, data=data, safe=False)


class RetailerTraining(LoginRequiredMixin, View):
    login_url = reverse_lazy('authentication:login')
    template_name = 'training.html'

    def get(self, request):
        return render(request, template_name=self.template_name)


class RetailerPrivacyPolicy(LoginRequiredMixin, View):
    login_url = reverse_lazy('authentication:login')
    template_name = 'privacy-policy.html'

    def get(self, request):
        return render(request, template_name=self.template_name)


class RetailerCollectionFromDues(LoginRequiredMixin, View):
    login_url = reverse_lazy('authentication:login')
    template_name = 'collection.html'

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
            'phone': phone,
            'name': name,
            'cash_due': due,
            'show_suggestions': False,
        }
        print(data)
        return render(request=request, template_name=self.template_name, context=data)

    def post(self, request, phone):
        return RetailerCollection().post(request)
