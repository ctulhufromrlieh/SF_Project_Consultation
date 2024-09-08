from main.models import *
from rest_framework import serializers

from django.contrib.auth.models import User

from main.utils import *

class UserSerializer(serializers.ModelSerializer):
    user_type_caption = serializers.SerializerMethodField('user_type_caption_func')
    def user_type_caption_func(self, obj):
        return get_user_type_caption(obj)   

    class Meta:
        model = User
        fields = ('id', 'username', 'user_type_caption')

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'name')

class SpecialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialist
        fields = ('id', 'name')