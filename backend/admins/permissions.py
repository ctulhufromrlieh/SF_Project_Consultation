# from rest_framework import permissions

from main.permissions import CodeNamePermission

class ViewUserPermission(CodeNamePermission):
    codename = "admins.view_user"

class ChangeUserStatusPermission(CodeNamePermission):
    codename = "admins.change_user_status"

# from main.models import Admin

# class AdminPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # if Client.is_own(request.user):
#         if request.user.groups.filter(name="admins").exists():
#             # return True
#             return request.user.is_active
#         else:
#             return False

#     def has_object_permission(self, request, view, obj):
#         # return False
#         # if Client.is_own(request.user):
#         if request.user.groups.filter(name="admins").exists():
#             # return True
#             return request.user.is_active
#         else:
#             return False
        
#     # def has_permission(self, request, view):
#     #     if request.user:
#     #         # if request.user.is_staff:
#     #         if Admin.is_own(request.user):
#     #             return True
#     #     return False

#     # def has_object_permission(self, request, view, obj):
#     #     if request.user:
#     #         # if request.user.is_staff:
#     #         if Admin.is_own(request.user):
#     #             return True
#     #     return False