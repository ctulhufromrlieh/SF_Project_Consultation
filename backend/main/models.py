from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class MyUser(User):
#     pass

class SlotStatusTypes(models.TextChoices):
    SLOT_STATUS_NEW = "NEW", "Recent created"
    SLOT_STATUS_QUERY = "QRY", "Client query sent"
    SLOT_STATUS_ACCEPTED = "ACP", "Client accepted"
    SLOT_STATUS_CANCELED = "CNL", "Canceled"

class ConsultType(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Consult type name")

    def __str__(self):
        return self.name

class CancelType(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Cancel type name")

    def __str__(self):
        return self.name
    
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client")
    name = models.CharField(max_length=255, unique=True, help_text="Client name")

    def __str__(self):
        return self.name
    
    @staticmethod
    def is_own(user):
        return user.groups.filter(name='clients').exists()


class Specialist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="specialist")
    name = models.CharField(max_length=255, unique=True, help_text="Specialist name")

    def __str__(self):
        return self.name
    
    @staticmethod
    def is_own(user):
        return user.groups.filter(name='specialists').exists()
    
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin")
    name = models.CharField(max_length=255, unique=True, help_text="Admin name")

    def __str__(self):
        return self.name
    
    @staticmethod
    def is_own(user):
        return user.groups.filter(name='admins').exists()

class Slot(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, default=None)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    type = models.ForeignKey(ConsultType, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, help_text="Slot title")
    datetime1 = models.DateTimeField(help_text="Datetime of start")
    datetime2 = models.DateTimeField(help_text="Datetime of end")
    description = models.TextField(default="", help_text="Description of slot", null=True, blank=True)
    cost = models.FloatField(help_text="Cost for consultation", default=0)
    status = models.CharField(max_length=3, choices=SlotStatusTypes.choices, default=SlotStatusTypes.SLOT_STATUS_NEW)
    cancel_type = models.ForeignKey(CancelType, on_delete=models.CASCADE, null=True, blank=True, default=None)
    cancel_comment = models.TextField(default="", help_text="Cancellation - comment", null=True, blank=True)

    def __str__(self):
        if self.specialist:
            spec_name = self.specialist.name
        else:
            spec_name = "<Unknown>"

        if self.client:
            client_name = self.client.name
        else:
            client_name = "<Unknown>"

        return f"{self.datetime1} : {spec_name} - {client_name} -- {self.status}"


class SlotQuery(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=SlotStatusTypes.choices, default=SlotStatusTypes.SLOT_STATUS_NEW)
    datetime = models.DateTimeField()

    def __str__(self):
        if self.client:
            client_name = self.client.name
        else:
            client_name = "<Unknown>"

        return f"{self.datetime} : {client_name} -- {self.status}"
