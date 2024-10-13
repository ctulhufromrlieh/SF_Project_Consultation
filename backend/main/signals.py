import datetime

from django.db.models.signals import post_save, post_delete, post_migrate
from django.apps import AppConfig
from django.dispatch import receiver

from .models import Slot, SlotAction, SlotStatusActionType
from .email_sending import send_email_about_slot_action
# from .db_init import *

# @receiver(post_migrate, sender=AppConfig)
# def migrations_made(sender, app_config, verbosity, interactive, stdout, using, plan, apps, **kwargs):
#     print("migrations_made")
#     # raise Exception("123")
#     create_permissions()

@receiver(post_save, sender=SlotAction)
def slot_action_created(sender, instance, created, **kwargs):
    # print("slot_action_created")
    if created:
        send_email_about_slot_action(instance)
        # send_email_about_slot_action(instance.id)

@receiver(post_save, sender=Slot)
def slot_created(sender, instance, created, **kwargs):
    # print("slot_created")
    if created:
        slot_action = SlotAction.objects.create(client=None, slot=instance, datetime=datetime.datetime.now(datetime.timezone.utc),
                                        status=SlotStatusActionType.SLOT_STATUS_ACTION_NEW, 
                                        reason_type=None, comment="" )        
        # send_email_about_slot_action(instance.id)

@receiver(post_delete, sender=Slot)
def slot_deleted(sender, instance, **kwargs):
    # print("slot_deleted")
    slot_action = SlotAction.objects.create(client=None, slot=instance, datetime=datetime.datetime.now(datetime.timezone.utc),
                                    status=SlotStatusActionType.SLOT_STATUS_ACTION_DELETE, 
                                    reason_type=None, comment="" )