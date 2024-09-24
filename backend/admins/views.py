from django.shortcuts import render

from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.contrib.auth.models import User

from .permissions import *
from .serializers import *
from main.models import *

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = ForAdminUserSerializer
    permission_classes = [AdminPermission]

class UserView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ForAdminUserSerializer
    permission_classes = [AdminPermission]

class ClientListView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ForAdminClientSerializer
    permission_classes = [AdminPermission]

class ClientView(RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ForAdminClientSerializer
    permission_classes = [AdminPermission]

class SpecialistListView(ListAPIView):
    queryset = Specialist.objects.all()
    serializer_class = ForAdminSpecialistSerializer
    permission_classes = [AdminPermission]

class SpecialistView(RetrieveAPIView):
    queryset = Specialist.objects.all()
    serializer_class = ForAdminSpecialistSerializer
    permission_classes = [AdminPermission]

# Create your views here.
def change_user_active(request, user, active):
    if request.method == "POST":
        # if not user or not user.is_staff:
        #     return Response({
        #         "status": 403,
        #         "error": "User is not authenticated"
        #         })
        

        user_obj = User.objects.all().filter(user=user)
        if not user_obj:
            return Response({
                "status": 400,
                "error": "Wrong user id"
                })

        if user_obj.is_active == active:
            if user_obj.is_active:
                return Response({
                    "status": 400,
                    "error": "User already activated"
                    })
            else:
                return Response({
                    "status": 400,
                    "error": "User already deactivated"
                    })

        user_obj.is_active = active
        user_obj.save()
        
@api_view(["POST",])
@permission_classes([AdminPermission])
def user_activate(request, user):
    change_user_active(request, user, True)

@api_view(["POST",])
@permission_classes([AdminPermission])
def user_deactivate(request, user):
    change_user_active(request, user, False)