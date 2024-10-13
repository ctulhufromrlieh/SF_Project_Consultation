# Generated by Django 4.2.15 on 2024-10-10 19:43

from django.db import migrations

app_names = ["clients", "specialists", "admins"]

# Evil hack - for making custom permissions before this
# Except block based on https://code.djangoproject.com/ticket/23422
def make_permissions(apps, schema_editor, with_create_permissions=True):
    Group = apps.get_model("auth", "Group")
    clients, created_clients = Group.objects.get_or_create(name="clients")
    specialists, created_specialists = Group.objects.get_or_create(name="specialists")
    admins, created_admins = Group.objects.get_or_create(name="admins")

    Permission = apps.get_model("auth", "Permission")

    try:
        clients.permissions.add(Permission.objects.get(content_type__app_label="clients", codename="view_spec"))
        clients.permissions.add(Permission.objects.get(content_type__app_label="clients", codename="view_slot"))
        clients.permissions.add(Permission.objects.get(content_type__app_label="clients", codename="sign_slot"))
        clients.permissions.add(Permission.objects.get(content_type__app_label="clients", codename="unsign_slot"))
        clients.permissions.add(Permission.objects.get(content_type__app_label="clients", codename="view_slot_action"))

        specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="view_slot"))
        specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="add_slot"))
        specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="change_slot"))
        specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="delete_slot"))
        specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="accept_slot"))
        specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="decline_slot"))
        specialists.permissions.add(Permission.objects.get(content_type__app_label="specialists", codename="view_slot_action"))

        admins.permissions.add(Permission.objects.get(content_type__app_label="admins", codename="view_user"))
        admins.permissions.add(Permission.objects.get(content_type__app_label="admins", codename="change_user_status"))
    except Permission.DoesNotExist:
        if with_create_permissions:
            for curr_app_name in app_names:
                # Manually run create_permissions
                from django.contrib.auth.management import create_permissions
                # assert not getattr(apps, 'models_module', None)
                app_config = apps.get_app_config(curr_app_name)
                app_config.models_module = True
                create_permissions(app_config, verbosity=0)
                app_config.models_module = None
            
            return make_permissions(apps, schema_editor, with_create_permissions=False)
        else:
            raise


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('clients', '0001_initial'),
        ('specialists', '0002_alter_specialistpermissions_options'),
        ('admins', '0002_alter_adminpermissions_options'),
        ('main', '0012_remove_client_user_remove_specialist_user_and_more'),
    ]

    operations = [
        migrations.RunPython(make_permissions),
    ]
