# permissions.py

from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsRegularUser(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_superuser and request.user.is_authenticated


class IsRetailer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_retailer
