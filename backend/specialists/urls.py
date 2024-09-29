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

from .views import *

urlpatterns = [
    path('slots', SlotListView.as_view(), name='api_specialists_slot_list'),
    # path('slots/create', SlotCreateView.as_view(), name='api_specialists_slot_create'),
    path('slots/<int:pk>', SlotOneView.as_view(), name='api_specialists_slot_one'),
    path('slots/accept/<int:slot>', accept_slot, name='api_specialists_accept_slot'),
    path('slots/decline/<int:slot>', decline_slot, name='api_specialists_decline_slot'),    
]
