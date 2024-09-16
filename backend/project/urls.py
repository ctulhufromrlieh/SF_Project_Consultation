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
from rest_framework_swagger.views import get_swagger_view

from main.views import *

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/accounts/", include("accounts.urls")),   

    path("api/v1/for_clients/", include("clients.urls")),   
    path("api/v1/for_specialists/", include("specialists.urls")),   
    path("api/v1/for_admins/", include("admins.urls")),   

    # path('api/v1/clients/', ClientView.as_view(), name='api_clients'),
    # path('api/v1/specialists/', SpecialistView.as_view(), name='api_specialists'),
    # path('api/v1/slots/', SlotView.as_view(), name='api_slots'),

    path('openapi', get_schema_view(
        title="Consultation",
        description="API for Consultation"
    ), name='openapi-schema'),

    path('swagger', schema_view)
]
