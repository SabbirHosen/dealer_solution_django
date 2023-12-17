from django.contrib import admin
from .models import CustomUser, UserInformation


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["get_full_name", "phone", "get_role"]

    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.short_description = "Name"


@admin.register(UserInformation)
class UserInformationAdmin(admin.ModelAdmin):
    list_display = ["get_full_name", "get_role"]

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_role(self, obj):
        return obj.user.get_role

    get_full_name.short_description = "Name"
    get_role.short_description = "Role"
