import json
import unittest

from flask import url_for

from app import create_app, db
from app.models import Account, Transaction, User


class AccountModelTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

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

    def add_funds(self, msisdn, amount):
        registered_user = User.query.filter(User.msisdn == msisdn).first()
        account = registered_user.account
        account.balance = amount
        account.save()

    def create_user(self, msisdn, first_name="TestName", last_name="LastName", funds=0):
        params = {"msisdn": msisdn, "first_name": first_name, "last_name": last_name}
        url = url_for("api.users_api")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))
        if funds > 0:
            self.add_funds(msisdn, funds)

    def test_user_create_account_without_funds(self):
        self.create_user("254717416435")
        registered_user = User.query.filter(User.msisdn == "254717416435").first()
        account = registered_user.account

        self.assertIsNotNone(account)
        self.assertEqual(0.0, account.balance)

    def test_create_transaction_error_no_source(self):

        params = {"destination": "254717416434", "amount": 10.0, "currency": "USD"}
        url = url_for("api.transfers_api")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(400, response.status_code)
        error = json_response["error"]
        self.assertIsNotNone(error)
        self.assertEquals(["Source is required."], error)

    def test_create_transaction_error_invalid_source(self):

        params = {"source": "25471741643A", "destination": "254717416434", "amount": 10.0, "currency": "USD"}
        url = url_for("api.transfers_api")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(400, response.status_code)
        error = json_response["error"]
        self.assertIsNotNone(error)
        self.assertEquals(["Source and Destination must be numbers."], error)

    def test_create_transaction_error_unregistered_destination(self):
        self.create_user("254717416435")

        params = {"source": "254717416435", "destination": "254717416434", "amount": 10.0, "currency": "USD"}
        url = url_for("api.transfers_api")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(400, response.status_code)
        error = json_response["error"]
        self.assertIsNotNone(error)
        self.assertEquals(["Source and Destination must be registered."], error)

    def test_create_transaction_error_not_funds(self):
        self.create_user("254717416435")
        self.create_user("254717416434")

        params = {"source": "254717416435", "destination": "254717416434", "amount": 10.0, "currency": "USD"}
        url = url_for("api.transfers_api")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(400, response.status_code)
        error = json_response["error"]
        self.assertIsNotNone(error)
        self.assertEquals(["Source doesn't have enough funds."], error)

    def test_create_transaction_success(self):
        self.create_user("254717416435", funds=100)
        self.create_user("254717416434")

        params = {"source": "254717416435", "destination": "254717416434", "amount": 10.0, "currency": "USD"}
        url = url_for("api.transfers_api")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(json_response['transfer']['balance'], 90.0)

    def test_get_user_transactions_success(self):
        self.create_user("254717416435", funds=100)
        self.create_user("254717416434")

        params = {"source": "254717416435", "destination": "254717416434", "amount": 10.0, "currency": "USD"}
        url = url_for("api.transfers_api")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(json_response['transfer']['balance'], 90.0)

    def test_get_user_transactions_no_transactions(self):
        self.create_user("254717412451")

        url = url_for("api.users_transfers_api", msisdn='254717412451')
        response = self.client.get(url, headers=self.get_api_headers())
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json_response['transactions']), 0)

    def test_get_user_transactions_error_invalid_msisdn(self):
        url = url_for("api.users_transfers_api", msisdn='254717412A51')
        response = self.client.get(url, headers=self.get_api_headers())
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(400, response.status_code)
        error = json_response["error"]
        self.assertIsNotNone(error)
        self.assertEquals(["Phone number must contain just numbers."], error)

    def test_get_user_transactions_error_unkown_msisdn(self):
        url = url_for("api.users_transfers_api", msisdn='254717412451')
        response = self.client.get(url, headers=self.get_api_headers())
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(404, response.status_code)
        error = json_response["error"]
        self.assertIsNotNone(error)
        self.assertEquals(["Unknown phone number."], error)

    def test_get_user_transactions_list_success(self):
        self.create_user("254717416435", funds=100)
        self.create_user("254717412451")

        params = {"source": "254717416435", "destination": "254717412451", "amount": 10.0, "currency": "USD"}
        url = url_for("api.transfers_api")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        url = url_for("api.users_transfers_api", msisdn='254717416435')
        response = self.client.get(url, headers=self.get_api_headers())
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json_response['transactions']), 1)
        self.assertEqual(json_response['transactions'][0]['amount'], -10)

    def test_get_all_transactions_success(self):
        self.create_user("254717416435", funds=100)
        self.create_user("254717412451")

        params = {"source": "254717416435", "destination": "254717412451", "amount": 10.0, "currency": "USD"}
        url = url_for("api.transfers_api")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        params = {"source": "254717412451", "destination": "254717416435", "amount": 2.0, "currency": "USD"}
        url = url_for("api.transfers_api")
        response = self.client.post(url, headers=self.get_api_headers(), data=json.dumps(params))

        url = url_for("api.transfers_api")
        response = self.client.get(url, headers=self.get_api_headers())
        json_response = json.loads(response.data.decode('utf-8'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json_response['transactions']), 4)
