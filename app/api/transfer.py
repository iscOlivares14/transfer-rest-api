from flask import current_app, jsonify, make_response, request
from flask.views import MethodView
from flask_jwt import jwt_required

from . import api
from .utils import transfer_error as terr
from ..models import Currency, Transaction, TransactionType as ttype, User


class TransferAPI(MethodView):
    """/api/v1/transfers ."""

    def __init__(self):
        self.logger = current_app.logger

    @jwt_required()
    def get(self):
        transfers = Transaction.get_all()
        json_transfers = [t.to_json() for t in transfers]

        return make_response(jsonify({"success": "OK", "transactions": json_transfers}), 200)

    def make_special_transaction(self, source, destination, amount, currency):
        user_destination = User.query.filter_by(msisdn=destination).first()
        if not user_destination:
            return make_response(jsonify(terr['dstReq']), 400)
        if source == ttype.ADD_FUNDS.value:
            transaction_in = Transaction(source=source,
                                         destination=destination,
                                         amount=amount,
                                         currency=currency,
                                         account=user_destination.account)
            transaction_in.save()
            user_destination.account.balance += amount
            user_destination.account.save()

        transfer_result = {}
        transfer_result["success"] = "OK"
        transfer_result["transfer"] = {}
        transfer_result["transfer"]["balance"] = user_destination.account.balance
        transfer_result["transfer"]["transaction"] = user_destination.to_json()

        return make_response(jsonify(transfer_result), 200)

    @jwt_required()
    def post(self):
        try:
            json_dict = request.get_json()
        except Exception as e:
            return make_response(jsonify(terr['missingData']), 400)

        source = json_dict.get('source', None)
        destination = json_dict.get('destination', None)
        amount = json_dict.get('amount', None)
        currency = json_dict.get('currency')

        if not source:
            return make_response(jsonify(terr['srcReq']), 400)
        if not destination:
            return make_response(jsonify(terr['dstReq']), 400)
        if not source.isdigit() or not destination.isdigit():
            return make_response(jsonify(terr['srcdestInval']), 400)
        if not amount:
            return make_response(jsonify(terr['amntReq']), 400)
        if amount < 0:
            return make_response(jsonify(terr['amntInval']), 400)
        if not currency:
            return make_response(jsonify(terr['currReq']), 400)
        if currency not in [c.name for c in Currency]:
            return make_response(jsonify(terr['currInvalid']), 400)

        # chack for a special transaction
        if source in [t.value for t in ttype]:
            return self.make_special_transaction(source, destination, amount, currency)

        user_source = User.query.filter_by(msisdn=source).first()
        user_destination = User.query.filter_by(msisdn=destination).first()
        if not (user_source and user_destination):
            return make_response(jsonify(terr['srcdestReq']), 400)

        # enough funds
        if user_source.account.balance - amount >= 0:
            transaction_out = Transaction(source=source,
                                          destination=destination,
                                          amount=(amount * -1),
                                          currency=currency,
                                          account=user_source.account)
            transaction_out.save()
            user_source.account.balance -= amount
            user_source.account.save()
            transaction_in = Transaction(source=source,
                                         destination=destination,
                                         amount=amount,
                                         currency=currency,
                                         account=user_destination.account)
            transaction_in.save()
            user_destination.account.balance += amount
            user_destination.account.save()
        else:
            return make_response(jsonify(terr['amntInsuf']), 400)

        transfer_result = {}
        transfer_result["success"] = "OK"
        transfer_result["transfer"] = {}
        transfer_result["transfer"]["balance"] = user_source.account.balance
        transfer_result["transfer"]["transaction"] = transaction_out.to_json()

        return make_response(jsonify(transfer_result), 200)


class TransferItemAPI(MethodView):
    """/api/v1/transactions/<ref> ."""

    def __init__(self):
        self.logger = current_app.logger


transfer_view = TransferAPI.as_view("transfers_api")

api.add_url_rule("/transactions/", view_func=transfer_view)
