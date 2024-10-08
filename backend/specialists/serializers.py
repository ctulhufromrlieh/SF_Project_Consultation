from rest_framework import serializers

from main.models import *
from main.utils import to_int, is_datetimes_intersect

# class ClientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Client
#         fields = ('id', 'name')

# class SpecialistSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Specialist
#         fields = ('id', 'name')

class SlotSerializerRead(serializers.ModelSerializer):
    client__name = serializers.CharField(source='client.name', required=False, allow_null=True, )
    specialist__name = serializers.CharField(source='specialist.name', required=False, allow_null=True, )
    type__name = serializers.CharField(source='type.name', required=False, allow_null=True, )
    datetime1 = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    datetime2 = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Slot
        fields = ('id', 'client', 'client__name', 'specialist', 'specialist__name', 'type', 'type__name',
                  'title', 'datetime1', 'datetime2', 'description', 'cost', 'is_accepted',
                 )
        
class SlotSerializerWrite(serializers.ModelSerializer):
    datetime1 = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    datetime2 = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Slot
        # fields = ('id', 'specialist', 'type', 'title', 'datetime1', 'datetime2', 'description', 'cost', 
        #          )
        fields = ('id', 'type', 'title', 'datetime1', 'datetime2', 'description', 'cost', 
                 )
        

    def validate(self, data):
        # print(self.context)
        # print("context:")
        # print(self.context)
        # print("data:")
        # print(data)
        request = self.context["request"]
        user = request.user
        instance = self.context.get("instance", None)
        # if instance:
        #     my_id = instance.pk
        # else:
        #     my_id = -1

        errors = {}

        datetime1 = data["datetime1"]
        datetime2 = data["datetime2"]

        if datetime1 >= datetime2:
            errors["datetime1, datetime2"] = "Datetime2 should be greater then Datetime1!"
        else:
            specialist_slots = Slot.objects.all().filter(specialist=user.specialist)
            if instance:
                specialist_slots = specialist_slots.exclude(pk=instance.pk)
            for curr_slot in specialist_slots:
                curr_datetime_1 = curr_slot.datetime1
                curr_datetime_2 = curr_slot.datetime2
                
                if (is_datetimes_intersect(datetime1, datetime2, curr_datetime_1, curr_datetime_2)):
                    errors["datetime1, datetime2"] = "New slot and old slots intersects!"
                    break

        if errors:
            raise serializers.ValidationError(errors)
        
        return data

class ForSpecialistSlotActionSerializer(serializers.ModelSerializer):
    client__name = serializers.CharField(source='client.name', required=False, allow_null=True,)
    slot__specialist = serializers.CharField(source='slot.specialist')
    slot__specialist__name = serializers.CharField(source='slot.specialist.name', required=False, allow_null=True,)
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
        
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    # status = models.CharField(max_length=3, choices=SlotStatusTypes.choices, default=SlotStatusTypes.SLOT_STATUS_NEW)
    status = models.CharField(max_length=3, choices=SlotStatusActionType.choices, default=SlotStatusActionType.SLOT_STATUS_ACTION_NEW)
    reason_type = models.ForeignKey(ReasonType, on_delete=models.CASCADE, null=True, blank=True, default=None)
    comment = models.TextField(default="", help_text="Status action comment", null=True, blank=True)
    datetime = models.DateTimeField(help_text="Datetime of event")       

    # def get_client(self, obj):
    #     if obj.client:
    #         return obj.client.pk
    #     else:
    #         return -1
        
    # def get_cancel_type(self, obj):
    #     if obj.type:
    #         return obj.type.pk
    #     else:
    #         return -1
        
# class SlotUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Slot
#         fields = ('title', 'datetime1', 'datetime2', 'description'
#                  )
