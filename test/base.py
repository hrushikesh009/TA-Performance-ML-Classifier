# project/tests/test_config.py
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory to the system path
sys.path.append(BASE_DIR)
from flask_testing import TestCase

from server import app, db


class BaseTestCase(TestCase):
    """ Base Tests """
    def create_app(self):
        app.config.from_object('server.config.TestingConfig')
        return app
        
    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()