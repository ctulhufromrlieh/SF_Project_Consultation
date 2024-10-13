from django.db import models

# Create your models here.

class ClientPermissions(models.Model):
    class Meta:
        permissions = [
            ("view_spec", "Can view specialist/specialists"),
            ("view_slot", "Can view slot/slots"),
            ("sign_slot", "Can sign slot"),
            ("unsign_slot", "Can unsign slot"),
            ("view_slot_action", "Can view slot action/slot actions"),
        ]
