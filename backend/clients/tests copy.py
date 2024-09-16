# import json

# from django.test import TestCase
# from rest_framework.test import APIRequestFactory, RequestsClient, APITestCase, APIClient

# # from django.urls import reverse
# from django.contrib.auth.models import User

# # from rest_framework import status
# from rest_framework.authtoken.models import Token

# from main.tests_common import *

# # class AnonymousTests(APITestCase):
# class AnonymousTests(BaseTest):
#     base_url = "/api/v1/for_clients"

#     response_field_name = "detail"
#     response_field_text = "Authentication credentials were not provided."

#     def setUp(self) -> None:
#         super().setUp()

#     def tearDown(self) -> None:
#         super().tearDown()

#     def test_specialist_list(self):
#         self.check_get_simple("/specialists", 403, self.response_field_name, self.response_field_text)
    
#     def test_specialist_one_1(self):
#         self.check_get_simple("/specialists/1", 403, self.response_field_name, self.response_field_text)

#     def test_slot_list(self):
#         self.check_get_simple("/slots", 403, self.response_field_name, self.response_field_text)

#     def test_slot_one_1(self):
#         self.check_get_simple("/slots/1", 403, self.response_field_name, self.response_field_text)

#     # def test_specialist_list(self):
#     #     url = self.base_url + "/specialists"
#     #     headers = self.get_headers()
#     #     data = {}
#     #     response = self.client.get(url, data, headers=headers, format='json')
#     #     json_response = json.loads(response.content)

#     #     # print(f"self.text={self.text}")
#     #     # print(f"json_response[self.text_name]={json_response[self.text_name]}")
#     #     self.assertEqual(response.status_code, self.status_code)
#     #     self.assertEqual(json_response[self.response_field_name], self.text)

#     # def test_specialist_one_1(self):
#     #     url = self.base_url + "/specialists/1"
#     #     headers = self.get_headers()
#     #     data = {}
#     #     response = self.client.get(url, data, headers=headers, format='json')
#     #     json_response = json.loads(response.content)

#     #     self.assertEqual(response.status_code, self.status_code)
#     #     self.assertEqual(json_response[self.text_name], self.text)

#     # def test_slot_list(self):
#     #     url = self.base_url + "/slots"
#     #     headers = self.get_headers()
#     #     data = {}
#     #     response = self.client.get(url, data, headers=headers, format='json')
#     #     json_response = json.loads(response.content)

#     #     self.assertEqual(response.status_code, self.status_code)
#     #     self.assertEqual(json_response[self.text_name], self.text)

#     # def test_slot_one_1(self):
#     #     url = self.base_url + "/slots/1"
#     #     headers = self.get_headers()
#     #     data = {}
#     #     response = self.client.get(url, data, headers=headers, format='json')
#     #     json_response = json.loads(response.content)

#     #     self.assertEqual(response.status_code, self.status_code)
#     #     self.assertEqual(json_response[self.text_name], self.text)

#     # def test_slot_sign_1(self):
#     #     url = self.base_url + "/slots/sign/1"
#     #     headers = self.get_headers()
#     #     data = {}
#     #     response = self.client.get(url, data, headers=headers, format='json')
#     #     json_response = json.loads(response.content)

#     #     self.assertEqual(response.status_code, self.status_code)
#     #     self.assertEqual(json_response[self.text_name], self.text)

#     # def test_slot_unsign_1(self):
#     #     url = self.base_url + "/slots/unsign/1"
#     #     headers = self.get_headers()
#     #     data = {}
#     #     response = self.client.get(url, data, headers=headers, format='json')
#     #     json_response = json.loads(response.content)

#     #     self.assertEqual(response.status_code, self.status_code)
#     #     self.assertEqual(json_response[self.text_name], self.text)

# # class AnonymousTests(APITestCase):
# #     base_url = "/api/v1/for_clients"
# #     token = ""
# #     api_client = APIClient()

# #     status_code = 403
# #     response_field_name = "detail"
# #     text = "Authentication credentials were not provided."

# #     def login(self, username, password):
# #         user = User.objects.get(username=username)
# #         self.token = Token.objects.create(user=user)
# #         self.token.save()

# #         print(f"token = {self.token}")
        
# #     def logout(self):
# #         Token.objects.all().delete()

# #     def get_headers(self):
# #         if (self.token):
# #             return {
# #                 "Authorization": f"Token {self.token}"
# #             }
# #         else:
# #             return None

# #         return headers

# #     def setUp(self) -> None:
# #         super().setUp()

# #     def tearDown(self) -> None:
# #         super().tearDown()

# #     def test_specialist_list(self):
# #         url = self.base_url + "/specialists"
# #         headers = self.get_headers()
# #         data = {}
# #         response = self.client.get(url, data, headers=headers, format='json')
# #         json_response = json.loads(response.content)

# #         # print(f"self.text={self.text}")
# #         # print(f"json_response[self.text_name]={json_response[self.text_name]}")
# #         self.assertEqual(response.status_code, self.status_code)
# #         self.assertEqual(json_response[self.response_field_name], self.text)

# #     # def test_specialist_one_1(self):
# #     #     url = self.base_url + "/specialists/1"
# #     #     headers = self.get_headers()
# #     #     data = {}
# #     #     response = self.client.get(url, data, headers=headers, format='json')
# #     #     json_response = json.loads(response.content)

# #     #     self.assertEqual(response.status_code, self.status_code)
# #     #     self.assertEqual(json_response[self.text_name], self.text)

# #     # def test_slot_list(self):
# #     #     url = self.base_url + "/slots"
# #     #     headers = self.get_headers()
# #     #     data = {}
# #     #     response = self.client.get(url, data, headers=headers, format='json')
# #     #     json_response = json.loads(response.content)

# #     #     self.assertEqual(response.status_code, self.status_code)
# #     #     self.assertEqual(json_response[self.text_name], self.text)

# #     # def test_slot_one_1(self):
# #     #     url = self.base_url + "/slots/1"
# #     #     headers = self.get_headers()
# #     #     data = {}
# #     #     response = self.client.get(url, data, headers=headers, format='json')
# #     #     json_response = json.loads(response.content)

# #     #     self.assertEqual(response.status_code, self.status_code)
# #     #     self.assertEqual(json_response[self.text_name], self.text)

# #     # def test_slot_sign_1(self):
# #     #     url = self.base_url + "/slots/sign/1"
# #     #     headers = self.get_headers()
# #     #     data = {}
# #     #     response = self.client.get(url, data, headers=headers, format='json')
# #     #     json_response = json.loads(response.content)

# #     #     self.assertEqual(response.status_code, self.status_code)
# #     #     self.assertEqual(json_response[self.text_name], self.text)

# #     # def test_slot_unsign_1(self):
# #     #     url = self.base_url + "/slots/unsign/1"
# #     #     headers = self.get_headers()
# #     #     data = {}
# #     #     response = self.client.get(url, data, headers=headers, format='json')
# #     #     json_response = json.loads(response.content)

# #     #     self.assertEqual(response.status_code, self.status_code)
# #     #     self.assertEqual(json_response[self.text_name], self.text)

# class SpecialistTests(AnonymousTests):
#     # api_client = APIClient()
#     # token = ""
#     status_code = 403
#     response_field_name = "detail"
#     response_field_text = "You do not have permission to perform this action."

    
#     def setUp(self) -> None:
#         super().setUp()
#         create_example_database_only_users_1()

#         username = "spec1"
#         password = "spec1psw"

#         self.login(username, password)
        
#         # # self.api_client.login(username=username, password=password)
#         # user = User.objects.get(username=username)
#         # print(Token.objects.count())
#         # self.token = Token.objects.get(user=user)
#         # print(self.token)

#     def tearDown(self) -> None:
#         super().tearDown()
#         # self.api_client.logout()
#         self.logout()

# # class ClientTests(APITestCase):
# #     base_url = "/api/v1/for_clients"

# #     def setUp(self):
# #         # create_example_database_1()
# #         pass

# #     def test_specialist_list(self):
# #         url = self.base_url + "/specialists"
# #         data = {}
# #         response = self.client.get(url, data, format='json')

# #         self.assertEqual(response.status_code, 403)

# #     def test_specialist_one_1(self):
# #         url = self.base_url + "/specialists/1"
# #         data = {}
# #         response = self.client.get(url, data, format='json')

# #         self.assertEqual(response.status_code, 403)

# #     def test_slot_list(self):
# #         url = self.base_url + "/slots"
# #         data = {}
# #         response = self.client.get(url, data, format='json')

# #         self.assertEqual(response.status_code, 403)

# #     def test_slot_one_1(self):
# #         url = self.base_url + "/slots/1"
# #         data = {}
# #         response = self.client.get(url, data, format='json')

# #         self.assertEqual(response.status_code, 403)

# #     def test_slot_sign_1(self):
# #         url = self.base_url + "/slots/sign/1"
# #         data = {}
# #         response = self.client.get(url, data, format='json')

# #         self.assertEqual(response.status_code, 403)

# #     def test_slot_unsign_1(self):
# #         url = self.base_url + "/slots/unsign/1"
# #         data = {}
# #         response = self.client.get(url, data, format='json')

# #         self.assertEqual(response.status_code, 403)