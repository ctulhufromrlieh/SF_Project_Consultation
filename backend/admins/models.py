from django.db import models

# Create your models here.

class AdminPermissions(models.Model):
    class Meta:
        permissions = [
            ("view_user", "Can view user/users"),
            ("change_user_status", "Can change user status active"),
        ]