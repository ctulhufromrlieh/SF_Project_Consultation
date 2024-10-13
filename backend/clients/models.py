from main.models import Slot
from django.db import models

# Create your models here.

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class ClientPermissions(models.Model):
    class Meta:
        permissions = [
            ("view_spec", "Can view specialist/specialists"),
            ("view_slot", "Can view slot/slots"),
            ("sign_slot", "Can sign slot"),
            ("unsign_slot", "Can unsign slot"),
            ("view_slot_action", "Can view slot action/slot actions"),
        ]

# content_type = ContentType.objects.get_for_model(Slot)
# permission = Permission.objects.create(
#     codename="slot_can_change_client_to_self",
#     name="Can Publish Posts",
#     content_type=content_type,
# )