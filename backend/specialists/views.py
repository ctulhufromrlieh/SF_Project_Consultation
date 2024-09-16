from django.shortcuts import render

from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from main.models import Client, Specialist, Slot
from main.serializers import SpecialistSerializer, SlotSerializer, SlotUpdateSerializer
from main.utils import to_int, is_datetimes_intersect
from .querysets import get_slot_queryset
from .permissions import SpecialistPermission


# import main.models
# import main.serializers
# from main import models
# import querysets

# Create your views here.

class SlotListView(ListCreateAPIView):
    # queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    permission_classes = [SpecialistPermission]

    def get_queryset(self):
        return get_slot_queryset(self.request)

class SlotView(RetrieveUpdateDestroyAPIView):
    # queryset = Slot.objects.all()
    # serializer_class = SlotSerializer
    permission_classes = [SpecialistPermission]
    
    def get_queryset(self):
        return get_slot_queryset(self.request)    
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SlotSerializer
        elif self.request.method == 'PUT':
            return SlotUpdateSerializer
        elif self.request.method == 'DELETE':
            return SlotSerializer
        
        raise Exception("SlotView.get_serializer_class: wrong self.request.method")


# class SlotView(RetrieveAPIView):
#     # queryset = Slot.objects.all()
#     serializer_class = SlotSerializer
#     permission_classes = [SpecialistPermission]
    
#     def get_queryset(self):
#         return get_slot_queryset(self.request)

# class SlotUpdateView(UpdateAPIView):
#     # queryset = Slot.objects.all()
#     serializer_class = SlotUpdateSerializer
#     permission_classes = [SpecialistPermission]

#     def get_queryset(self):
#         return get_slot_queryset(self.request)