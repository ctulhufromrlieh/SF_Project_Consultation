from django.contrib.auth.models import Group, User

def create_client(name, username, email, password):
    user = User.objects.create_user(username=username, password=password, email=email, first_name=name)
    clients_group = Group.objects.get(name='clients')
    user.groups.add(clients_group)

    return user

def create_specialist(name, username, email, password):
    user = User.objects.create_user(username=username, password=password, email=email, first_name=name)
    specialists_group = Group.objects.get(name='specialists')
    user.groups.add(specialists_group)

    return user

def create_admin(name, username, email, password):
    user = User.objects.create_user(username=username, password=password, email=email, first_name=name)
    admins_group = Group.objects.get(name='admins')
    user.groups.add(admins_group)

    return user
