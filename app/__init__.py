#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

# import rq_dashboard
from flask import Flask, jsonify
from flask_bootstrap import Bootstrap
# from flask_login import LoginManager
from flask_login import current_user
from flask_jwt import JWT, jwt_required, current_identity
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

from .config import config

db = SQLAlchemy()
sentry = Sentry()
# login_manager = LoginManager()
# login_manager.session_protection = "strong"
# login_manager.login_view = "/"


def is_accessible():
    if not current_user or not current_user.is_authenticated:
        return False
    return True


def add_auth(blueprint, app, realm="RQ Dashboard"):
    """ Only allow admins to view RQ Dash
    """

    @blueprint.before_request
    def check_for_user(*args, **kwargs):
        if not current_user or not current_user.is_authenticated:
            response = jsonify({"error": "forbidden"})
            response.status_code = 403
            return response
        response = jsonify({"success": "OK"})
        response.status_code = 200
        return response


def setup_sentry(app):
    if "SENTRY_DSN_KEY" in app.config:
        print("sentry active in {} config".format(app.config["ENVIRONMENT"]))
        sentry.init_app(
            app, dsn=app.config["SENTRY_DSN_KEY"], logging=True, level=logging.ERROR
        )


# def add_rq_dashboard(app):
#     add_auth(rq_dashboard.blueprint, app)


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
    Bootstrap(app)
    app.config.from_object(config[config_name])
    db.init_app(app)
    # login_manager.init_app(app)
    if add_logging is True:
        config[config_name].init_app(app)
        setup_sentry(app)
    if conf_error is not None:
        app.logger.error("Env is none, fatal error")
    app.logger.warning("warning Environment set: {}".format(config_name))

    add_api_blueprint(app)
    jwt = JWT(app, authenticate, identity)
    #add_rq_dashboard(app)
    return app
