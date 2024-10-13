# from rest_framework import permissions

from main.permissions import CodeNamePermission

class ViewUserPermission(CodeNamePermission):
    codename = "admins.view_user"

class ChangeUserStatusPermission(CodeNamePermission):
    codename = "admins.change_user_status"
