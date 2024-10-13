import json
from datetime import datetime

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from rest_framework_simplejwt.tokens import AccessToken, AuthUser

from main.models import *
from main.debug_helpers import *
from main.utils import *

class BaseTest(APITestCase):
    base_url = ""
    token = ""
        
    def login(self, username, password):
        self.token = get_token_for_user(username, password)
        
    def logout(self):
        self.token = ""

    def get_headers(self):
        if (self.token):
            return {
                "Authorization": f"Bearer {self.token}"
            }
        else:
            return None

    @staticmethod
    def is_users_equal(obj, dict):
        return (
            (obj.pk == dict["id"]) and
            (obj.username == dict["username"]) and
            (obj.first_name == dict["first_name"]) and
            (obj.last_name == dict["last_name"])
        )

    @staticmethod
    def is_slots_equal(obj, dict):
        if obj.client:
            client_id = obj.client.pk
        else:
            client_id = None

        if obj.specialist:
            specialist_id = obj.specialist.pk
        else:
            specialist_id = None

        if obj.type:
            type_id = obj.type.pk
        else:
            type_id = None

        dict_datetime1 = str_to_datetime(dict["datetime1"], "+00:00")
        dict_datetime2 = str_to_datetime(dict["datetime2"], "+00:00")

        return (
            (obj.pk == dict["id"]) and
            (client_id == dict.get("client", None)) and
            (specialist_id == dict["specialist"]) and
            (type_id == dict["type"]) and
            (obj.title == dict["title"]) and
            (obj.datetime1 == dict_datetime1) and
            (obj.datetime2 == dict_datetime2) and
            (obj.description == dict["description"]) and
            (obj.cost == dict["cost"]) and
            (obj.is_accepted == dict["is_accepted"]) 
        )

    def check_get_simple(self, loc_url, status_code, response_field_name, response_field_text, data={}):
        url = self.base_url + loc_url
        headers = self.get_headers()
        data = {}
        
        response = self.client.get(url, data, headers=headers)
        if not (response.status_code == 404):
            json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status_code)
        if response_field_name:
            self.assertEqual(json_response[response_field_name], response_field_text)

    def check_post_simple(self, loc_url, status_code, response_field_name, response_field_text, data={}):
        url = self.base_url + loc_url
        headers = self.get_headers()

        response = self.client.post(url, data, headers=headers)
        if not (response.status_code == 404):
            json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status_code)
        if response_field_name:
            self.assertEqual(json_response[response_field_name], response_field_text)

    def check_put_simple(self, loc_url, status_code, response_field_name, response_field_text, data={}):
        url = self.base_url + loc_url
        headers = self.get_headers()
        
        response = self.client.put(url, data, headers=headers)
        if not (response.status_code == 404):
            json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status_code)
        if response_field_name:
            self.assertEqual(json_response[response_field_name], response_field_text)

    def check_patch_simple(self, loc_url, status_code, response_field_name, response_field_text, data={}):
        url = self.base_url + loc_url
        headers = self.get_headers()
        
        response = self.client.patch(url, data, headers=headers)
        if not (response.status_code == 404):
            json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status_code)
        if response_field_name:
            self.assertEqual(json_response[response_field_name], response_field_text)

    def check_delete_simple(self, loc_url, status_code, data={}):
        url = self.base_url + loc_url
        headers = self.get_headers()
        
        response = self.client.delete(url, data, headers=headers)
        
        self.assertEqual(response.status_code, status_code)

    def get_simple(self, loc_url, data={}):
        url = self.base_url + loc_url
        headers = self.get_headers()

        response = self.client.get(url, data, headers=headers)
        json_response = json.loads(response.content)

        return {
            'status_code': response.status_code,
            'data':  json_response
        }

    def post_simple(self, loc_url, data={}):
        url = self.base_url + loc_url
        headers = self.get_headers()

        response = self.client.post(url, data, headers=headers)
        json_response = json.loads(response.content)

        return {
            'status_code': response.status_code,
            'data':  json_response
        }

class AnonymousBaseTest(BaseTest):
    # status_code = 403
    status_code = 401
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
        create_example_database_1()

        self.login(self.username, self.password)

    def tearDown(self) -> None:
        super().tearDown()
        self.logout()

# based on https://stackoverflow.com/questions/63046840/getting-user-details-from-access-token-in-django-rest-framework-simple-jwt
def get_user_from_access_token(access_token_str):
    access_token_obj = AccessToken(access_token_str)
    user_id=access_token_obj['user_id']
    user=User.objects.get(id=user_id)
    return user

def get_token_for_user(username, password):
    user = User.objects.filter(username=username).first()
    if user:
        return AccessToken.for_user(user)
    else:
        return None

def create_example_database_only_users_1():
    # User.objects.exclude(username="admin").delete()
    User.objects.all().delete()

    # Superuser
    user=User.objects.create_user('admin', password='admin')
    user.is_superuser=True
    user.is_staff=True
    user.save()

    # Clients
    create_client(name='Вася Пупкин', username="client1", email="client1@clients.aa", password="client1psw")
    create_client(name='Иван Петров', username="client2", email="client2@clients.bb", password="client2psw")

    # Specialists
    create_specialist(name="Проффффессор", username="spec1", email="spec1@specialists.aa", password="spec1psw")
    create_specialist(name="Доцент", username="spec2", email="spec2@specialists.bb", password="spec2psw")

    # Admins
    create_admin(name="ГлавАдмин", username="admin1", email="admin1@admins.aa", password="admin1psw")
    create_admin(name="Почти главный админ", username="admin2", email="admin2@admins.bb", password="admin2psw")

def create_example_database_1():
    create_example_database_only_users_1()

    client1 = User.objects.get(username="client1")
    client2 = User.objects.get(username="client2")

    spec1 = User.objects.get(username="spec1")
    spec2 = User.objects.get(username="spec2")

    # ConsultType
    ConsultType.objects.all().delete()

    cot1 = ConsultType.objects.create(name="Математика")
    cot2 = ConsultType.objects.create(name="Физика")

    # ReasonType
    ReasonType.objects.all().delete()

    rt1 = ReasonType.objects.create(name="Другая")
    rt2 = ReasonType.objects.create(name="Передумал")
    rt3 = ReasonType.objects.create(name="Забыл")

    # Slots
    Slot.objects.all().delete()

    slot1 = Slot.objects.create(client=client1, specialist=spec1, type=cot1, title="Проффффессор - Математика", 
        datetime1="2024-01-10 10:00+03:00", datetime2="2024-01-10 12:00 +03:00", description="Консультация: Проффффессор - Математика")
    slot2 = Slot.objects.create(client=client2, specialist=spec1, type=cot1, title="Проффффессор - Математика", 
        datetime1="2024-01-10 12:00+03:00", datetime2="2024-01-10 14:00 +03:00", description="Консультация: Проффффессор - Математика")
    slot3 = Slot.objects.create(client=None, specialist=spec1, type=cot1, title="Проффффессор - Математика", 
        datetime1="2024-01-10 14:00+03:00", datetime2="2024-01-10 16:00 +03:00", description="Консультация: Проффффессор - Математика")
    slot4 = Slot.objects.create(client=client1, specialist=spec2, type=cot2, title="Доцент - Физика", 
        datetime1="2024-01-11 10:00+03:00", datetime2="2024-01-11 12:00 +03:00", description="Консультация: Доцент - Физика")
    slot5 = Slot.objects.create(client=client2, specialist=spec2, type=cot2, title="Доцент - Физика", 
        datetime1="2024-01-11 12:00+03:00", datetime2="2024-01-11 14:00 +03:00", description="Консультация: Доцент - Физика")
    slot6 = Slot.objects.create(client=None, specialist=spec2, type=cot2, title="Доцент - Физика", 
        datetime1="2024-01-11 14:00+03:00", datetime2="2024-01-11 16:00 +03:00", description="Консультация: Доцент - Физика")
