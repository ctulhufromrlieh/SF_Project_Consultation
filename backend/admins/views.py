from django.shortcuts import render

from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.contrib.auth.models import User

from .permissions import *
from .serializers import *
from main.models import *
from main.permissions import CodeNamePermission

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = ForAdminUserSerializer
    # permission_classes = [AdminPermission]
    # permission_classes = [CodeNamePermission('admins.view_user')]
    permission_classes = [ViewUserPermission]

class UserView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ForAdminUserSerializer
    # permission_classes = [AdminPermission]
    # permission_classes = [CodeNamePermission('admins.view_user')]
    permission_classes = [ViewUserPermission]

# class ClientListView(ListAPIView):
#     queryset = Client.objects.all()
#     serializer_class = ForAdminClientSerializer
#     permission_classes = [AdminPermission]

# class ClientView(RetrieveAPIView):
#     queryset = Client.objects.all()
#     serializer_class = ForAdminClientSerializer
#     permission_classes = [AdminPermission]

# class SpecialistListView(ListAPIView):
#     queryset = Specialist.objects.all()
#     serializer_class = ForAdminSpecialistSerializer
#     permission_classes = [AdminPermission]

# class SpecialistView(RetrieveAPIView):
#     queryset = Specialist.objects.all()
#     serializer_class = ForAdminSpecialistSerializer
#     permission_classes = [AdminPermission]

# class SlotActionListView(ListAPIView):
#     serializer_class = ForAdminSlotActionSerializer
#     # permission_classes = [AdminPermission]
#     permission_classes = [CodeNamePermission('admins.view_slot_action')]

#     def get_queryset(self):
#         return SlotAction.objects.all()
    
# class SlotActionOneView(RetrieveAPIView):
#     serializer_class = ForAdminSlotActionSerializer
#     # permission_classes = [AdminPermission]
#     permission_classes = [CodeNamePermission('admins.view_slot_action')]

#     def get_queryset(self):
#         return SlotAction.objects.all()

# Create your views here.
def change_user_active(request, user, active):
    if request.method == "POST":
        # if not user or not user.is_staff:
        #     return Response({
        #         "status": 403,
        #         "error": "User is not authenticated"
        #         })
        

        # print(f"user: {user}")

        user_obj = User.objects.filter(pk=user).first()
        if not user_obj:
            return Response({
                "error": "Wrong user id"
                }, 400)

        if user_obj.is_active == active:
            if user_obj.is_active:
                return Response({
                    "error": "User already activated"
                    }, 400)
            else:
                return Response({
                    "error": "User already deactivated"
                    }, 400)

        user_obj.is_active = active
        user_obj.save()

        if active:
            return Response({
                "success": "You successfully activate user"
                }, 200)
        else:
            return Response({
                "success": "You successfully deactivate user"
                }, 200)
        
@api_view(["POST",])
# @permission_classes([AdminPermission])
# @permission_classes([CodeNamePermission('admins.change_user_status')])
@permission_classes([ChangeUserStatusPermission])
def user_activate(request, user):
    return change_user_active(request, user, True)

@api_view(["POST",])
# @permission_classes([AdminPermission])
# @permission_classes([CodeNamePermission('admins.change_user_status')])
@permission_classes([ChangeUserStatusPermission])
def user_deactivate(request, user):
    return change_user_active(request, user, False)