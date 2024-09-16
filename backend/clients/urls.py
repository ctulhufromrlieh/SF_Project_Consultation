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

from clients.views import *

urlpatterns = [
    path('specialists', SpecialistListView.as_view(), name='api_clients_specialist_list'),
    path('specialists/<int:pk>', SpecialistView.as_view(), name='api_clients_specialist_one'),
    path('slots', SlotListView.as_view(), name='api_clients_slot_list'),
    path('slots/<int:pk>', SlotView.as_view(), name='api_clients_slot_one'),
    path('slots/sign/<int:slot>', sign_to_slot, name='api_clients_sign_to_slot'),
    path('slots/unsign/<int:slot>', unsign_from_slot, name='api_clients_unsign_from_slot'),
]
