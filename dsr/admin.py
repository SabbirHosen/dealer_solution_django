from django.contrib import admin
from .models import *


@admin.register(DSRProductWallet)
class DSRProductAdmin(admin.ModelAdmin):
    pass


@admin.register(DSRVoucher)
class DSRVoucherAdmin(admin.ModelAdmin):
    pass
