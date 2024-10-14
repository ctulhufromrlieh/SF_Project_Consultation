import datetime

from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from main.models import Slot, SlotStatusActionType, ReasonType, SlotAction
from main.utils import is_datetimes_intersect
from .serializers import ForClientUserSerializer, ForClientSlotSerializer, ForClientSlotActionSerializer, UnsignSlotActionSerializer
from .permissions import *
from main.views import *

# Create your views here.
class SpecialistListView(LoggedListModelMixin, ListAPIView):
    queryset = User.objects.filter(groups__name='specialists')
    serializer_class = ForClientUserSerializer
    permission_classes = [ViewSpecPermission]

class SpecialistView(LoggedRetrieveModelMixin, RetrieveAPIView):
    queryset = User.objects.filter(groups__name='specialists')
    serializer_class = ForClientUserSerializer
    permission_classes = [ViewSpecPermission]

class SlotListView(LoggedListModelMixin, ListAPIView):
    serializer_class = ForClientSlotSerializer
    permission_classes = [ViewSlotPermission]

    def get_queryset(self):
        user = self.request.user
        if not user.groups.filter(name="clients").exists():
            return Slot.objects.none()
        
        return Slot.objects.all().exclude(is_deleted=True).filter(Q(client=None) | Q(client=user))
    
class SlotOneView(LoggedRetrieveModelMixin, RetrieveAPIView):
    serializer_class = ForClientSlotSerializer
    permission_classes = [ViewSlotPermission]

    def get_queryset(self):
        user = self.request.user
        if not user.groups.filter(name="clients").exists():
            return Slot.objects.none()
        
        return Slot.objects.all().exclude(is_deleted=True).filter(Q(client=None) | Q(client=user))
    
class SlotActionListView(LoggedListModelMixin, ListAPIView):
    serializer_class = ForClientSlotActionSerializer
    permission_classes = [ViewSlotActionPermission]

    def get_queryset(self):
        try:
            return SlotAction.objects.filter(client=self.request.user.client)
        except:
            return SlotAction.objects.none()
    
class SlotActionOneView(LoggedRetrieveModelMixin, RetrieveAPIView):
    serializer_class = ForClientSlotActionSerializer
    permission_classes = [ViewSlotActionPermission]

    def get_queryset(self):
        try:
            return SlotAction.objects.filter(client=self.request.user.client)
        except:
            return SlotAction.objects.none()

@api_view(["POST",])
@permission_classes([SignSlotActionPermission])
@make_logged
def sign_to_slot(request, slot=-1):
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
        
        if slot_obj.client == user:
            return Response({
                "error": "This slot already used by you"
                }, 400)

        if slot_obj.client:
            return Response({
                "error": "This slot already used"
                }, 400)
        
        client_slots = Slot.objects.all().filter(client=user)
        for curr_slot in client_slots:
            curr_datetime_1 = curr_slot.datetime1
            curr_datetime_2 = curr_slot.datetime2
            
            if (is_datetimes_intersect(slot_obj.datetime1, slot_obj.datetime2, curr_datetime_1, curr_datetime_2)):
                return Response({
                    "status": 400,
                    "error": "New slot and old slot is intersects"
                    })
            
        slot_obj.client = user
        slot_obj.save()

        slot_action = SlotAction.objects.create(client=user, slot=slot_obj, datetime=datetime.datetime.now(datetime.timezone.utc),
                                                status=SlotStatusActionType.SLOT_STATUS_ACTION_CLIENT_SIGN, 
                                                reason_type=None, comment="" )

        return Response({
            "status": 200,
            "success": "You successfully signed to slot"
            })

@swagger_auto_schema(method='POST', request_body=UnsignSlotActionSerializer)
@api_view(["POST",])
@permission_classes([UnsignSlotActionPermission])
@make_logged
def unsign_from_slot(request, slot):
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

        if not (slot_obj.client == user):
            return Response({
                "error": "You are not signed to this slot"
                }, 400)
        
        reason_type = request.POST.get('reason_type', -1)
        comment = request.POST.get('comment', "")
        reason_type_obj = ReasonType.objects.filter(pk=reason_type).first()
        if not reason_type_obj:
            reason_type = -1

        if (reason_type == -1) and (not comment):
            return Response({
                "error": "You should set valid Reason Type or set non-empty comment"
                }, 400)
        
        slot_obj.client = None
        slot_obj.is_accepted = False
        slot_obj.save()

        slot_action = SlotAction.objects.create(client=user, slot=slot_obj, datetime=datetime.datetime.now(datetime.timezone.utc),
                                                status=SlotStatusActionType.SLOT_STATUS_ACTION_CLIENT_UNSIGN, 
                                                reason_type=reason_type_obj, comment=comment )

        return Response({
            "success": "You successfully unsigned from slot"
            }, 200)
