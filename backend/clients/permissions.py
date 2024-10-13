from rest_framework import permissions
from django.contrib.auth.models import User
# from main.models import Client
from main.permissions import CodeNamePermission

class ViewSpecPermission(CodeNamePermission):
    codename = "clients.view_spec"

class ViewSlotPermission(CodeNamePermission):
    codename = "clients.view_slot"

class ViewSlotActionPermission(CodeNamePermission):
    codename = "clients.view_slot_action"

class SignSlotActionPermission(CodeNamePermission):
    codename = "clients.sign_slot"

class UnsignSlotActionPermission(CodeNamePermission):
    codename = "clients.unsign_slot"

# class ClientPermission(permissions.BasePermission):

#     def has_permission(self, request, view):
#         # if Client.is_own(request.user):
#         if request.user.groups.filter(name="clients").exists():
#             # return True
#             return request.user.is_active
#         else:
#             return False

#     def has_object_permission(self, request, view, obj):
#         # return False
#         # if Client.is_own(request.user):
#         if request.user.groups.filter(name="clients").exists():
#             # return True
#             return request.user.is_active
#         else:
#             return False