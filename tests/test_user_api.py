# -*- coding: utf-8 -*-
import json
import unittest

from flask import url_for
from faker import Faker

from app import create_app, db
from app.models import User


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.faker = Faker()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.app_context.pop()

    def get_api_headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def test_create_user_success(self):
        params = {"msisdn": "254717416435",
                  "first_name": self.faker.first_name(), "last_name": self.faker.last_name()}
        url = url_for("api.users_api")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        saved_user = User.query.filter(User.msisdn == "254717416435").first()

        self.assertEqual(201, response.status_code)
        self.assertTrue(saved_user.msisdn == "254717416435")

    def test_create_user_missing_first_name(self):
        params = {"msisdn": "254717416435", "last_name": self.faker.last_name()}
        url = url_for("api.users_api")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        json_response = json.loads(response.data.decode("utf-8"))

        self.assertEqual(400, response.status_code)
        self.assertTrue("error" in json_response)
        error = json_response["error"]
        self.assertEqual(400, response.status_code)
        self.assertEquals(["First name is required."], error)

    def test_create_user_missing_last_name(self):
        params = {"msisdn": "254717416435", "first_name": self.faker.first_name()}
        url = url_for("api.users_api")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        json_response = json.loads(response.data.decode("utf-8"))

        self.assertEqual(400, response.status_code)
        self.assertTrue("error" in json_response)
        error = json_response["error"]
        self.assertEqual(400, response.status_code)
        self.assertEquals(["Last name is required."], error)

    def test_create_user_missing_msisdn(self):
        params = {"first_name": self.faker.first_name(), "last_name": self.faker.last_name()}
        url = url_for("api.users_api")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        json_response = json.loads(response.data.decode("utf-8"))

        self.assertEqual(400, response.status_code)
        self.assertTrue("error" in json_response)
        error = json_response["error"]
        self.assertEqual(400, response.status_code)
        self.assertEquals(["Phone number is required."], error)

    def test_create_user_invalid_msisdn(self):
        params = {"msisdn": "abd254717416435",
                  "first_name": self.faker.first_name(), "last_name": self.faker.last_name()}
        url = url_for("api.users_api")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        json_response = json.loads(response.data.decode("utf-8"))

        self.assertEqual(400, response.status_code)
        self.assertTrue("error" in json_response)
        error = json_response["error"]
        self.assertEqual(400, response.status_code)
        self.assertEquals(["Phone number must contain just numbers."], error)

    def test_create_user_error_user_already_exists(self):
        user = User(msisdn="254717416435")
        user.save()

        params = {"msisdn": "254717416435",
                  "first_name": self.faker.first_name(), "last_name": self.faker.last_name()}
        url = url_for("api.users_api")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        json_response = json.loads(response.data.decode("utf-8"))

        self.assertEqual(400, response.status_code)
        self.assertTrue("error" in json_response)
        error = json_response["error"]
        self.assertEqual(400, response.status_code)
        self.assertEquals(["User with that phone number already exists."], error)

    def test_retrieve_user_success(self):
        user = User(msisdn="254717416435",
                    first_name=self.faker.first_name(),
                    last_name=self.faker.first_name())
        user.save()

        url = url_for("api.users_item_api", msisdn="254717416435")
        response = self.client.get(url)

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(200, response.status_code)
        self.assertEqual("254717416435", json_response['user']['msisdn'])

    def test_retrieve_user_error_not_found(self):
        url = url_for("api.users_item_api", msisdn="1")
        response = self.client.get(url)

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(404, response.status_code)
        self.assertTrue("error" in json_response)

    def test_retrieve_all_users_success(self):
        user = User(msisdn="254717416435",
                    first_name=self.faker.first_name(),
                    last_name=self.faker.first_name())
        user.save()

        url = url_for("api.users_api")
        response = self.client.get(url)

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(200, response.status_code)
        self.assertTrue(len(json_response['users']) > 0)
