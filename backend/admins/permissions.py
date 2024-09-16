from rest_framework import permissions

from main.models import Admin

class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user:
            # if request.user.is_staff:
            if Admin.is_own(request.user):
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user:
            # if request.user.is_staff:
            if Admin.is_own(request.user):
                return True
        return False