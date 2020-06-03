#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

from flask_login import UserMixin

from .. import db
from ..helpers import CoreMixin


class Account(CoreMixin, db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float(precision=2), default=0.00)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    transactions = db.relationship('Transaction', backref='account', lazy=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        params = {}
        params["id"] = self.id
        params["user_id"] = self.user_id
        params["balance"] = self.balance
        return params


class Currency(Enum):
    USD = "dollar"

    @classmethod
    def to_list(cls):
        return [c.name for c in cls]


class TransactionType(Enum):
    ADD_FUNDS = "0000000110"

    @classmethod
    def to_list(cls):
        return [t.value for t in cls]


class Transaction(CoreMixin, db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(16))
    destination = db.Column(db.String(16))
    amount = db.Column(db.Float(precision=2))
    currency = db.Column(db.String(3))
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    @staticmethod
    def get_all():
        return Transaction.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        params = {}
        params["id"] = self.id
        params["source"] = self.source
        params["destination"] = self.destination
        params["amount"] = self.amount
        params["currency"] = self.currency
        params["created"] = self.created
        return params
