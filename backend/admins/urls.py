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
    path('clients', ClientListView.as_view(), name='api_admins_client_list'),
    path('clients/<int:pk>', ClientView.as_view(), name='api_admins_client_one'),
    path('specialists', SpecialistListView.as_view(), name='api_admins_specialist_list'),
    path('specialists/<int:pk>', SpecialistView.as_view(), name='api_admins_specialist_one'),
    path('user_activate/<int:user>', user_activate, name='api_admins_user_activate'),
    path('user_deactivate/<int:user>', user_deactivate, name='api_admins_user_deactivate'),
]
