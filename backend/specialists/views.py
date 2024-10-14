import datetime

from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from main.models import Slot, SlotAction, SlotStatusActionType
from .permissions import *
from .serializers import SlotSerializerRead, SlotSerializerWrite, ForSpecialistSlotActionSerializer
from main.views import *

# Create your views here.

class SlotListView(LoggedListModelMixin, LoggedCreateModelMixin, ListCreateAPIView):
    permission_classes = [SlotListViewPermission]

    def get_queryset(self):
        user = self.request.user
        if not user.groups.filter(name="specialists").exists():
            return Slot.objects.none()
        
        return Slot.objects.all().exclude(is_deleted=True).filter(specialist=user)
        
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
        return context

    def perform_create(self, serializer):
        serializer.save(specialist=self.request.user)

class SlotOneView(LoggedRetrieveModelMixin, LoggedUpdateModelMixin, LoggedDestroyModelMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = SlotSerializerWrite
    permission_classes = [SlotOneViewPermission]

    def get_queryset(self):
        user = self.request.user
        if not user.groups.filter(name="specialists").exists():
            return Slot.objects.none()
        
        return Slot.objects.all().exclude(is_deleted=True).filter(specialist=user)

    def get_serializer(self, *args, **kwargs):
        #
        kwargs.setdefault('context', self.get_serializer_context())

        if self.request.method == "GET":
            return SlotSerializerRead(*args, **kwargs)
        elif self.request.method == "PUT":
            return SlotSerializerWrite(*args, **kwargs)
        elif self.request.method == "PATCH":
            return SlotSerializerWrite(*args, **kwargs)        
        elif self.request.method == "DELETE":
            return SlotSerializerWrite(*args, **kwargs)
        else:
            raise Exception("SlotOneView.get_serializer_class: Wrong self.request.method")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        try:
            context.update({"instance": self.get_object()})
        except:
            context.update({"instance": None})

        return context
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
    
class SlotActionListView(LoggedListModelMixin, ListAPIView):
    serializer_class = ForSpecialistSlotActionSerializer
    permission_classes = [ViewSlotActionPermission]

    def get_queryset(self):
        try:
            return SlotAction.objects.filter(slot__specialist=self.request.user)
        except:
            return SlotAction.objects.none()
    
class SlotActionOneView(LoggedRetrieveModelMixin, RetrieveAPIView):
    serializer_class = ForSpecialistSlotActionSerializer
    permission_classes = [ViewSlotActionPermission]

    def get_queryset(self):
        try:
            return SlotAction.objects.filter(slot__specialist=self.request.user)
        except:
            return SlotAction.objects.none()

@api_view(["POST",])
@permission_classes([AcceptSlotActionPermission])
@make_logged
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
        
        if slot_obj.specialist != user:
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
@permission_classes([DeclineSlotActionPermission])
@make_logged
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
        
        if slot_obj.specialist != user:
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

        slot_action = SlotAction.objects.create(client=client, slot=slot_obj, datetime=datetime.datetime.now(datetime.timezone.utc),
                                                status=SlotStatusActionType.SLOT_STATUS_ACTION_SPECIALIST_DECLINE, 
                                                reason_type=None, comment="" )

        return Response({
            "success": "You successfully decline slot"
            }, 200)
