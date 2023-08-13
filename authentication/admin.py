from django.contrib import admin
from .models import CustomUser, UserInformation
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserInformation)
