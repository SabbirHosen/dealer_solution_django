from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    pass


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass


@admin.register(DealerExpense)
class DealerExpenseAdmin(admin.ModelAdmin):
    pass

@admin.register(DealerRepresentative)
class DealerRepresentativeAdmin(admin.ModelAdmin):
    pass