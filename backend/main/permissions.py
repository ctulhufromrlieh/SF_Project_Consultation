from rest_framework import permissions

class CodeNamePermission(permissions.BasePermission):
    codename = ""

    def has_permission(self, request, view):
        if self.codename:
            return request.user.has_perm(self.codename)
        else:
            return False
