import json
import unittest

from django.test import TestCase
from rest_framework.test import APIRequestFactory, RequestsClient, APITestCase, APIClient

from django.db.models import Q
# from django.urls import reverse
from django.contrib.auth.models import User

# from rest_framework import status
# from rest_framework.authtoken.models import Token

from main.tests_common import *

skip_tests = True

class TestsMixin():
    need_params = False

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
        self.check_post_status("/slots/sign/3")

    def atest_slot_unsign_1(self):
        if not self.need_params:        
            self.check_post_status("/slots/unsign/1")

    def test_all(self):
        self.atest_specialist_list()
        self.atest_specialist_one_1()
        self.atest_slot_list()
        self.atest_slot_one_1()
        self.atest_slot_sign_1()
        self.atest_slot_unsign_1()

@unittest.skipIf(skip_tests, "Skip these tests")
class AnonymousTests(TestsMixin, AnonymousBaseTest):
    base_url = "/api/v1/for_clients"

@unittest.skipIf(skip_tests, "Skip these tests")
class SpecialistTests(TestsMixin, ForbiddenBaseTest):
    base_url = "/api/v1/for_clients"

    username = "spec1"
    password = "spec1psw"     

@unittest.skipIf(skip_tests, "Skip these tests")
class AdminTests(TestsMixin, ForbiddenBaseTest):
    base_url = "/api/v1/for_clients"

    username = "admin1"
    password = "admin1psw"

@unittest.skipIf(skip_tests, "Skip these tests")
class ClientTests(TestsMixin, SuccessBaseTest):
    base_url = "/api/v1/for_clients"

    username = "client1"
    password = "client1psw"
    myclient = None

    need_params = True

    def setUp(self) -> None:
        super().setUp()
        self.myclient = Client.objects.get(user__username=self.username)
        # print(self.myclient)

    def atest_specialist_list(self):
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
    
    def atest_specialist_one(self):
        ids = [1, 2]
        for curr_id in ids:
            curr_loc_url = f"/specialists/{curr_id}"
            curr_resp_result = self.get_simple(curr_loc_url)
            curr_spec_r = curr_resp_result["data"]
            curr_spec_b = Specialist.objects.get(pk=curr_id)

            # self.assertEqual(resp_result["status_code"], 200)
            self.assertTrue(self.is_specialists_equal(curr_spec_b, curr_spec_r))

    def atest_slot_list(self):
        slots_b = Slot.objects.filter(Q(client=None) | Q(client=self.myclient))

        resp_result = self.get_simple("/slots")
        slots_r = resp_result["data"]

        # self.assertEqual(resp_result["status_code"], 200)
        self.assertEqual(slots_b.count(), len(slots_r))

        for i in range(len(slots_r)):
            curr_slot_r = slots_r[i]
            curr_slot_b = slots_b[i]
            
            self.assertTrue(self.is_slots_equal(curr_slot_b, curr_slot_r))

    def test_get(self):
        self.atest_specialist_list()
        self.atest_specialist_one()
        self.atest_slot_list()

    def test_slot_sign_and_unsign_1(self):
        # sign
        self.check_post_simple("/slots/sign/", 404, "", "")
        self.check_post_simple("/slots/sign/100500", 400, "error", "Slot with such id not exists")
        self.check_post_simple("/slots/sign/1", 400, "error", "This slot already used by you")
        self.check_post_simple("/slots/sign/2", 400, "error", "This slot already used")

        slot = Slot.objects.get(pk=3)
        self.assertEqual(slot.client, None)

        self.check_post_simple("/slots/sign/3", 200, "success", "You successfully signed to slot")
        self.check_post_simple("/slots/sign/1", 400, "error", "This slot already used by you")

        slot = Slot.objects.get(pk=3)
        self.assertEqual(slot.client, self.myclient)

        self.check_post_simple("/slots/sign/3", 400, "error", "This slot already used by you")

        # unsign
        self.check_post_simple("/slots/unsign/", 404, "", "")
        self.check_post_simple("/slots/unsign/100500", 400, "error", "Slot with such id not exists")
        self.check_post_simple("/slots/unsign/2", 400, "error", "You are not signed to this slot")
        self.check_post_simple("/slots/unsign/1", 400, "error", "You should set valid Cancel Type or set non-empty Cancel comment")
        self.check_post_simple("/slots/unsign/3", 400, "error", "You should set valid Cancel Type or set non-empty Cancel comment")
        self.check_post_simple("/slots/unsign/1", 400, "error", "You should set valid Cancel Type or set non-empty Cancel comment", data={"cancel_type": 100500})
        
        self.assertEqual(Slot.objects.filter(pk=1).first().cancel_type, None)
        self.check_post_simple("/slots/unsign/1", 200, "success", "You successfully unsigned from slot", data={"cancel_type": 1})
        self.assertEqual(Slot.objects.filter(pk=1).first().cancel_type.pk, 1)

        self.assertEqual(Slot.objects.filter(pk=1).first().cancel_comment, "")
        self.check_post_simple("/slots/unsign/3", 200, "success", "You successfully unsigned from slot", data={"cancel_comment": "I am sorry"})
        self.assertEqual(Slot.objects.filter(pk=3).first().cancel_comment, "I am sorry")
        # print(resp_result)
