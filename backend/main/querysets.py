from .models import *    

from .utils import *

# def to_int(str_value, def_value):
#     if str_value.isdigit():
#         return int(str_value)
#     else:
#         return def_value

# def get_slot_queryset(request):
#     user = request.user

#     specialist_id = -1
#     if Specialist.is_own(user):
#         specialist_id = user.specialist.id
#     else:
#         specialist_id = to_int(request.GET.get('specialist', ''), -1)

#     print("specialist=", specialist_id)

#     if specialist_id == -1:
#         return Slot.objects.none()
#     else:
#         return Slot.objects.all().filter(specialist=specialist_id)

# def get_simple_car_queryset(request, use_filter):
#     res = Car.objects.all()
    
#     if not use_filter:
#         return res

#     filter_car_num = request.GET.get('car_num', '')
#     # filter_car_model = request.GET.get('car_model', '')
#     # filter_engine_model = request.GET.get('engine_model', '')
#     # filter_transmission_model = request.GET.get('transmission_model', '')
#     # filter_main_bridge_model = request.GET.get('main_bridge_model', '')
#     # filter_steerable_bridge_model = request.GET.get('steerable_bridge_model', '')

#     if filter_car_num:
#         res = res.filter(car_num__icontains=filter_car_num)

#     return res

# def get_car_queryset(request, is_all, use_filter):
#     res = Car.objects.all()
    
#     user = request.user

#     if not is_all:
#         # if user.client:
#         if Client.is_own(user):
#             res = res.filter(client__user=user)
#         # if user.service_company:
#         elif ServiceCompany.is_own(user):
#             res = res.filter(service_company__user=user)       
#         # if user.manager:
#         elif Manager.is_own(user):
#             res = res  # if user is manager - no user filtering
#         elif user.is_staff:
#             res = res  # if user is admin - no user filtering
#         else:
#             return Car.objects.none()  # if user is out of these groups - get nothing
#     else:
#         if not Client.is_own(user) and not ServiceCompany.is_own(user) and not Manager.is_own(user) and not user.is_staff:
#         # if not (user.client or user.service_company or user.manager):
#             return Car.objects.none()  # if user is out of these groups - get nothing

#     if not use_filter:
#         return res

#     filter_car_num = request.GET.get('car_num', '')
#     filter_car_model = request.GET.get('car_model', '')
#     filter_engine_model = request.GET.get('engine_model', '')
#     filter_transmission_model = request.GET.get('transmission_model', '')
#     filter_main_bridge_model = request.GET.get('main_bridge_model', '')
#     filter_steerable_bridge_model = request.GET.get('steerable_bridge_model', '')

#     if filter_car_num:
#         res = res.filter(car_num__icontains=filter_car_num)
    
#     if filter_car_model:
#         filter_car_model_i = to_int(filter_car_model, -1)
#         if filter_car_model_i != -1:
#             res = res.filter(car_model=filter_car_model_i)
    
#     if filter_engine_model:
#         filter_engine_model_i = to_int(filter_engine_model, -1)
#         if filter_engine_model_i != -1:
#             res = res.filter(engine_model=filter_engine_model_i)
    
#     if filter_transmission_model:
#         filter_transmission_model_i = to_int(filter_transmission_model, -1)
#         if filter_transmission_model_i != -1:
#             res = res.filter(transmission_model=filter_transmission_model_i)
    
#     if filter_main_bridge_model:
#         filter_main_bridge_model_i = to_int(filter_main_bridge_model, -1)
#         if filter_main_bridge_model_i != -1:
#             res = res.filter(main_bridge_model=filter_main_bridge_model_i)
    
#     if filter_steerable_bridge_model:
#         filter_steerable_bridge_model_i = to_int(filter_steerable_bridge_model, -1)
#         if filter_steerable_bridge_model_i != -1:
#             res = res.filter(steerable_bridge_model=filter_steerable_bridge_model_i)

#     return res

# def get_maintenance_queryset(request, use_filter):
#     res = Maintenance.objects.all()

#     user = request.user

#     # if user.client:
#     if Client.is_own(user):
#         res = res.filter(car__client__user=user)
#     # if user.service_company:
#     elif ServiceCompany.is_own(user):
#         res = res.filter(service_company__user=user)
#     elif Manager.is_own(user):
#         res = res  # if user is manager - no user filtering
#     elif user.is_staff:
#         res = res  # if user is admin - no user filtering        
#     else:
#         return Maintenance.objects.none()  # if user is out of these groups - get nothing

#     if not use_filter:
#         return res

#     filter_car_num = request.GET.get('car_num', '')
#     # filter_service_company__name = request.GET.get('service_company', '')
#     filter_service_company__name = request.GET.get('service_company__name', '')
#     filter_type = request.GET.get('type', '')
    

#     if filter_car_num:
#         res = res.filter(car__car_num__icontains=filter_car_num)

#     if filter_service_company__name:
#         if filter_service_company__name == "<none>":
#             res = res.filter(service_company__name__iexact=None)
#         else:
#             res = res.filter(service_company__name__icontains=filter_service_company__name)

#     if filter_type:
#         filter_type_i = to_int(filter_type, -1)
#         if filter_type_i != -1:
#             res = res.filter(type=filter_type_i)

#     return res

# def get_reclamation_queryset(request, use_filter):
#     res = Reclamation.objects.all()

#     user = request.user

#     # if user.client:
#     if Client.is_own(user):
#         res = res.filter(car__client__user=user)
#     # if user.service_company:
#     elif ServiceCompany.is_own(user):
#         res = res.filter(car__service_company__user=user)
#     # if user.manager:
#     elif Manager.is_own(user):
#         res = res  # if user is manager - no user filtering
#     elif user.is_staff:
#         res = res  # if user is admin - no user filtering
#     else:
#         return Reclamation.objects.none()  # if user is out of these groups - get nothing

#     if not use_filter:
#         return res

#     filter_car_num = request.GET.get('car_num', '')
#     # filter_service_company__name = request.GET.get('service_company', '')
#     filter_service_company__name = request.GET.get('service_company__name', '')
#     filter_failure_node = request.GET.get('failure_node', '')
#     filter_recovery_method = request.GET.get('recovery_method', '')

#     if filter_car_num:
#         res = res.filter(car__car_num__icontains=filter_car_num)

#     if filter_service_company__name:
#         res = res.filter(car__service_company__name__icontains=filter_service_company__name)

#     if filter_failure_node:
#         filter_failure_node_i = to_int(filter_failure_node, -1)
#         if filter_failure_node_i != -1:
#             res = res.filter(failure_node=filter_failure_node_i)

#     if filter_recovery_method:
#         filter_recovery_method_i = to_int(filter_recovery_method, -1)
#         if filter_recovery_method_i != -1:
#             res = res.filter(recovery_method=filter_recovery_method_i)

#     return res