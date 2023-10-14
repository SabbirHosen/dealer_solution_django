from authentication.models import UserInformation
from django.utils.translation import gettext as _


def get_dealer_info(request):
    user_info = UserInformation.objects.filter(user=request.user).first()

    data = {
        "name": user_info.user.get_full_name(),
        "shop_name": user_info.shop_name,
        "phone": user_info.user.phone,
        "image": user_info.photo.url,
        "account": _("ডিলার"),
    }
    return data
