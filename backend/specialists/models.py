from django.db import models

# Create your models here.

class SpecialistPermissions(models.Model):
    class Meta:
        permissions = [
            ("view_slot", "Can view slot/slots"),
            ("add_slot", "Can add slot"),
            ("change_slot", "Can change slot"),
            ("delete_slot", "Can delete slot"),
            ("accept_slot", "Can accept slot with client"),
            ("decline_slot", "Can decline slot with client"),
            ("view_slot_action", "Can view slot action/slot actions"),
        ]