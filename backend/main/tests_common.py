import json
from datetime import datetime

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

    @staticmethod
    def is_clients_equal(obj, dict):
        return (
            (obj.pk == dict["id"]) and
            (obj.name == dict["name"])
        )

    @staticmethod
    def is_specialists_equal(obj, dict):
        return (
            (obj.pk == dict["id"]) and
            (obj.name == dict["name"])
        )

    @staticmethod
    def is_admins_equal(obj, dict):
        return (
            (obj.pk == dict["id"]) and
            (obj.name == dict["name"])
        )
    
    @staticmethod
    def is_slots_equal(obj, dict):
        if obj.client:
            client_id = obj.client.pk
        else:
            # client_id = -1
            client_id = None

        if obj.specialist:
            specialist_id = obj.specialist.pk
        else:
            # specialist_id = -1
            specialist_id = None

        if obj.type:
            type_id = obj.type.pk
        else:
            # type_id = -1
            type_id = None

        if obj.cancel_type:
            cancel_type_id = obj.cancel_type.pk
        else:
            # cancel_type_id = -1
            cancel_type_id = None

        dict_datetime1 = datetime.strptime(f"{dict['datetime1']} +00:00", "%Y-%m-%d %H:%M:%S %z")
        dict_datetime2 = datetime.strptime(f"{dict['datetime2']} +00:00", "%Y-%m-%d %H:%M:%S %z")

        # print(dict)

        # print(f'obj.pk == dict["id"]=>{obj.pk} == {dict["id"]}=>{obj.pk == dict["id"]}')
        # print(f'client_id == dict["client"]=>{client_id} == {dict["client"]}=>{client_id == dict["client"]}')
        # print(f'specialist_id == dict["specialist"]=>{specialist_id} == {dict["specialist"]}=>{specialist_id == dict["specialist"]}')
        # print(f'type_id == dict["type"]=>{type_id} == {dict["type"]}=>{type_id == dict["type"]}')
        # print(f'obj.title == dict["title"]=>{obj.title} == {dict["title"]}=>{obj.title == dict["title"]}')
        # print(f'obj.datetime1==dict_datetime1=>{obj.datetime1}=={dict_datetime1}=>{obj.datetime1==dict_datetime1}')
        # print(f'obj.datetime2==dict_datetime2=>{obj.datetime2}=={dict_datetime2}=>{obj.datetime2==dict_datetime2}')
        # print(f'obj.description==dict["description"]=>{obj.description}=={dict["description"]}=>{obj.description==dict["description"]}')
        # print(f'obj.cost==dict["cost"]=>{obj.cost}=={dict["cost"]}=>{obj.cost==dict["cost"]}')
        # print(f'obj.status==dict["status"]=>{obj.status}=={dict["status"]}=>{obj.status==dict["status"]}')
        # print(f'cancel_type_id==dict["cancel_type"]=>{cancel_type_id}=={dict["cancel_type"]}=>{cancel_type_id==dict["cancel_type"]}')
        # print(f'obj.cancel_comment==dict["cancel_comment"]=>{obj.cancel_comment}=={dict["cancel_comment"]}=>{obj.cancel_comment==dict["cancel_comment"]}')

        return (
            (obj.pk == dict["id"]) and
            (client_id == dict["client"]) and
            (specialist_id == dict["specialist"]) and
            (type_id == dict["type"]) and
            (obj.title == dict["title"]) and
            (obj.datetime1 == dict_datetime1) and
            (obj.datetime2 == dict_datetime2) and
            # (obj.datetime1 == dict["datetime1"]) and
            # (obj.datetime2 == dict["datetime2"]) and
            (obj.description == dict["description"]) and
            (obj.cost == dict["cost"]) and
            (obj.status == dict["status"]) and
            (cancel_type_id == dict["cancel_type"]) and
            (obj.cancel_comment == dict["cancel_comment"])
        )

    def check_get_simple(self, loc_url, status_code, response_field_name, response_field_text, data={}):
        url = self.base_url + loc_url
        headers = self.get_headers()
        data = {}
        # response = self.client.get(url, data, headers=headers, format='json')
        response = self.client.get(url, data, headers=headers)
        # print("url:")
        # print(url)
        # print("response.content:")
        # print(response.content)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status_code)
        if response_field_name:
            self.assertEqual(json_response[response_field_name], response_field_text)
        # print("json_response:")
        # print(json_response)

    def check_post_simple(self, loc_url, status_code, response_field_name, response_field_text, data={}):
        url = self.base_url + loc_url
        headers = self.get_headers()
        # data = {}
        # print(data)
        
        # response = self.client.post(url, data, headers=headers, format='json')
        response = self.client.post(url, data, headers=headers)
        # print(response.content)
        # response = self.client.post(url, json.dumps(data), headers=headers, format='json')
        
        if not (response.status_code == 404):
            json_response = json.loads(response.content)

        # print(f"<{loc_url}>: response.status_code = {response.status_code}")
        self.assertEqual(response.status_code, status_code)
        if response_field_name:
            self.assertEqual(json_response[response_field_name], response_field_text)

    def get_simple(self, loc_url, data={}):
        url = self.base_url + loc_url
        headers = self.get_headers()
        # data = {}
        # response = self.client.get(url, data, headers=headers, format='json')
        response = self.client.get(url, data, headers=headers)
        json_response = json.loads(response.content)

        return {
            'status_code': response.status_code,
            'data':  json_response
        }

    def post_simple(self, loc_url, data={}):
        url = self.base_url + loc_url
        headers = self.get_headers()
        # data = {}
        # response = self.client.post(url, data, headers=headers, format='json')
        response = self.client.post(url, data, headers=headers)
        json_response = json.loads(response.content)

        return {
            'status_code': response.status_code,
            'data':  json_response
        }

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

    # print("Cancel type ids:")
    # print(cat1.pk)
    # print(cat2.pk)
    # print(cat3.pk)

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
