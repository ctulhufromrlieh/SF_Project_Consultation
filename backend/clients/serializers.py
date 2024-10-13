from main.models import *
from rest_framework import serializers

# class ClientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Client
#         fields = ('id', 'name')

# class SpecialistSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Specialist
#         fields = ('id', 'name')

class ForClientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class ForClientSlotSerializer(serializers.ModelSerializer):
    client__name = serializers.CharField(source='client.name', required=False, allow_null=True, )
    specialist__name = serializers.CharField(source='specialist.name', required=False, allow_null=True, )
    type__name = serializers.CharField(source='type.name', required=False, allow_null=True, )
    # cancel_type__name = serializers.CharField(source='cancel_type.name', required=False, allow_null=True, )
    datetime1 = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    datetime2 = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Slot
        # fields = ('id', 'client', 'client__name', 'specialist', 'specialist__name', 'type', 'type__name',
        #           'title', 'datetime1', 'datetime2', 'description', 'cost', 'is_accepted',
        #           'cancel_comment'
        #          )
        fields = ('id', 'client', 'client__name', 'specialist', 'specialist__name', 'type', 'type__name',
                  'title', 'datetime1', 'datetime2', 'description', 'cost', 'is_accepted',
                 )
        
class ForClientSlotActionSerializer(serializers.ModelSerializer):
    # client__name = serializers.CharField(source='client.name', required=False, allow_null=True,)
    client__name = serializers.CharField(source='client.first_name', required=False, allow_null=True,)
    slot__specialist = serializers.CharField(source='slot.specialist')
    # slot__specialist__name = serializers.CharField(source='slot.specialist.name', required=False, allow_null=True,)
    slot__specialist__name = serializers.CharField(source='slot.specialist.first_name', required=False, allow_null=True,)
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
        
    # client = models.ForeignKey(Client, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    # status = models.CharField(max_length=3, choices=SlotStatusTypes.choices, default=SlotStatusTypes.SLOT_STATUS_NEW)
    status = models.CharField(max_length=3, choices=SlotStatusActionType.choices, default=SlotStatusActionType.SLOT_STATUS_ACTION_NEW)
    reason_type = models.ForeignKey(ReasonType, on_delete=models.CASCADE, null=True, blank=True, default=None)
    comment = models.TextField(default="", help_text="Status action comment", null=True, blank=True)
    datetime = models.DateTimeField(help_text="Datetime of event")        
    

class UnsignSlotActionSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        print("update:")
        print(validated_data)
        super().update(instance, validated_data)

    class Meta:
        model = SlotAction
        fields = ('id', 'reason_type', 'comment',
                 )
        