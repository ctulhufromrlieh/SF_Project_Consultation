from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SlotAction
from .email_sending import send_email_about_slot_action

@receiver(post_save, sender=SlotAction)
def slot_action_created(sender, instance, created, **kwargs):
    if created:
        send_email_about_slot_action(instance)
        # send_email_about_slot_action(instance.id)