from main.models import Slot
from django.db import models

# Create your models here.

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# content_type = ContentType.objects.get_for_model(Slot)
# permission = Permission.objects.create(
#     codename="slot_can_change_client_to_self",
#     name="Can Publish Posts",
#     content_type=content_type,
# )