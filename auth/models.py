# project/server/models.py

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory to the system path
sys.path.append(BASE_DIR)
import datetime

from werkzeug.security import check_password_hash, generate_password_hash
from server import db

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def authenticate_user(self,user,user_enterd_password): 
        if check_password_hash(user.password,user_enterd_password):
            return True
        return False


class TeachingAssisstant(db.Model):
    __tablename__ = 'teaching_assisstant'

    id = db.Column(db.Integer, primary_key=True)
    is_native_english_speaker = db.Column(db.Boolean, nullable=False)
    instructor = db.Column(db.String(25), nullable=False)
    course = db.Column(db.String(26), nullable=False)
    is_summer = db.Column(db.Boolean, nullable=False)
    class_size = db.Column(db.Integer, nullable=False)
    class_attribute = db.Column(db.String(10), nullable=False)
