from django.contrib import admin
from .models import *


@admin.register(DSRProductWallet)
class DSRProductAdmin(admin.ModelAdmin):
    pass


@admin.register(DSRVoucher)
class DSRVoucherAdmin(admin.ModelAdmin):
    pass


@admin.register(DSRSellingVoucher)
class DSRSellingAdmin(admin.ModelAdmin):
    pass


@admin.register(DSRSales)
class DSRSaleAdmin(admin.ModelAdmin):
    pass


@admin.register(DSRCollections)
class DSRCollectionsAdmin(admin.ModelAdmin):
    pass
