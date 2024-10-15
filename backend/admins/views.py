import logging

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User

from .permissions import *
from .serializers import *
from main.models import *
from main.views import *

# logger = logging.getLogger(__name__)

class UserListView(LoggedListModelMixin, ListAPIView):
    queryset = User.objects.all()
    serializer_class = ForAdminUserSerializer
    permission_classes = [ViewUserPermission]


class UserView(LoggedRetrieveModelMixin, RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ForAdminUserSerializer
    permission_classes = [ViewUserPermission]

# Create your views here.
def change_user_active(request, user, active):
    if request.method == "POST":
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
@permission_classes([ChangeUserStatusPermission])
@make_logged
def user_activate(request, user):
    return change_user_active(request, user, True)

@api_view(["POST",])
@permission_classes([ChangeUserStatusPermission])
@make_logged
def user_deactivate(request, user):
    return change_user_active(request, user, False)
