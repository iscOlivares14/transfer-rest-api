#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .. import db
from ..helpers import CoreMixin


class User(CoreMixin, db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    msisdn = db.Column(db.String(16), unique=True)
    password_hash = db.Column(db.String(128))
    account = db.relationship(
        'Account', backref='user', lazy=True, uselist=False)

    def __unicode__(self):
        return str(self.id) or ""

    @staticmethod
    def get_by_msisdn(msisdn):
        return User.query.filter_by(msisdn=msisdn).first()

    @staticmethod
    def get_all():
        return User.query.all()

    @property
    def password(self):
        raise AttributeError('password is not readable.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        params = {}
        if self.first_name is not None:
            params["first_name"] = self.first_name
        if self.last_name is not None:
            params["last_name"] = self.last_name
        if self.msisdn is not None:
            params["msisdn"] = self.msisdn
        params["balance"] = self.account.balance
        params["id"] = self.id
        return params
