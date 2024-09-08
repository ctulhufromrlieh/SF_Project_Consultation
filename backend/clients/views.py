from django.shortcuts import render

from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from main.models import Client, Specialist, Slot
from main.serializers import SpecialistSerializer, SlotSerializer
from main.utils import to_int, is_datetimes_intersect
from .querysets import get_slot_queryset
from .permissions import ClientPermission


# import main.models
# import main.serializers
# from main import models
# import querysets

# Create your views here.
class SpecialistListView(ListAPIView):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer
    permission_classes = [ClientPermission]

class SpecialistView(RetrieveAPIView):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer
    permission_classes = [ClientPermission]

class SlotListView(ListAPIView):
    # queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    permission_classes = [ClientPermission]

    def get_queryset(self):
        return get_slot_queryset(self.request, True)
    
class SlotView(RetrieveAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    permission_classes = [ClientPermission]

@api_view(["POST",])
@permission_classes([ClientPermission])
def sign_to_slot(request, slot):
    if request.method == "POST":
        user = request.user
        if not user or not user.is_authenticated or not user.is_active:
            return Response({
                "status": 403,
                "error": "User is not authenticated"
                })

        if not Client.is_own(user):
            return Response({
                "status": 403,
                "error": "User is not permited"
                })
        
        # slot_param = request.POST.get("slot", "")
        # slot_param = slot
        # slot_id = to_int(slot_param, -1)
        if slot:
            slot_id=slot
        else:
            slot_id=-1
        if slot_id == -1:
            return Response({
                "status": 400,
                "error": "Slot id not defined"
                })
        
        slot_obj = Slot.objects.filter(id=slot_id).first()
        if not slot_obj:
            return Response({
                "status": 400,
                "error": "Slot with such id not exists"
                })
        
        if slot_obj.client == user.client:
            return Response({
                "status": 400,
                "error": "This slot already used by you"
                })

        if slot_obj.client:
            return Response({
                "status": 400,
                "error": "This slot already used"
                })
        
        client_slots = Slot.objects.all().filter(client=user.client)
        for curr_slot in client_slots:
            curr_datetime_1 = curr_slot.datetime1
            curr_datetime_2 = curr_slot.datetime2
            
            if (is_datetimes_intersect(slot_obj.datetime1, slot_obj.datetime2, curr_datetime_1, curr_datetime_2)):
                return Response({
                    "status": 400,
                    "error": "New slot and old slot is intersects"
                    })
            
        slot_obj.client = user.client
        slot_obj.save()
        return Response({
            "status": 200,
            "success": "Client successfully signed to slot"
            })

# class SlotSetSelfClientView(UpdateAPIView):
#     serializer_class = SlotSerializer
#     permission_classes = [CanSlotSetSelfClient]