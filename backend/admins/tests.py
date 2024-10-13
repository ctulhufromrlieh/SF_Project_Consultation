import json
import unittest

from django.test import TestCase
from rest_framework.test import APIRequestFactory, RequestsClient, APITestCase, APIClient

from django.db.models import Q
from django.contrib.auth.models import User

from main.tests_common import *

# skip_tests = True
skip_tests = False

class TestsMixin():
    is_logined = False

    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    @staticmethod
    def is_for_admin_users_equal(obj, dict):
        return (
            (obj.pk == dict["id"]) and
            (obj.username == dict["username"]) and
            (obj.first_name == dict["first_name"]) and
            (obj.last_name == dict["last_name"]) and
            (obj.last_name == dict["last_name"]) and 
            (get_user_type_caption(obj) == dict["user_type_caption"])
        )

    # remove "a" for separate tests
    def atest_user_list(self):
        self.check_get_status("/users")
    
    def atest_user_one_1(self):
        self.check_get_status("/users/1")

    def atest_user_activate_1(self):
        if not self.is_logined:
            self.check_post_status("/users/activate/1")

    def atest_user_deactivate_1(self):
        if not self.is_logined:
            self.check_post_status("/users/deactivate/1")

    def test_all(self):
        self.atest_user_list()
        self.atest_user_one_1()
        self.atest_user_activate_1()
        self.atest_user_deactivate_1()

@unittest.skipIf(skip_tests, "Skip these tests")
class AnonymousTests(TestsMixin, AnonymousBaseTest):
    base_url = "/api/v1/for_admins"

@unittest.skipIf(skip_tests, "Skip these tests")
class SpecialistTests(TestsMixin, ForbiddenBaseTest):
    base_url = "/api/v1/for_admins"

    username = "spec1"
    password = "spec1psw"     

@unittest.skipIf(skip_tests, "Skip these tests")
class ClientTests(TestsMixin, ForbiddenBaseTest):
    base_url = "/api/v1/for_admins"

    username = "client1"
    password = "client1psw"

@unittest.skipIf(skip_tests, "Skip these tests")
class AdminTests(TestsMixin, SuccessBaseTest):
    base_url = "/api/v1/for_admins"

    username = "admin1"
    password = "admin1psw"
    myadmin = None

    is_logined = True

    def setUp(self) -> None:
        super().setUp()
        self.myadmin = User.objects.get(username=self.username)

    def atest_user_list_a(self):
        users_b = User.objects.all()

        resp_result = self.get_simple("/users")
        users_r = resp_result["data"]

        self.assertEqual(resp_result["status_code"], 200)
        self.assertEqual(users_b.count(), len(users_r))

        for i in range(len(users_r)):
            curr_user_r = users_r[i]
            curr_user_b = users_b[i]
            self.assertTrue(self.is_users_equal(curr_user_b, curr_user_r))
    
    def atest_user_one_a(self):
        ids = [1, 2, 3, 4, 5, 6]
        for curr_id in ids:
            curr_loc_url = f"/users/{curr_id}"
            curr_resp_result = self.get_simple(curr_loc_url)
            curr_user_r = curr_resp_result["data"]
            curr_user_b = User.objects.get(pk=curr_id)

            self.assertEqual(curr_resp_result["status_code"], 200)
            self.assertTrue(self.is_users_equal(curr_user_b, curr_user_r))

    # def atest_specialist_list_a(self):
    #     # specs_b = Specialist.objects.all()
    #     specs_b = User.objects.filter(groups__name='specialists')

    #     resp_result = self.get_simple("/specialists")
    #     specs_r = resp_result["data"]

    #     self.assertEqual(resp_result["status_code"], 200)
    #     self.assertEqual(specs_b.count(), len(specs_r))

    #     for i in range(len(specs_r)):
    #         curr_spec_r = specs_r[i]
    #         curr_spec_b = specs_b[i]
    #         self.assertTrue(self.is_specialists_equal(curr_spec_b, curr_spec_r))
    
    # def atest_specialist_one_a(self):
    #     ids = [1, 2]
    #     for curr_id in ids:
    #         curr_loc_url = f"/specialists/{curr_id}"
    #         curr_resp_result = self.get_simple(curr_loc_url)
    #         curr_spec_r = curr_resp_result["data"]
    #         curr_spec_b = User.objects.filter(groups__name='specialists').get(pk=curr_id)

    #         self.assertEqual(curr_resp_result["status_code"], 200)
    #         self.assertTrue(self.is_specialists_equal(curr_spec_b, curr_spec_r))

    # def atest_client_list_a(self):
    #     clients_b = User.objects.filter(groups__name='clients')

    #     resp_result = self.get_simple("/clients")
    #     clients_r = resp_result["data"]

    #     self.assertEqual(resp_result["status_code"], 200)
    #     self.assertEqual(clients_b.count(), len(clients_r))

    #     for i in range(len(clients_r)):
    #         curr_client_r = clients_r[i]
    #         curr_client_b = clients_b[i]
    #         self.assertTrue(self.is_clients_equal(curr_client_b, curr_client_r))
    
    # def atest_client_one_a(self):
    #     ids = [1, 2]
    #     for curr_id in ids:
    #         curr_loc_url = f"/clients/{curr_id}"
    #         curr_resp_result = self.get_simple(curr_loc_url)
    #         curr_client_r = curr_resp_result["data"]
    #         curr_client_b = User.objects.filter(groups__name='specialists').get(pk=curr_id)

    #         self.assertEqual(resp_result["status_code"], 200)
    #         self.assertTrue(self.is_clients_equal(curr_client_b, curr_client_r))

    def test_get(self):
        self.atest_user_list_a()
        self.atest_user_one_a()

    def test_activate_and_deactivate(self):
        self.check_post_simple("/users/activate/", 404, "", "")
        self.check_post_simple("/users/deactivate/", 404, "", "")
        self.check_post_simple("/users/activate/100500", 400, "error", "Wrong user id")
        self.check_post_simple("/users/deactivate/100500", 400, "error", "Wrong user id")

        self.check_post_simple("/users/activate/1", 400, "error", "User already activated")
        
        user = User.objects.filter(pk=1).first()
        self.assertTrue(user.is_active)
        
        self.check_post_simple("/users/activate/1", 400, "error", "User already activated")
        self.check_post_simple("/users/deactivate/1", 200, "success", "You successfully deactivate user")
        
        user = User.objects.filter(pk=1).first()
        self.assertTrue(not user.is_active)
        
        self.check_post_simple("/users/deactivate/1", 400, "error", "User already deactivated")
        self.check_post_simple("/users/activate/1", 200, "success", "You successfully activate user")
        
        user = User.objects.filter(pk=1).first()
        self.assertTrue(user.is_active)
