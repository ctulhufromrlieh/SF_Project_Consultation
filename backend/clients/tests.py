import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory, RequestsClient, APITestCase, APIClient

# from django.urls import reverse
from django.contrib.auth.models import User

# from rest_framework import status
from rest_framework.authtoken.models import Token

from main.tests_common import *

class TestsMixin():
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    # # remove "a" for separate tests
    # def atest_specialist_list(self):
    #     self.check_get_simple("/specialists", self.status_code, self.response_field_name, self.response_field_text)
    
    # def atest_specialist_one_1(self):
    #     self.check_get_simple("/specialists/1", self.status_code, self.response_field_name, self.response_field_text)

    # def atest_slot_list(self):
    #     self.check_get_simple("/slots", self.status_code, self.response_field_name, self.response_field_text)

    # def atest_slot_one_1(self):
    #     self.check_get_simple("/slots/3", self.status_code, self.response_field_name, self.response_field_text)

    # def atest_slot_sign_1(self):
    #     self.check_post_simple("/slots/sign/1", self.status_code, self.response_field_name, self.response_field_text)

    # def atest_slot_unsign_1(self):
    #     self.check_post_simple("/slots/unsign/1", self.status_code, self.response_field_name, self.response_field_text)

    # remove "a" for separate tests
    def atest_specialist_list(self):
        self.check_get_status("/specialists")
    
    def atest_specialist_one_1(self):
        self.check_get_status("/specialists/1")

    def atest_slot_list(self):
        self.check_get_status("/slots")

    def atest_slot_one_1(self):
        self.check_get_status("/slots/3")

    def atest_slot_sign_1(self):
        self.check_post_status("/slots/sign/1")

    def atest_slot_unsign_1(self):
        self.check_post_status("/slots/unsign/1")

    def test_all(self):
        self.atest_specialist_list()
        self.atest_specialist_one_1()
        self.atest_slot_list()
        self.atest_slot_one_1()
        self.atest_slot_sign_1()
        self.atest_slot_unsign_1()

class AnonymousTests(TestsMixin, AnonymousBaseTest):
    base_url = "/api/v1/for_clients"

class ClientTests(TestsMixin, SuccessBaseTest):
    base_url = "/api/v1/for_clients"

    username = "client1"
    password = "client1psw"     

class SpecialistTests(TestsMixin, ForbiddenBaseTest):
    base_url = "/api/v1/for_clients"

    username = "spec1"
    password = "spec1psw"     

class AdminTests(TestsMixin, ForbiddenBaseTest):
    base_url = "/api/v1/for_clients"

    username = "admin1"
    password = "admin1psw"