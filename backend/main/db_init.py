# from django.contrib.auth.models import User, Group, Permission

# def create_permissions():
#     print("create_permissions")
#     # Group = apps.get_model('auth', 'Group')
#     clients, created_clients = Group.objects.get_or_create(name="clients")
#     specialists, created_specialists = Group.objects.get_or_create(name="specialists")
#     admins, created_admins = Group.objects.get_or_create(name="admins")

#     # if not created_clients and not created_specialists and not created_admins:
#         # return

#     # Permission = apps.get_model('auth', 'Permission')

#     # print("Permission.objects.count()")
#     # print(Permission.objects.count())

#     print("Permission.objects.count()")
#     print(Permission.objects.count())

#     clients.permissions.add(Permission.objects.get(content_type__app_label="clients", codename="view_spec"))
#     clients.permissions.add(Permission.objects.get(content_type__app_label="clients", codename="view_slot"))
#     clients.permissions.add(Permission.objects.get(content_type__app_label="clients", codename="sign_slot"))
#     clients.permissions.add(Permission.objects.get(content_type__app_label="clients", codename="unsign_slot"))
#     clients.permissions.add(Permission.objects.get(content_type__app_label="clients", codename="view_slot_action"))

#     specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="view_slot"))
#     specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="add_slot"))
#     specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="change_slot"))
#     specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="delete_slot"))
#     specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="accept_slot"))
#     specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="decline_slot"))
#     specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="view_slot_action"))

#     admins.permissions.add(Permission.objects.get(content_type__app_label="admins", codename="view_user"))
#     admins.permissions.add(Permission.objects.get(content_type__app_label="admins", codename="change_user_status"))

# # def create_permissions():
# #     Group = apps.get_model('auth', 'Group')
# #     clients, created_clients = Group.objects.get_or_create(name="clients")
# #     specialists, created_specialists = Group.objects.get_or_create(name="specialists")
# #     admins, created_admins = Group.objects.get_or_create(name="admins")

# #     Permission = apps.get_model('auth', 'Permission')

# #     print("Permission.objects.count()")
# #     print(Permission.objects.count())

# #     clients.permissions.add(Permission.objects.get(content_type__app_label="clients", codename="view_spec"))
# #     clients.permissions.add(Permission.objects.get(content_type__app_label="clients", codename="view_slot"))
# #     clients.permissions.add(Permission.objects.get(content_type__app_label="clients", codename="sign_slot"))
# #     clients.permissions.add(Permission.objects.get(content_type__app_label="clients", codename="unsign_slot"))
# #     clients.permissions.add(Permission.objects.get(content_type__app_label="clients", codename="view_slot_action"))

# #     specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="view_slot"))
# #     specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="add_slot"))
# #     specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="change_slot"))
# #     specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="delete_slot"))
# #     specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="accept_slot"))
# #     specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="decline_slot"))
# #     specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="view_slot_action"))

# #     admins.permissions.add(Permission.objects.get(content_type__app_label="admins", codename="view_user"))
# #     admins.permissions.add(Permission.objects.get(content_type__app_label="admins", codename="change_user_status"))