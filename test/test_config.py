# project/tests/test_config.py

import os
import sys
import unittest

from flask import current_app
from flask_testing import TestCase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory to the system path
sys.path.append(BASE_DIR)

from server import app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('server.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'Your mysql configuration'
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('server.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'Your mysql configuration'
        )


if __name__ == '__main__':
    unittest.main()