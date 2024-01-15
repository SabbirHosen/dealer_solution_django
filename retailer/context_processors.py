from datetime import datetime
from django.db.models import Sum
from django.utils.translation import gettext as _
from authentication.models import UserInformation
from .models import Sell, Expense


def get_retailer_info(request):
    user_info = UserInformation.objects.filter(user=request.user).first()

    # Calculate today's sell and due
    sell_objs_today = Sell.objects.filter(
        date=datetime.now().date(), retailer=request.user
    )
    today_summary_sell = (
        sell_objs_today.aggregate(today_total_sell=Sum("payable_amount"))
        if sell_objs_today
        else {"today_total_sell": 0}
    )
    today_summary_due = sum(obj.get_due for obj in sell_objs_today)

    # Fetch all sell objects
    sell_objs_all = Sell.objects.filter(retailer=request.user)

    # Calculate total due for all sells
    total_sell_all = sell_objs_all.aggregate(
        total_sell_all=Sum("payable_amount") if sell_objs_all else {"total_sell_all": 0}
    )
    total_due_all = sum(obj.get_due for obj in sell_objs_all)

    # Calculate today's expenses
    expenses_obj_today = Expense.objects.filter(
        date=datetime.now().date(), retailer=request.user
    ).aggregate(Sum("paid_amount"))
    today_expenses = (
        expenses_obj_today.get("paid_amount__sum")
        if expenses_obj_today.get("paid_amount__sum")
        else 0
    )

    # Calculate all expenses
    all_expenses = (
        Expense.objects.filter(retailer=request.user)
        .aggregate(Sum("paid_amount"))
        .get("paid_amount__sum", 0)
    )
    all_expenses = all_expenses if all_expenses else 0

    # Calculate my_cash and my_due
    my_cash = total_sell_all.get("total_sell_all") - (total_due_all + all_expenses)

    data = {
        "name": user_info.user.get_full_name(),
        "shop_name": user_info.shop_name,
        "phone": user_info.user.phone,
        "image": user_info.photo.url,
        "account": _("রিটেইলার"),
        "today_total_sell": today_summary_sell.get("today_total_sell", 0),
        "today_total_due": today_summary_due,
        "today_total_expenses": today_expenses,
        "total_my_cash": my_cash,
        "total_my_due": total_due_all,
    }

    return data
