from main.models import *
from rest_framework import serializers

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'name')

class SpecialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialist
        fields = ('id', 'name')

class SlotSerializer(serializers.ModelSerializer):
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
        
class SlotUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ('title', 'datetime1', 'datetime2', 'description'
                 )
