from rest_framework import permissions

from main.models import Specialist

class ClientPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if Specialist.is_own(request.user):
            # return True
            return request.user.is_active
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # return False
        if Specialist.is_own(request.user):
            # return True
            return request.user.is_active
        else:
            return False