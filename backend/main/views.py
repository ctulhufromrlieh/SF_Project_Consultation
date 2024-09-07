from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import NOT, IsAuthenticated, DjangoModelPermissions

from .serializers import *
from .models import *
from .querysets import *

# Create your views here.

# class ClientView(ListCreateAPIView):
class ClientView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    # permission_classes = [DjangoModelPermissions]

# class SpecialistView(ListCreateAPIView):
class SpecialistViewList(ListAPIView):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer
    # permission_classes = [DjangoModelPermissions]

class SlotView(ListAPIView):
    # queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    # permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        return get_slot_queryset(self.request)

# class ServiceCompanyView(ListCreateAPIView):
#     queryset = ServiceCompany.objects.all()
#     serializer_class = ServiceCompanySerializer
#     permission_classes = [DjangoModelPermissions]

# class CarModelView(ListCreateAPIView):
#     queryset = CarModel.objects.all()
#     serializer_class = CarModelSerializer
#     permission_classes = [DjangoModelPermissions]

# class SingleCarModelView(RetrieveUpdateDestroyAPIView):
#     queryset = CarModel.objects.all()
#     serializer_class = CarModelSerializer
#     permission_classes = [DjangoModelPermissions]

# class EngineModelView(ListCreateAPIView):
#     queryset = EngineModel.objects.all()
#     serializer_class = EngineModelSerializer
#     permission_classes = [DjangoModelPermissions]

# class SingleEngineModelView(RetrieveUpdateDestroyAPIView):
#     queryset = EngineModel.objects.all()
#     serializer_class = EngineModelSerializer
#     permission_classes = [DjangoModelPermissions]

# class TransmissionModelView(ListCreateAPIView):
#     queryset = TransmissionModel.objects.all()
#     serializer_class = TransmissionModelSerializer
#     permission_classes = [DjangoModelPermissions]

# class SingleTransmissionModelView(RetrieveUpdateDestroyAPIView):
#     queryset = TransmissionModel.objects.all()
#     serializer_class = TransmissionModelSerializer
#     permission_classes = [DjangoModelPermissions]

# class MainBridgeModelView(ListCreateAPIView):
#     queryset = MainBridgeModel.objects.all()
#     serializer_class = MainBridgeModelSerializer
#     permission_classes = [DjangoModelPermissions]

# class SingleMainBridgeModelView(RetrieveUpdateDestroyAPIView):
#     queryset = MainBridgeModel.objects.all()
#     serializer_class = MainBridgeModelSerializer
#     permission_classes = [DjangoModelPermissions]

# class SteerableBridgeModelView(ListCreateAPIView):
#     queryset = SteerableBridgeModel.objects.all()
#     serializer_class = SteerableBridgeModelSerializer
#     permission_classes = [DjangoModelPermissions]

# class SingleSteerableBridgeModelView(RetrieveUpdateDestroyAPIView):
#     queryset = SteerableBridgeModel.objects.all()
#     serializer_class = SteerableBridgeModelSerializer
#     permission_classes = [DjangoModelPermissions]

# class MaintenanceTypeView(ListCreateAPIView):
#     queryset = MaintenanceType.objects.all()
#     serializer_class = MaintenanceTypeSerializer
#     permission_classes = [DjangoModelPermissions]

# class SingleMaintenanceTypeView(RetrieveUpdateDestroyAPIView):
#     queryset = MaintenanceType.objects.all()
#     serializer_class = MaintenanceTypeSerializer
#     permission_classes = [DjangoModelPermissions]

# class FailureNodeView(ListCreateAPIView):
#     queryset = FailureNode.objects.all()
#     serializer_class = FailureNodeSerializer
#     permission_classes = [DjangoModelPermissions]

# class SingleFailureNodeView(RetrieveUpdateDestroyAPIView):
#     queryset = FailureNode.objects.all()
#     serializer_class = FailureNodeSerializer
#     permission_classes = [DjangoModelPermissions]

# class RecoveryMethodView(ListCreateAPIView):
#     queryset = RecoveryMethod.objects.all()
#     serializer_class = RecoveryMethodSerializer
#     permission_classes = [DjangoModelPermissions]

# class SingleRecoveryMethodView(RetrieveUpdateDestroyAPIView):
#     queryset = RecoveryMethod.objects.all()
#     serializer_class = RecoveryMethodSerializer
#     permission_classes = [DjangoModelPermissions]

# class CarSimpleListAPIView(ListAPIView):
#     queryset = Car.objects.all()
#     serializer_class = CarSerializerSimple
#     ordering = ["factory_shipment_date",]
#     # permission_classes = [NOT(IsAuthenticated)]

#     def get_queryset(self):
#         return get_simple_car_queryset(self.request, True)

# class CarView(ListCreateAPIView):
#     # queryset = Car.objects.all()
#     serializer_class = CarSerializer
#     permission_classes = [DjangoModelPermissions]
#     ordering = ["factory_shipment_date",]

#     # def get_queryset(self):
#     #     return get_car_queryset(self.request, True, True)

#     def get_queryset(self):
#         return get_car_queryset(self.request, False, True)

#     def is_visible_car(self, user, car):
#         if not user:
#             return False
        
#         # return True

#         if Client.is_own(user):
#             return user.client.id == car['client']
#             # return User.objects.filter(client__id=car['client']).exists()
#             # return user.client.id == car['client']
        
#         if ServiceCompany.is_own(user):
#             # print("car_num = ", car['car_num'])
#             # return User.objects.filter(service_company__id=car['service_company']).exists()
#             # print("car__service_company = ", car['service_company'])
#             return user.service_company.id == car['service_company']
        
#         if Manager.is_own(user):
#             return True
        
#         return False


#     # def list(self, request, *args, **kwargs):
#     #     response = super().list(request, *args, **kwargs)

#     #     # hide foreign cars
#     #     for car in response.data:
#     #         # rec = Car.objects.get(id=car['id'])
#     #         if not self.is_visible_car(request.user, car):
#     #             # print('invisible car = ', car)
#     #             car['supply_agreement'] = "<classified>"
#     #             car['factory_shipment_date'] = "<classified>"
#     #             car['consignee'] = "<classified>"
#     #             car['shipment_address'] = "<classified>"
#     #             car['add_options'] = "<classified>"
#     #             car['client__name'] = "<classified>"
#     #             car['client'] = -1
#     #             car['service_company__name'] = "<classified>"
#     #             car['service_company'] = -1

#     #     return response

# class SingleCarView(RetrieveUpdateDestroyAPIView):
#     # queryset = Car.objects.all()
#     serializer_class = CarSerializer
#     permission_classes = [DjangoModelPermissions]

#     def get_queryset(self):
#         return get_car_queryset(self.request, False, False)
  
# class MaintenanceView(ListCreateAPIView):
#     serializer_class = MaintenanceSerializer
#     permission_classes = [DjangoModelPermissions]
#     ordering = ["maintenance_date",]

#     def get_queryset(self):
#         return get_maintenance_queryset(self.request, True)
    
# class SingleMaintenanceView(RetrieveUpdateDestroyAPIView):
#     serializer_class = MaintenanceSerializer
#     permission_classes = [DjangoModelPermissions]

#     def get_queryset(self):
#         return get_maintenance_queryset(self.request, False)
    
# class ReclamationView(ListCreateAPIView):
#     serializer_class = ReclamationSerializer
#     permission_classes = [DjangoModelPermissions]
#     ordering = ["failure_date",]

#     def get_queryset(self):
#         return get_reclamation_queryset(self.request, True)
    
# class SingleReclamationView(RetrieveUpdateDestroyAPIView):
#     serializer_class = ReclamationSerializer
#     permission_classes = [DjangoModelPermissions]
    
#     def get_queryset(self):
#         return get_reclamation_queryset(self.request, False)