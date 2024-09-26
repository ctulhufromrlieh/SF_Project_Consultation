import datetime
from django.shortcuts import render

from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from main.models import Client, Specialist, Slot, SlotStatusActionType, ReasonType, SlotAction
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
def sign_to_slot(request, slot=-1):
    if request.method == "POST":
        user = request.user

        if slot:
            slot_id=slot
        else:
            slot_id=-1

        if slot_id == -1:
            return Response({
                # "status": 400,
                "error": "Slot id not defined"
                }, 400)
        
        slot_obj = Slot.objects.filter(id=slot_id).first()
        if not slot_obj:
            return Response({
                # "status": 400,
                "error": "Slot with such id not exists"
                }, 400)
        
        if slot_obj.client == user.client:
            return Response({
                # "status": 400,
                "error": "This slot already used by you"
                }, 400)

        if slot_obj.client:
            return Response({
                # "status": 400,
                "error": "This slot already used"
                }, 400)
        
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

        slot_action = SlotAction.objects.create(client=user.client, slot=slot_obj, datetime=datetime.datetime.now(datetime.timezone.utc),
                                                status=SlotStatusActionType.SLOT_STATUS_ACTION_CLIENT_SIGN, 
                                                reason_type=None, comment="" )

        return Response({
            "status": 200,
            "success": "You successfully signed to slot"
            })

@api_view(["POST",])
@permission_classes([ClientPermission])
def unsign_from_slot(request, slot):
    if request.method == "POST":
        user = request.user

        if slot:
            slot_id=slot
        else:
            slot_id=-1

        if slot_id == -1:
            return Response({
                # "status": 400,
                "error": "Slot id not defined"
                }, 400)
        
        slot_obj = Slot.objects.filter(id=slot_id).first()
        if not slot_obj:
            return Response({
                # "status": 400,
                "error": "Slot with such id not exists"
                }, 400)

        if not (slot_obj.client == user.client):
            # print("unsign_from_slot: not (slot_obj.client == user.client)")
            return Response({
                "error": "You are not signed to this slot"
                }, 400)
        
        # print("request.POST:")
        # print(request.POST.dict())

        # cancel_type = request.POST.get('cancel_type', -1)
        # cancel_comment = request.POST.get('cancel_comment', "")
        # # print(f"cancel_type from request: {cancel_type}")
        # cancel_type_obj = CancelType.objects.filter(pk=cancel_type).first()
        # if not cancel_type_obj:
        #     cancel_type = -1
        reason_type = request.POST.get('reason_type', -1)
        comment = request.POST.get('comment', "")
        # print(f"cancel_type from request: {cancel_type}")
        reason_type_obj = ReasonType.objects.filter(pk=reason_type).first()
        if not reason_type_obj:
            reason_type = -1

        # print(f"unsign_from_slot: cancel_type={cancel_type}")
        # print(f"unsign_from_slot: cancel_comment={cancel_comment}")

        if (reason_type == -1) and (not comment):
            return Response({
                "error": "You should set valid Reason Type or set non-empty comment"
                }, 400)
            
        slot_obj.client = None
        slot_obj.is_accepted = False
        slot_obj.save()

        slot_action = SlotAction.objects.create(client=user.client, slot=slot_obj, datetime=datetime.datetime.now(datetime.timezone.utc),
                                                status=SlotStatusActionType.SLOT_STATUS_ACTION_CLIENT_UNSIGN, 
                                                reason_type=reason_type_obj, comment=comment )

        # if not (reason_type == -1):
        #     slot_obj.cancel_type = cancel_type_obj
        # else:
        #     slot_obj.cancel_comment = cancel_comment

        # slot_obj.save()

        # print(f"slot_obj.cancel_comment={slot_obj.cancel_comment}")

        return Response({
            "success": "You successfully unsigned from slot"
            }, 200)

# class SlotSetSelfClientView(UpdateAPIView):
#     serializer_class = SlotSerializer
#     permission_classes = [CanSlotSetSelfClient]