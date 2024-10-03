import datetime
# import serializers
from django.shortcuts import render
from django.http import HttpResponseBadRequest

from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from main.models import Client, Specialist, Slot, SlotAction, SlotStatusActionType
# from main.serializers import SpecialistSerializer, SlotSerializer, SlotUpdateSerializer
from main.utils import to_int, is_datetimes_intersect
from .querysets import get_slot_queryset
from .permissions import SpecialistPermission
from .serializers import SlotSerializerRead, SlotSerializerWrite, ForSpecialistSlotActionSerializer


# import main.models
# import main.serializers
# from main import models
# import querysets

# Create your views here.

class SlotListView(ListCreateAPIView):
    # queryset = Slot.objects.all()
    # serializer_class = SlotSerializerRead
    permission_classes = [SpecialistPermission]

    def get_queryset(self):
        return get_slot_queryset(self.request)
    
    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        if self.request.method == "GET":
            return SlotSerializerRead(*args, **kwargs)
        elif self.request.method == "POST":
            return SlotSerializerWrite(*args, **kwargs)
        else:
            raise Exception("SlotListView.get_serializer: Wrong self.request.method")
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        # print("get_serializer_context:")
        # print(context)
        return context

    def perform_create(self, serializer):
        # super().perform_create(serializer)
        # raise ValueError("123456")
        # raise HttpResponseBadRequest("qwerty")
        serializer.save(specialist=self.request.user.specialist)

    # def validate(self, data):
    #     super().validate()
    #     errors = {}
        
    #     # required fields
    #     required_fields = ['username', 'password', 'email']
    #     for field in required_fields:
    #         if field not in data:
    #             errors[field] = 'This field is required.'
        
    #     if errors:
    #         raise serializers.ValidationError(errors)

class SlotOneView(RetrieveUpdateDestroyAPIView):
    # queryset = Slot.objects.all()
    serializer_class = SlotSerializerWrite
    permission_classes = [SpecialistPermission]
    
    def get_queryset(self):
        return get_slot_queryset(self.request)    
    
    def get_serializer(self, *args, **kwargs):
        #
        kwargs.setdefault('context', self.get_serializer_context())

        if self.request.method == "GET":
            return SlotSerializerRead(*args, **kwargs)
        elif self.request.method == "PUT":
            # print("get_serializer: PUT")
            return SlotSerializerWrite(*args, **kwargs)
        elif self.request.method == "PATCH":
            return SlotSerializerWrite(*args, **kwargs)        
        elif self.request.method == "DELETE":
            return SlotSerializerWrite(*args, **kwargs)
        else:
            raise Exception("SlotOneView.get_serializer_class: Wrong self.request.method")

    def get_serializer_context(self):
        # print("get_serializer_context")
        context = super().get_serializer_context()
        context.update({"request": self.request})
        context.update({"instance": self.get_object()})
        # print("get_serializer_context:")
        # print(context)
        return context
    
class SlotActionListView(ListAPIView):
    serializer_class = ForSpecialistSlotActionSerializer
    permission_classes = [SpecialistPermission]

    # def get_queryset(self):
    #     user = self.request.user
    #     if user:
    #         specialist = user.specialist
    #     else:
    #         specialist = None

    #     if specialist:
    #         return SlotAction.objects.filter(slot__specialist=specialist)
    #     else:
    #         return SlotAction.objects.none()
    def get_queryset(self):
        try:
            return SlotAction.objects.filter(slot__specialist=self.request.user.specialist)
        except:
            return SlotAction.objects.none()
    
class SlotActionOneView(RetrieveAPIView):
    serializer_class = ForSpecialistSlotActionSerializer
    permission_classes = [SpecialistPermission]

    # def get_queryset(self):
    #     user = self.request.user
    #     if user:
    #         specialist = user.specialist
    #     else:
    #         specialist = None

    #     if specialist:
    #         return SlotAction.objects.filter(slot__specialist=specialist)
    #     else:
    #         return SlotAction.objects.none()

    def get_queryset(self):
        try:
            return SlotAction.objects.filter(slot__specialist=self.request.user.specialist)
        except:
            return SlotAction.objects.none()

@api_view(["POST",])
@permission_classes([SpecialistPermission])
def accept_slot(request, slot=-1):
    if request.method == "POST":
        user = request.user

        if slot:
            slot_id=slot
        else:
            slot_id=-1

        if slot_id == -1:
            return Response({
                "error": "Slot id not defined"
                }, 400)
        
        slot_obj = Slot.objects.filter(id=slot_id).first()
        if not slot_obj:
            return Response({
                "error": "Slot with such id not exists"
                }, 400)
        
        if slot_obj.specialist.user != user:
            return Response({
                "error": "It is not your slot"
                }, 400)

        if not slot_obj.client:
            return Response({
                "error": "Client is not assigned yet"
                }, 400)
       
        if  slot_obj.is_accepted:
            return Response({
                "error": "This slot already accepted"
                }, 400)

        slot_obj.is_accepted = True
        slot_obj.save()

        slot_action = SlotAction.objects.create(client=slot_obj.client, slot=slot_obj, datetime=datetime.datetime.now(datetime.timezone.utc),
                                                status=SlotStatusActionType.SLOT_STATUS_ACTION_SPECIALIST_ACCEPT, 
                                                reason_type=None, comment="" )

        return Response({
            "success": "You successfully accept slot"
            }, 200)

@api_view(["POST",])
@permission_classes([SpecialistPermission])
def decline_slot(request, slot=-1):
    if request.method == "POST":
        user = request.user

        if slot:
            slot_id=slot
        else:
            slot_id=-1

        if slot_id == -1:
            return Response({
                "error": "Slot id not defined"
                }, 400)
        
        slot_obj = Slot.objects.filter(id=slot_id).first()
        if not slot_obj:
            return Response({
                "error": "Slot with such id not exists"
                }, 400)
        
        if slot_obj.specialist.user != user:
            return Response({
                "error": "It is not your slot"
                }, 400)

        if not slot_obj.client:
            return Response({
                "error": "Client is not assigned yet"
                }, 400)
       
        client = slot_obj.client

        slot_obj.client = None
        slot_obj.save()

        # print(f"client={client}")

        slot_action = SlotAction.objects.create(client=client, slot=slot_obj, datetime=datetime.datetime.now(datetime.timezone.utc),
                                                status=SlotStatusActionType.SLOT_STATUS_ACTION_SPECIALIST_DECLINE, 
                                                reason_type=None, comment="" )

        return Response({
            "success": "You successfully decline slot"
            }, 200)