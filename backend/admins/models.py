from django.db import models

# Create your models here.

class AdminPermissions(models.Model):
    class Meta:
        permissions = [
            # ("view_slot", "Can view slot/slots"),
            ("view_user", "Can view user/users"),
            ("change_user_status", "Can change user status active"),
            # ("view_slot_action", "Can view slot action/slot actions"),
        ]