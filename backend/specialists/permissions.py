from rest_framework import permissions

# from main.models import Specialist
from main.permissions import CodeNamePermission

class SlotListViewPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user.has_perm("specialists.view_slot")
        elif request.method == "POST":
            return request.user.has_perm("specialists.add_slot")
        else:
            return False

class SlotOneViewPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user.has_perm("specialists.view_slot")
        elif request.method in ["PUT", "PATCH"]:
            return request.user.has_perm("specialists.change_slot")
        elif request.method == "DELETE":
            return request.user.has_perm("specialists.delete_slot")
        else:
            return False
        
class ViewSlotActionPermission(CodeNamePermission):
    codename = "specialists.view_slot_action"

class AcceptSlotActionPermission(CodeNamePermission):
    codename = "specialists.accept_slot"

class DeclineSlotActionPermission(CodeNamePermission):
    codename = "specialists.decline_slot"

# class SpecialistPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # if Client.is_own(request.user):
#         if request.user.groups.filter(name="specialists").exists():
#             # return True
#             return request.user.is_active
#         else:
#             return False

#     def has_object_permission(self, request, view, obj):
#         # return False
#         # if Client.is_own(request.user):
#         if request.user.groups.filter(name="specialists").exists():
#             # return True
#             return request.user.is_active
#         else:
#             return False

#     # def has_permission(self, request, view):
#     #     if Specialist.is_own(request.user):
#     #         # return True
#     #         return request.user.is_active
#     #     else:
#     #         return False

#     # def has_object_permission(self, request, view, obj):
#     #     # return False
#     #     if Specialist.is_own(request.user):
#     #         # return True
#     #         return request.user.is_active
#     #     else:
#     #         return False