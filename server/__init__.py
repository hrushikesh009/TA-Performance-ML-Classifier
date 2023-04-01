import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


template_dir = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__,template_folder=template_dir)

app_settings = os.getenv(
    'APP_SETTINGS',
    'server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)



# Initialize the database with the app
db = SQLAlchemy(app)

# Import and register blueprints for different parts of the app
from auth.app import auth_blueprint
app.register_blueprint(auth_blueprint)




