from flask import current_app
from app import create_app, db
import unittest


class BasicsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.app_context.pop()

    def test_app_exists(self):
        """ test app exists """
        # the app should exist
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """ test app is called testing """
        # the app should be called 'TESTING'
        self.assertTrue(current_app.config["TESTING"])
