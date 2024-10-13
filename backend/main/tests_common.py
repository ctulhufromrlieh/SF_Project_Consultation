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

    # def login(self, username, password):
    #     user = User.objects.get(username=username)
    #     self.token = Token.objects.create(user=user)
    #     self.token.save()
        
    # def logout(self):
    #     Token.objects.all().delete()

    def login(self, username, password):
        self.token = get_token_for_user(username, password)
        # print(self.token)
        
    def logout(self):
        self.token = ""

    def get_headers(self):
        if (self.token):
            # return {
            #     "Authorization": f"Token {self.token}"
            # }
            return {
                "Authorization": f"Bearer {self.token}"
            }
        else:
            return None

    # @staticmethod
    # def is_users_equal(obj, dict):
    #     return (
    #         (obj.pk == dict["id"]) and
    #         (obj.username == dict["username"]) and
    #         (get_user_type_caption(obj) == dict["user_type_caption"])
    #     )

    # @staticmethod
    # def is_clients_equal(obj, dict):
    #     return (
    #         (obj.pk == dict["id"]) and
    #         (obj.name == dict["name"])
    #     )

    # @staticmethod
    # def is_specialists_equal(obj, dict):
    #     return (
    #         (obj.pk == dict["id"]) and
    #         (obj.name == dict["name"])
    #     )

    # @staticmethod
    # def is_admins_equal(obj, dict):
    #     return (
    #         (obj.pk == dict["id"]) and
    #         (obj.name == dict["name"])
    #     )
    
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

        # if obj.cancel_type:
        #     cancel_type_id = obj.cancel_type.pk
        # else:
        #     # cancel_type_id = -1
        #     cancel_type_id = None

        # dict_datetime1 = datetime.strptime(f"{dict['datetime1']} +00:00", "%Y-%m-%d %H:%M:%S %z")
        # dict_datetime2 = datetime.strptime(f"{dict['datetime2']} +00:00", "%Y-%m-%d %H:%M:%S %z")
        dict_datetime1 = str_to_datetime(dict["datetime1"], "+00:00")
        dict_datetime2 = str_to_datetime(dict["datetime2"], "+00:00")

        # print(dict)

        # print(f'obj.pk == dict["id"]=>{obj.pk} == {dict["id"]}=>{obj.pk == dict["id"]}')
        # # print(f'client_id == dict["client"]=>{client_id} == {dict["client"]}=>{client_id == dict["client"]}')
        # print(f'client_id == dict["client"]=>{client_id} == {dict.get("client", None)}=>{client_id == dict.get("client", None)}')
        # # print(f'specialist_id == dict["specialist"]=>{specialist_id} == {dict["specialist"]}=>{specialist_id == dict["specialist"]}')
        # print(f'specialist_id == dict["specialist"]=>{specialist_id} == {dict.get("specialist", None)}=>{specialist_id == dict.get("specialist", None)}')
        # print(f'type_id == dict["type"]=>{type_id} == {dict["type"]}=>{type_id == dict["type"]}')
        # print(f'obj.title == dict["title"]=>{obj.title} == {dict["title"]}=>{obj.title == dict["title"]}')
        # print(f'obj.datetime1==dict_datetime1=>{obj.datetime1}=={dict_datetime1}=>{obj.datetime1==dict_datetime1}')
        # print(f'obj.datetime2==dict_datetime2=>{obj.datetime2}=={dict_datetime2}=>{obj.datetime2==dict_datetime2}')
        # print(f'obj.description==dict["description"]=>{obj.description}=={dict["description"]}=>{obj.description==dict["description"]}')
        # print(f'obj.cost==dict["cost"]=>{obj.cost}=={dict["cost"]}=>{obj.cost==dict["cost"]}')
        # # print(f'obj.status==dict["status"]=>{obj.status}=={dict["status"]}=>{obj.status==dict["status"]}')
        # # print(f'cancel_type_id==dict["cancel_type"]=>{cancel_type_id}=={dict["cancel_type"]}=>{cancel_type_id==dict["cancel_type"]}')
        # # print(f'obj.cancel_comment==dict["cancel_comment"]=>{obj.cancel_comment}=={dict["cancel_comment"]}=>{obj.cancel_comment==dict["cancel_comment"]}')

        return (
            (obj.pk == dict["id"]) and
            # (client_id == dict["client"]) and
            (client_id == dict.get("client", None)) and
            (specialist_id == dict["specialist"]) and
            (type_id == dict["type"]) and
            (obj.title == dict["title"]) and
            (obj.datetime1 == dict_datetime1) and
            (obj.datetime2 == dict_datetime2) and
            # (obj.datetime1 == dict["datetime1"]) and
            # (obj.datetime2 == dict["datetime2"]) and
            (obj.description == dict["description"]) and
            (obj.cost == dict["cost"]) and
            (obj.is_accepted == dict["is_accepted"]) 
            # (obj.status == dict["status"]) and
            # (cancel_type_id == dict["cancel_type"]) and
            # (obj.cancel_comment == dict["cancel_comment"])
        )

    def check_get_simple(self, loc_url, status_code, response_field_name, response_field_text, data={}):
        url = self.base_url + loc_url
        headers = self.get_headers()
        data = {}
        # response = self.client.get(url, data, headers=headers, format='json')
        response = self.client.get(url, data, headers=headers)
        # print("url:")
        # print(url)
        # print("headers:")
        # print(headers)
        # print("response.content:")
        # print(response.content)
        # print("response.status_code:")
        # print(response.status_code)
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status_code)
        if response_field_name:
            self.assertEqual(json_response[response_field_name], response_field_text)
        # print("json_response:")
        # print(json_response)

    def check_post_simple(self, loc_url, status_code, response_field_name, response_field_text, data={}):
        url = self.base_url + loc_url
        headers = self.get_headers()
        
    
        response = self.client.post(url, data, headers=headers)
        # print("url:")
        # print(url)
        # print("headers:")
        # print(headers)
        # print("response.content:")
        # print(response.content)           
        # print("response.status_code:")
        # print(response.status_code)
        if not (response.status_code == 404):
            json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status_code)
        if response_field_name:
            self.assertEqual(json_response[response_field_name], response_field_text)

    def check_put_simple(self, loc_url, status_code, response_field_name, response_field_text, data={}):
        url = self.base_url + loc_url
        headers = self.get_headers()
        
        # print("check_put_simple:")
        response = self.client.put(url, data, headers=headers)
        
        if not (response.status_code == 404):
            json_response = json.loads(response.content)

        # print(json_response)

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
        # create_example_database_only_users_1()
        create_example_database_1()

        self.login(self.username, self.password)

    def tearDown(self) -> None:
        super().tearDown()
        self.logout()

# # based on https://stackoverflow.com/questions/63046840/getting-user-details-from-access-token-in-django-rest-framework-simple-jwt
# def get_user_from_access_token_in_django_rest_framework_simplejwt(access_token_str):
#     access_token_obj = AccessToken(access_token_str)
#     user_id=access_token_obj['user_id']
#     user=User.objects.get(id=user_id)
#     print('user_id: ', user_id )
#     print('user: ', user)
#     print('user.id: ', user.id )
#     content =  {'user_id': user_id, 'user':user, 'user.id':user.id}
#     return Response(content)

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
    # # Groups
    # group_clients, created = Group.objects.get_or_create(name="clients")
    # group_specialists, created = Group.objects.get_or_create(name="specialists")
    # group_admins, created = Group.objects.get_or_create(name="admins")

    User.objects.exclude(username="admin").delete()

    # Clients
    # Client.objects.all().delete()

    create_client(name='Вася Пупкин', username="client1", email="client1@clients.aa", password="client1psw")
    create_client(name='Иван Петров', username="client2", email="client2@clients.bb", password="client2psw")

    # Specialists
    # Specialist.objects.all().delete()

    create_specialist(name="Проффффессор", username="spec1", email="spec1@specialists.aa", password="spec1psw")
    create_specialist(name="Доцент", username="spec2", email="spec2@specialists.bb", password="spec2psw")

    # Admins
    # Admin.objects.all().delete()

    create_admin(name="ГлавАдмин", username="admin1", email="admin1@admins.aa", password="admin1psw")
    create_admin(name="Почти главный админ", username="admin2", email="admin2@admins.bb", password="admin2psw")

def create_example_database_1():
    create_example_database_only_users_1()

    # client1 = Client.objects.get(user__username="client1")
    # client2 = Client.objects.get(user__username="client2")
    client1 = User.objects.get(username="client1")
    client2 = User.objects.get(username="client2")

    # spec1 = Specialist.objects.get(user__username="spec1")
    # spec2 = Specialist.objects.get(user__username="spec2")
    spec1 = User.objects.get(username="spec1")
    spec2 = User.objects.get(username="spec2")

    # # admin1 = Admin.objects.get(user__username="admin1")
    # # admin2 = Admin.objects.get(user__username="admin2")

    # ConsultType
    ConsultType.objects.all().delete()

    cot1 = ConsultType.objects.create(name="Математика")
    cot2 = ConsultType.objects.create(name="Физика")

    # # CancelType
    # CancelType.objects.all().delete()

    # cat1 = CancelType.objects.create(name="Другая")
    # cat2 = CancelType.objects.create(name="Передумал")
    # cat3 = CancelType.objects.create(name="Забыл")
    # ReasonType
    ReasonType.objects.all().delete()

    rt1 = ReasonType.objects.create(name="Другая")
    rt2 = ReasonType.objects.create(name="Передумал")
    rt3 = ReasonType.objects.create(name="Забыл")

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
