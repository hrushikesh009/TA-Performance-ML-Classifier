# project/server/config.py
import os

from dotenv import load_dotenv

load_dotenv()

db_pass = os.getenv("DATABASE_PASSWORD")
secret_key = os.getenv('SECRET_KEY')


DATABASE_HOST = "localhost"
DATABASE_USERNAME = "root" 
DATABASE_PASSWORD = db_pass



basedir = os.path.abspath(os.path.dirname(__file__))
mysql_local_base = 'mysql+mysqldb://'+DATABASE_USERNAME+':'+DATABASE_PASSWORD+'@'+DATABASE_HOST+'/'
database_name = 'Your Database Name'


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = secret_key
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = mysql_local_base + database_name


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = mysql_local_base + database_name + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


