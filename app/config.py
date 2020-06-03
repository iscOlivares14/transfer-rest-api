import datetime
import logging
import os
import sys

from pythonjsonlogger import jsonlogger


def init_json_logger(app):
    # TODO: inject request data to help with log parsing
    supported_keys = [
        "asctime",
        "created",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "module",
        "msecs",
        "message",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "thread",
        "threadName",
    ]
    log_format = lambda x: ["%({0:s})".format(i) for i in x]
    custom_format = " ".join(log_format(supported_keys))
    jsonformatter = jsonlogger.JsonFormatter(custom_format)
    app.logger.propagate = True
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(jsonformatter)
    # Remove everything else
    app.logger.handlers.clear()
    app.logger.addHandler(ch)


class Config:
    # DATABASES
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False

    VERSION = "4.4.24"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    JWT_AUTH_URL_RULE = '/auth'
    JWT_AUTH_USERNAME_KEY = 'msisdn'
    JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=300)
    JWT_AUTH_HEADER_PREFIX = 'JWT'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    ENVIRONMENT = "development"
    BASE_URL = "http://localhost:5000"
    TESTING = False
    DEBUG = True

    # PSQL configurations
    PSQL_DATABASE_DB = "walletcore"
    PSQL_DATABASE_PASSWORD = "password"
    PSQL_DATABASE_HOST = "postgres"
    PSQL_DATABASE_USER = "tiernan"
    SQLALCHEMY_DATABASE_URI = "postgres://{}:{}@{}/{}".format(
        PSQL_DATABASE_USER, PSQL_DATABASE_PASSWORD, PSQL_DATABASE_HOST, PSQL_DATABASE_DB
    )

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class TestingConfig(Config):
    ENVIRONMENT = "testing"
    BASE_URL = "http://localhost:5001"
    TESTING = True
    DEBUG = True

    PSQL_DATABASE_DB = "walletcore"
    PSQL_DATABASE_PASSWORD = "password"
    PSQL_DATABASE_HOST = "postgres"
    PSQL_DATABASE_PORT = 5432
    PSQL_DATABASE_USER = "tiernan"
    TEST_DATABASE_URI = "postgres://{}:{}@{}/{}".format(
        PSQL_DATABASE_USER, PSQL_DATABASE_PASSWORD, PSQL_DATABASE_HOST, PSQL_DATABASE_DB
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or TEST_DATABASE_URI

    SERVER_NAME = "localhost:5001"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}
