from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ExpenseName)
admin.site.register(HelpSupport)
admin.site.register(RequestNewUser)


@admin.register(DealerCompany)
class DealerCompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass
