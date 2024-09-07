from rest_framework import permissions

from main.models import Client

class ClientPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if Client.is_own(request.user):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # return False
        if Client.is_own(request.user):
            return True
        else:
            return False