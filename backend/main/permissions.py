from rest_framework import permissions

class CodeNamePermission(permissions.BasePermission):
    codename = ""

    def has_permission(self, request, view):
        if self.codename:
            return request.user.has_perm(self.codename)
        else:
            return False

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