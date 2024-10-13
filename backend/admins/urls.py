"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view

from admins.views import *

urlpatterns = [
    path('users', UserListView.as_view(), name='api_admins_user_list'),
    path('users/<int:pk>', UserView.as_view(), name='api_admins_user_one'),
    path('users/activate/<int:user>', user_activate, name='api_admins_user_activate'),
    path('users/deactivate/<int:user>', user_deactivate, name='api_admins_user_deactivate'),
    # path('slot_actions', SlotActionListView.as_view(), name='api_admins_slot_actions_list'),
    # path('slot_actions/<int:pk>', SlotActionOneView.as_view(), name='api_admins_slot_action_one'),    
]
