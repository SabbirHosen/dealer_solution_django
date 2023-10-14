from retailer.context_processors import get_retailer_info
from dealer.context_processors import get_dealer_info


def get_user_info(request):
    if request.user.is_authenticated:
        if request.user.is_retailer:
            data = get_retailer_info(request=request)
        elif request.user.is_dealer:
            data = get_dealer_info(request=request)
        else:
            data = {}
        return data
    else:
        return {}
