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
        request = self.context["request"]
        user = request.user

        errors = {}

        datetime1 = data["datetime1"]
        datetime2 = data["datetime2"]

        specialist_slots = Slot.objects.all().filter(specialist=user.specialist)
        for curr_slot in specialist_slots:
            curr_datetime_1 = curr_slot.datetime1
            curr_datetime_2 = curr_slot.datetime2
            
            if (is_datetimes_intersect(datetime1, datetime2, curr_datetime_1, curr_datetime_2)):
                errors["datetime1, datetime2"] = "New slot and old slots intersects!"
                break

        if errors:
            raise serializers.ValidationError(errors)
        
        return data

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
