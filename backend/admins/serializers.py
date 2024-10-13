from main.models import *
from rest_framework import serializers

from django.contrib.auth.models import User

from main.utils import *

class ForAdminUserSerializer(serializers.ModelSerializer):
    user_type_caption = serializers.SerializerMethodField('user_type_caption_func')
    def user_type_caption_func(self, user):
        # return get_user_type_caption(obj)   
        return get_user_type_caption(user)
        # if user.groups.filter(name="clients").exists():
        #     return "Client"
        # elif user.groups.filter(name="specialists").exists():
        #     return "Specialist"
        # elif user.groups.filter(name="admins").exists():
        #     return "Admin"
        # else:
        #     return ""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'user_type_caption')

# class ForAdminClientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Client
#         fields = ('id', 'name')

# class ForAdminSpecialistSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Specialist
#         fields = ('id', 'name')

class ForAdminSlotActionSerializer(serializers.ModelSerializer):
    client__name = serializers.CharField(source='client.firts_name', required=False, allow_null=True,)
    slot__specialist = serializers.CharField(source='slot.specialist')
    slot__specialist__name = serializers.CharField(source='slot.specialist.firts_name', required=False, allow_null=True,)
    # slot__type = serializers.IntegerField(source='slot.type')
    slot__type = serializers.CharField(source='slot.type')
    slot__type__name = serializers.CharField(source='slot.type.name', required=False, allow_null=True,)
    slot__title = serializers.CharField(source='slot.title')
    slot__datetime1 = serializers.DateTimeField(source='slot.datetime1', format="%Y-%m-%d %H:%M:%S")
    slot__datetime2 = serializers.DateTimeField(source='slot.datetime2', format="%Y-%m-%d %H:%M:%S")
    slot__description = serializers.CharField(source='slot.description')
    slot__cost = serializers.FloatField(source='slot.cost')
    slot__is_accepted = serializers.BooleanField(source='slot.is_accepted')
    reason_type__name = serializers.CharField(source='reason_type.name', required=False, allow_null=True,)

    class Meta:
        model = SlotAction
        fields = ('id', 'client', 'client__name', 'slot', 
                  'slot__specialist', 'slot__specialist__name','slot__type', 'slot__type__name',
                  'slot__title', 'slot__datetime1', 'slot__datetime2', 'slot__description', 'slot__cost', 'slot__is_accepted',
                  'status', 'reason_type', 'reason_type__name', 'comment', 'datetime',
                 )
        
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    # status = models.CharField(max_length=3, choices=SlotStatusTypes.choices, default=SlotStatusTypes.SLOT_STATUS_NEW)
    status = models.CharField(max_length=3, choices=SlotStatusActionType.choices, default=SlotStatusActionType.SLOT_STATUS_ACTION_NEW)
    reason_type = models.ForeignKey(ReasonType, on_delete=models.CASCADE, null=True, blank=True, default=None)
    comment = models.TextField(default="", help_text="Status action comment", null=True, blank=True)
    datetime = models.DateTimeField(help_text="Datetime of event")   