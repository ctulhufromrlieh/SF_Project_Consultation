import json
import unittest

from django.test import TestCase
from rest_framework.test import APIRequestFactory, RequestsClient, APITestCase, APIClient

from django.db.models import Q
from django.contrib.auth.models import User

from main.tests_common import *
from main.utils import *

# skip_tests = True
skip_tests = False

class TestsMixin():
    need_params = False

    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    # remove "a" for separate tests
    # def atest_specialist_list(self):
    #     self.check_get_status("/specialists")
    
    # def atest_specialist_one_1(self):
    #     self.check_get_status("/specialists/1")

    def atest_slot_list(self):
        self.check_get_status("/slots")

    def atest_slot_one_1(self):
        self.check_get_status("/slots/3")

    # def atest_slot_sign_1(self):
    #     self.check_post_status("/slots/sign/3")

    # def atest_slot_unsign_1(self):
    #     if not self.need_params:        
    #         self.check_post_status("/slots/unsign/1")

    def test_all(self):
        # self.atest_specialist_list()
        # self.atest_specialist_one_1()
        self.atest_slot_list()
        self.atest_slot_one_1()
        # self.atest_slot_sign_1()
        # self.atest_slot_unsign_1()

@unittest.skipIf(skip_tests, "Skip these tests")
class AnonymousTests(TestsMixin, AnonymousBaseTest):
    base_url = "/api/v1/for_specialists"

@unittest.skipIf(skip_tests, "Skip these tests")
class ClientTests(TestsMixin, ForbiddenBaseTest):
    base_url = "/api/v1/for_specialists"

    username = "client1"
    password = "client1psw"     

@unittest.skipIf(skip_tests, "Skip these tests")
class AdminTests(TestsMixin, ForbiddenBaseTest):
    base_url = "/api/v1/for_specialists"

    username = "admin1"
    password = "admin1psw"

@unittest.skipIf(skip_tests, "Skip these tests")
class SpecialistTests(TestsMixin, SuccessBaseTest):
    base_url = "/api/v1/for_specialists"

    username = "spec1"
    password = "spec1psw"
    myspec = None

    need_params = True

    def setUp(self) -> None:
        super().setUp()
        self.myspec = Specialist.objects.get(user__username=self.username)
        # print(self.myclient)

    def atest_slot_list(self):
        slots_b = Slot.objects.filter(specialist=self.myspec)

        resp_result = self.get_simple("/slots")
        slots_r = resp_result["data"]

        self.assertEqual(slots_b.count(), len(slots_r))

        for i in range(len(slots_r)):
            curr_slot_r = slots_r[i]
            curr_slot_b = slots_b[i]
            
            self.assertTrue(self.is_slots_equal(curr_slot_b, curr_slot_r))

    def atest_slot_one(self):
        slots_b = Slot.objects.filter(specialist=self.myspec)

        for curr_slot_b in slots_b:
            resp_result = self.get_simple(f"/slots/{curr_slot_b.pk}")
            curr_slot_r = resp_result["data"]
            self.assertTrue(self.is_slots_equal(curr_slot_b, curr_slot_r))

    def test_get(self):
        self.atest_slot_list()
        self.atest_slot_one()

    def test_slot_accept_and_decline_1(self):
        # sign
        self.check_post_simple("/slots/accept/", 404, "", "")
        self.check_post_simple("/slots/accept/100500", 400, "error", "Slot with such id not exists")
        self.check_post_simple("/slots/accept/4", 400, "error", "It is not your slot")
        self.check_post_simple("/slots/accept/3", 400, "error", "Client is not assigned yet")

        slot = Slot.objects.get(pk=1)
        self.assertEqual(slot.is_accepted, False)
        self.check_post_simple("/slots/accept/1", 200, "success", "You successfully accept slot")
        slot = Slot.objects.get(pk=1)
        self.assertEqual(slot.is_accepted, True)
        self.check_post_simple("/slots/accept/1", 400, "error", "This slot already accepted")


        self.check_post_simple("/slots/decline/", 404, "", "")
        self.check_post_simple("/slots/decline/100500", 400, "error", "Slot with such id not exists")
        self.check_post_simple("/slots/decline/4", 400, "error", "It is not your slot")
        self.check_post_simple("/slots/decline/3", 400, "error", "Client is not assigned yet")

        slot = Slot.objects.get(pk=2)
        client = Client.objects.get(pk=2)
        self.assertEqual(slot.client, client)

        self.check_post_simple("/slots/decline/2", 200, "success", "You successfully decline slot")

        slot = Slot.objects.get(pk=2)
        self.assertEqual(slot.client, None)

        self.check_post_simple("/slots/decline/2", 400, "error", "Client is not assigned yet")

    def test_create_update_delete(self):
        self.assertEqual(Slot.objects.count(), 6)

        self.check_post_simple("/slots", 400, "", "")

        self.check_post_simple("/slots", 400, "", "", {
            "type": 20,
            "title": "the title",
            "datetime1": "2024-06-10 12:00 +03:00",
            "datetime2": "2024-06-10 14:00 +03:00",
            "description": "the description of slot",
            "cost": 1234
        })

        self.check_post_simple("/slots", 201, "", "", {
            "type": 1,
            "title": "the title",
            "datetime1": "2024-06-10 12:00 +03:00",
            "datetime2": "2024-06-10 14:00 +03:00",
            "description": "the description of slot",
            "cost": 1234
        })

        self.assertEqual(Slot.objects.count(), 7)

        slot = Slot.objects.order_by("pk").last()
        self.assertEqual(slot.type.pk, 1)
        self.assertEqual(slot.title, "the title")
        self.assertEqual(slot.datetime1, datetime.strptime("2024-06-10 12:00 +03:00", "%Y-%m-%d %H:%M %z"))
        self.assertEqual(slot.datetime2, datetime.strptime("2024-06-10 14:00 +03:00", "%Y-%m-%d %H:%M %z"))
        self.assertEqual(slot.description, "the description of slot")
        self.assertEqual(slot.cost, 1234)

        self.check_post_simple("/slots", 400, "", "", {
            "type": 1,
            "title": "the title",
            "datetime1": "2024-06-10 13:30 +03:00",
            "datetime2": "2024-06-10 15:30 +03:00",
            "description": "the description of slot",
            "cost": 1234
        })

        self.check_post_simple("/slots", 201, "", "", {
            "type": 1,
            "title": "the title",
            "datetime1": "2024-06-10 14:00 +03:00",
            "datetime2": "2024-06-10 16:00 +03:00",
            "description": "the description of slot",
            "cost": 1234
        })        

        # put
        slot = Slot.objects.order_by("pk").last()
        self.check_put_simple(f"/slots/{slot.pk}", 200, "", "", {
            "type": 2,
            "title": "the title new",
            "datetime1": "2024-06-10 16:00 +03:00",
            "datetime2": "2024-06-10 18:00 +03:00",
            "description": "the description of slot new",
            "cost": 12345
        })

        slot = Slot.objects.order_by("pk").last()
        self.assertEqual(slot.type.pk, 2)
        self.assertEqual(slot.title, "the title new")
        self.assertEqual(slot.datetime1, datetime.strptime("2024-06-10 16:00 +03:00", "%Y-%m-%d %H:%M %z"))
        self.assertEqual(slot.datetime2, datetime.strptime("2024-06-10 18:00 +03:00", "%Y-%m-%d %H:%M %z"))
        self.assertEqual(slot.description, "the description of slot new")
        self.assertEqual(slot.cost, 12345)

        # patch
        slot = Slot.objects.order_by("pk").last()
        self.check_patch_simple(f"/slots/{slot.pk}", 200, "", "", {
            "type": 1,
            "title": "the title new new",
            "datetime1": "2024-06-10 17:00 +03:00",
            "datetime2": "2024-06-10 19:00 +03:00",
            "description": "the description of slot new new",
            "cost": 123456
        })

        slot = Slot.objects.order_by("pk").last()
        self.assertEqual(slot.type.pk, 1)
        self.assertEqual(slot.title, "the title new new")
        self.assertEqual(slot.datetime1, datetime.strptime("2024-06-10 17:00 +03:00", "%Y-%m-%d %H:%M %z"))
        self.assertEqual(slot.datetime2, datetime.strptime("2024-06-10 19:00 +03:00", "%Y-%m-%d %H:%M %z"))
        self.assertEqual(slot.description, "the description of slot new new")
        self.assertEqual(slot.cost, 123456)

        # delete
        slot_id = slot.pk
        old_slot_count = Slot.objects.count()
        self.check_delete_simple(f"/slots/100500", 404)
        self.check_delete_simple(f"/slots/{slot_id}", 204)
        new_slot_count = Slot.objects.count()
        self.assertEqual(new_slot_count + 1, old_slot_count)
        self.assertEqual(Slot.objects.filter(pk=slot_id).first(), None)
