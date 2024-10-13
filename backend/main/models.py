from django.db import models
from django.contrib.auth.models import User

class SlotStatusActionType(models.TextChoices):
    SLOT_STATUS_ACTION_NEW = "NEW", "Recent created"
    SLOT_STATUS_ACTION_CLIENT_SIGN = "SGN", "Client sign"
    SLOT_STATUS_ACTION_CLIENT_UNSIGN = "USG", "Client unsign"
    SLOT_STATUS_ACTION_SPECIALIST_ACCEPT = "ACP", "Specialist accept"
    SLOT_STATUS_ACTION_SPECIALIST_DECLINE = "DCL", "Specialist decline"
    SLOT_STATUS_ACTION_DELETE = "DLT", "Slot destroyed"

class ConsultType(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Consult type name")

    def __str__(self):
        return self.name

class ReasonType(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Reason type name")
    status = models.CharField(max_length=3, choices=SlotStatusActionType.choices, default=SlotStatusActionType.SLOT_STATUS_ACTION_NEW)

    def __str__(self):
        return self.name


class Slot(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="client_slots")
    specialist = models.ForeignKey(User, on_delete=models.CASCADE, related_name="specialist_slots")
    type = models.ForeignKey(ConsultType, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, help_text="Slot title")
    datetime1 = models.DateTimeField(help_text="Datetime of start")
    datetime2 = models.DateTimeField(help_text="Datetime of end")
    description = models.TextField(default="", help_text="Description of slot", null=True, blank=True)
    cost = models.FloatField(help_text="Cost for consultation", default=0)
    is_accepted = models.BooleanField(help_text="Client query is accepted by specialist", default=False)
    is_deleted = models.BooleanField(help_text="Slot is deleted", default=False)

    def __str__(self):
        if self.specialist:
            spec_name = self.specialist.name
        else:
            spec_name = "<Unknown>"

        if self.client:
            client_name = self.client.name
        else:
            client_name = "<Unknown>"

        if self.is_accepted:
            is_accepted_str = "<Accepted>"
        else:
            is_accepted_str = "<Not accepted>"

        return f"{self.datetime1} : {spec_name} - {client_name} -- {is_accepted_str}"



class SlotAction(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="client_slot_actions")
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=SlotStatusActionType.choices, default=SlotStatusActionType.SLOT_STATUS_ACTION_NEW)
    reason_type = models.ForeignKey(ReasonType, on_delete=models.CASCADE, null=True, blank=True, default=None)
    comment = models.TextField(default="", help_text="Status action comment", null=True, blank=True)
    datetime = models.DateTimeField(help_text="Datetime of event")

    def __str__(self):
        if self.client:
            client_name = self.client.name
        else:
            client_name = "<Unknown>"

        return f"{self.datetime} : {client_name} -- {self.status}"
