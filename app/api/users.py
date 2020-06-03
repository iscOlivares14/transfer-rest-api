from datetime import datetime
import re

from flask import make_response, jsonify, request, current_app
from flask_jwt import jwt_required
from flask.views import MethodView

from . import api
from .utils import input_error as ierr
from ..models import User, Account


@api.route("/test", methods=["GET"])
def test():
    return "Project setup successfully!", 200


class UserAPI(MethodView):
    """/api/v1/users ."""

    def __init__(self):
        self.logger = current_app.logger

    @jwt_required()
    def get(self):
        """Get all users as a list ."""
        users = User.get_all()
        json_users = [u.to_json() for u in users]

        return make_response(jsonify({"success": "OK", "users": json_users}), 200)

    def post(self):
        """Create a new user ."""
        try:
            json_dict = request.get_json()
        except Exception as e:
            return make_response(jsonify(ierr['missingData']), 400)

        first_name = json_dict.get("first_name", None)
        last_name = json_dict.get("last_name", None)
        msisdn = json_dict.get("msisdn", None)
        password = json_dict.get("password", None)

        if not first_name:
            return make_response(jsonify(ierr['fnameReq']), 400)
        if not last_name:
            return make_response(jsonify(ierr['lnameReq']), 400)
        if not msisdn:
            return make_response(jsonify(ierr['msisdnReq']), 400)
        if not msisdn.isdigit():
            return make_response(jsonify(ierr['msisdnNonDigits']), 400)
        if not password:
            return make_response(jsonify(ierr['pwdReq']), 400)
        if re.match(r'[a-zA-Z0-9]+\\W', password):
            return make_response(jsonify(ierr['pwdError']), 400)

        user = User.get_by_msisdn(msisdn)
        if user is not None:
            return make_response(jsonify(ierr['msisdnExists']), 400)

        user = User(created=datetime.utcnow(), msisdn=msisdn,
                    first_name=first_name, last_name=last_name,
                    password=password)
        user.save()
        account = Account(user=user)
        account.save()

        return make_response(jsonify({"success": "OK", "user": user.to_json()}), 201)


class UserItemAPI(MethodView):
    """/api/v1/users/<msisdn> ."""

    def __init__(self):
        self.logger = current_app.logger

    @jwt_required()
    def get(self, msisdn):
        """Get a user by MSISDN ."""
        if not msisdn.isdigit():
            return make_response(jsonify(ierr['msisdnNonDigits']), 400)

        user = User.get_by_msisdn(msisdn)
        if not user:
            return make_response(jsonify(ierr['msisdnUnknown']), 404)
        return make_response(jsonify({"success": "OK", "user": user.to_json()}), 200)


class UserTransferAPI(MethodView):
    """/api/v1/users/<msisdn>/transactions ."""

    def __init__(self):
        self.logger = current_app.logger

    @jwt_required()
    def get(self, msisdn):
        """Get a user's transactions ."""
        if not msisdn.isdigit():
            return make_response(jsonify(ierr['msisdnNonDigits']), 400)

        user = User.get_by_msisdn(msisdn)
        if not user:
            return make_response(jsonify(ierr['msisdnUnknown']), 404)

        transactions = [t.to_json() for t in user.account.transactions]
        return make_response(jsonify({"success": "OK", 'transactions': transactions }))


user_view = UserAPI.as_view("users_api")
user_item_view = UserItemAPI.as_view("users_item_api")
user_transfers_view = UserTransferAPI.as_view("users_transfers_api")

api.add_url_rule("/users/", view_func=user_view)
api.add_url_rule("/users/<string:msisdn>", view_func=user_item_view)
api.add_url_rule("/users/<string:msisdn>/transactions", view_func=user_transfers_view)
