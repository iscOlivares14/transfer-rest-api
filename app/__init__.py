#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_jwt import JWT
from flask_sqlalchemy import SQLAlchemy

from .config import config

db = SQLAlchemy()


def add_api_blueprint(app):
    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix="/api/v1")


def authenticate(username, password):
    from .models import User
    user = User.get_by_msisdn(username)
    if user and user.verify_password(password):
        return user


def identity(payload):
    from .models import User
    user_id = payload['identity']
    user = User.query.filter_by(id=user_id).first()
    return user or None


def create_app(config_name, add_logging=True):
    conf_error = None
    if config_name is None:
        conf_error = "no config passed"
        config_name = "development"
    app = Flask(__name__, static_url_path="")
    app.config.from_object(config[config_name])
    db.init_app(app)
    # login_manager.init_app(app)
    if add_logging is True:
        config[config_name].init_app(app)
    if conf_error is not None:
        app.logger.error("Env is none, fatal error")
    app.logger.warning("warning Environment set: {}".format(config_name))

    add_api_blueprint(app)
    jwt = JWT(app, authenticate, identity)
    return app
