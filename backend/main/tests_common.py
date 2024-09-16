import json

from main.models import *
from main.debug_helpers import *
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

class BaseTest(APITestCase):
    base_url = ""
    token = ""

    def login(self, username, password):
        user = User.objects.get(username=username)
        self.token = Token.objects.create(user=user)
        self.token.save()
        
    def logout(self):
        Token.objects.all().delete()

    def get_headers(self):
        if (self.token):
            return {
                "Authorization": f"Token {self.token}"
            }
        else:
            return None
        
    def check_get_simple(self, loc_url, status_code, response_field_name, response_field_text):
        url = self.base_url + loc_url
        headers = self.get_headers()
        data = {}
        response = self.client.get(url, data, headers=headers, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status_code)
        if response_field_name:
            self.assertEqual(json_response[response_field_name], response_field_text)
        # print("json_response:")
        # print(json_response)

    def check_post_simple(self, loc_url, status_code, response_field_name, response_field_text):
        url = self.base_url + loc_url
        headers = self.get_headers()
        data = {}
        response = self.client.post(url, data, headers=headers, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status_code)
        if response_field_name:
            self.assertEqual(json_response[response_field_name], response_field_text)

class AnonymousBaseTest(BaseTest):
    status_code = 403
    response_field_name = "detail"
    response_field_text = "Authentication credentials were not provided."

    def check_get_status(self, loc_url):
        self.check_get_simple(loc_url, self.status_code, self.response_field_name, self.response_field_text)

    def check_post_status(self, loc_url):
        self.check_post_simple(loc_url, self.status_code, self.response_field_name, self.response_field_text)

class ForbiddenBaseTest(BaseTest):
    status_code = 403
    response_field_name = "detail"
    response_field_text = "You do not have permission to perform this action."

    username = ""
    password = ""

    def check_get_status(self, loc_url):
        self.check_get_simple(loc_url, self.status_code, self.response_field_name, self.response_field_text)

    def check_post_status(self, loc_url):
        self.check_post_simple(loc_url, self.status_code, self.response_field_name, self.response_field_text)

    def setUp(self) -> None:
        super().setUp()
        create_example_database_only_users_1()

        self.login(self.username, self.password)

    def tearDown(self) -> None:
        super().tearDown()
        self.logout()

class SuccessBaseTest(BaseTest):
    status_code = 200
    response_field_name = ""
    response_field_text = ""

    username = ""
    password = ""

    def check_get_status(self, loc_url):
        self.check_get_simple(loc_url, self.status_code, self.response_field_name, self.response_field_text)

    def check_post_status(self, loc_url):
        self.check_post_simple(loc_url, self.status_code, self.response_field_name, self.response_field_text)

    def setUp(self) -> None:
        super().setUp()
        # create_example_database_only_users_1()
        create_example_database_1()

        self.login(self.username, self.password)

    def tearDown(self) -> None:
        super().tearDown()
        self.logout()


def create_example_database_only_users_1():
    # Groups
    group_clients, created = Group.objects.get_or_create(name="clients")
    group_specialists, created = Group.objects.get_or_create(name="specialists")
    group_admins, created = Group.objects.get_or_create(name="admins")

    User.objects.exclude(username="admin").delete()

    # Clients
    Client.objects.all().delete()

    create_client(name='Вася Пупкин', username="client1", email="client1@clients.aa", password="client1psw")
    create_client(name='Иван Петров', username="client2", email="client2@clients.bb", password="client2psw")

    # Specialists
    Specialist.objects.all().delete()

    create_specialist(name="Проффффессор", username="spec1", email="spec1@specialists.aa", password="spec1psw")
    create_specialist(name="Доцент", username="spec2", email="spec2@specialists.bb", password="spec2psw")

    # Admins
    Admin.objects.all().delete()

    create_admin(name="ГлавАдмин", username="admin1", email="admin1@admins.aa", password="admin11psw")
    create_admin(name="Почти главный админ", username="admin2", email="admin2@admins.bb", password="admin2psw")

def create_example_database_1():
    create_example_database_only_users_1()

    client1 = Client.objects.get(user__username="client1")
    client2 = Client.objects.get(user__username="client2")

    spec1 = Specialist.objects.get(user__username="spec1")
    spec2 = Specialist.objects.get(user__username="spec2")

    # admin1 = Admin.objects.get(user__username="admin1")
    # admin2 = Admin.objects.get(user__username="admin2")

    # ConsultType
    ConsultType.objects.all().delete()

    cot1 = ConsultType.objects.create(name="Математика")
    cot2 = ConsultType.objects.create(name="Физика")

    # CancelType
    CancelType.objects.all().delete()

    cat1 = CancelType.objects.create(name="Другая")
    cat2 = CancelType.objects.create(name="Передумал")
    cat3 = CancelType.objects.create(name="Забыл")

    # Slots
    Slot.objects.all().delete()

    slot1 = Slot.objects.create(client=client1, specialist=spec1, type=cot1, title="Проффффессор - Математика", 
        datetime1="2024-01-10 10:00 +03:00", datetime2="2024-01-10 12:00 +03:00", description="Консультация: Проффффессор - Математика")
    slot2 = Slot.objects.create(client=client2, specialist=spec1, type=cot1, title="Проффффессор - Математика", 
        datetime1="2024-01-10 12:00 +03:00", datetime2="2024-01-10 14:00 +03:00", description="Консультация: Проффффессор - Математика")
    slot3 = Slot.objects.create(client=None, specialist=spec1, type=cot1, title="Проффффессор - Математика", 
        datetime1="2024-01-10 14:00 +03:00", datetime2="2024-01-10 16:00 +03:00", description="Консультация: Проффффессор - Математика")
    slot4 = Slot.objects.create(client=client1, specialist=spec2, type=cot2, title="Доцент - Физика", 
        datetime1="2024-01-11 10:00 +03:00", datetime2="2024-01-11 12:00 +03:00", description="Консультация: Доцент - Физика")
    slot5 = Slot.objects.create(client=client2, specialist=spec2, type=cot2, title="Доцент - Физика", 
        datetime1="2024-01-11 12:00 +03:00", datetime2="2024-01-11 14:00 +03:00", description="Консультация: Доцент - Физика")
    slot6 = Slot.objects.create(client=None, specialist=spec2, type=cot2, title="Доцент - Физика", 
        datetime1="2024-01-11 14:00 +03:00", datetime2="2024-01-11 16:00 +03:00", description="Консультация: Доцент - Физика")
