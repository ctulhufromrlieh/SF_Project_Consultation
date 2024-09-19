import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory, RequestsClient, APITestCase, APIClient

from django.db.models import Q
# from django.urls import reverse
from django.contrib.auth.models import User

# from rest_framework import status
# from rest_framework.authtoken.models import Token

from main.tests_common import *

class TestsMixin():
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

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

class SpecialistTests(TestsMixin, ForbiddenBaseTest):
    base_url = "/api/v1/for_clients"

    username = "spec1"
    password = "spec1psw"     

class AdminTests(TestsMixin, ForbiddenBaseTest):
    base_url = "/api/v1/for_clients"

    username = "admin1"
    password = "admin1psw"

class ClientTests(TestsMixin, SuccessBaseTest):
    base_url = "/api/v1/for_clients"

    username = "client1"
    password = "client1psw"
    myclient = None

    def setUp(self) -> None:
        super().setUp()
        self.myclient = Client.objects.get(user__username=self.username)
        # print(self.myclient)

    def test_specialist_list(self):
        specs_b = Specialist.objects.all()

        resp_result = self.get_simple("/specialists")
        # print(resp_result)
        specs_r = resp_result["data"]

        # self.assertEqual(resp_result["status_code"], 200)
        self.assertEqual(specs_b.count(), len(specs_r))

        for i in range(len(specs_r)):
            curr_spec_r = specs_r[i]
            curr_spec_b = specs_b[i]
            self.assertTrue(self.is_specialists_equal(curr_spec_b, curr_spec_r))
    
    def test_specialist_one(self):
        ids = [1, 2]
        for curr_id in ids:
            curr_loc_url = f"/specialists/{curr_id}"
            curr_resp_result = self.get_simple(curr_loc_url)
            curr_spec_r = curr_resp_result["data"]
            curr_spec_b = Specialist.objects.get(pk=curr_id)

            # self.assertEqual(resp_result["status_code"], 200)
            self.assertTrue(self.is_specialists_equal(curr_spec_b, curr_spec_r))

    def test_slot_list(self):
        slots_b = Slot.objects.filter(Q(client=None) | Q(client=self.myclient))

        resp_result = self.get_simple("/slots")
        # print(resp_result)
        slots_r = resp_result["data"]

        # self.assertEqual(resp_result["status_code"], 200)
        self.assertEqual(slots_b.count(), len(slots_r))

        for i in range(len(slots_r)):
            curr_slot_r = slots_r[i]
            curr_slot_b = slots_b[i]
            
            self.assertTrue(self.is_slots_equal(curr_slot_b, curr_slot_r))

    #     self.check_get_status("/specialists/1")

    # def atest_slot_list(self):
    #     self.check_get_status("/slots")

    # def atest_slot_one_1(self):
    #     self.check_get_status("/slots/3")

    # def atest_slot_sign_1(self):
    #     self.check_post_status("/slots/sign/1")

    # def atest_slot_unsign_1(self):
    #     self.check_post_status("/slots/unsign/1")

