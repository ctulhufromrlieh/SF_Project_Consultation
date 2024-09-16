# import json

# from django.test import TestCase
# from rest_framework.test import APIRequestFactory, RequestsClient, APITestCase, APIClient

# # from django.urls import reverse
# from django.contrib.auth.models import User

# # from rest_framework import status
# from rest_framework.authtoken.models import Token

# from main.tests_common import *

# class TestsMixin():
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

#     def test_slot_sign_1(self):
#         self.check_post_simple("/slots/sign/1", 403, self.response_field_name, self.response_field_text)

#     def test_slot_unsign_1(self):
#         self.check_post_simple("/slots/unsign/1", 403, self.response_field_name, self.response_field_text)

# class AnonymousTests(TestsMixin, AnonymousBaseTest):
#     base_url = "/api/v1/for_clients"

# # class AnonymousTests(APITestCase):
# # class AnonymousTests(BaseTest):
# #     base_url = "/api/v1/for_clients"

# #     response_field_name = "detail"
# #     response_field_text = "Authentication credentials were not provided."

# #     def setUp(self) -> None:
# #         super().setUp()

# #     def tearDown(self) -> None:
# #         super().tearDown()

# #     def test_specialist_list(self):
# #         self.check_get_simple("/specialists", 403, self.response_field_name, self.response_field_text)
    
# #     def test_specialist_one_1(self):
# #         self.check_get_simple("/specialists/1", 403, self.response_field_name, self.response_field_text)

# #     def test_slot_list(self):
# #         self.check_get_simple("/slots", 403, self.response_field_name, self.response_field_text)

# #     def test_slot_one_1(self):
# #         self.check_get_simple("/slots/1", 403, self.response_field_name, self.response_field_text)

# #     def test_slot_sign_1(self):
# #         self.check_post_simple("/slots/sign/1", 403, self.response_field_name, self.response_field_text)

# #     def test_slot_unsign_1(self):
# #         self.check_post_simple("/slots/unsign/1", 403, self.response_field_name, self.response_field_text)

# class SpecialistTests(TestsMixin, ForbiddenBaseTest):
#     base_url = "/api/v1/for_clients"

#     username = "spec1"
#     password = "spec1psw"     

# # class SpecialistTests(AnonymousTests):
# #     response_field_name = "detail"
# #     response_field_text = "You do not have permission to perform this action."

# #     username = "spec1"
# #     password = "spec1psw"    
    
# #     def setUp(self) -> None:
# #         super().setUp()
# #         create_example_database_only_users_1()

# #         username = "spec1"
# #         password = "spec1psw"

# #         self.login(username, password)

# #     def tearDown(self) -> None:
# #         super().tearDown()
# #         self.logout()
