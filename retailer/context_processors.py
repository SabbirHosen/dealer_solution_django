from datetime import datetime
from django.db.models import Sum
from authentication.models import UserInformation
from .models import Sell, Expense


def get_retailer_info(request):
    if request.user.is_authenticated and request.user.is_retailer:
        user_info = UserInformation.objects.filter(user=request.user).first()
        sell_objs_today = Sell.objects.filter(date=datetime.now().date(), retailer=request.user).annotate()
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
        # print(f'___from retailer context processor: {data}')
        return data
    else:
        return {}
