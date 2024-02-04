# """Validator Module"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory to the system path
sys.path.append(BASE_DIR)
import re

import jsonschema
from flask import jsonify


def validate(data, regex):
    """Custom Validator"""
    return True if re.match(regex, data) else False

def validate_password(password: str):
    """Password Validator"""
    reg = r"\b^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$\b"
    return validate(password, reg)

def validate_email(email: str):
    """Email Validator"""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return validate(email, regex)

def validate_user(**args):
    """User Validator"""
    if  not args.get('email') or not args.get('password'):
        return {
            'email': 'Email is required',
            'password': 'Password is required',
        }
    if not isinstance(args.get('email'), str) or not isinstance(args.get('password'), str):
        return {
            'email': 'Email must be a string',
            'password': 'Password must be a string',
        }
    if not validate_email(args.get('email')):
        return {
            'email': 'Email is invalid'
        }
    if not validate_password(args.get('password')):
        return {
            'password': 'Password is invalid, Should be atleast 8 characters with upper and lower case letters, numbers and special characters'
        }
    return True

def validate_email_and_password(email, password):
    """Email and Password Validator"""
    if not (email and password):
        return {
            'email': 'Email is required',
            'password': 'Password is required'
        }
    if not validate_email(email):
        return {
            'email': 'Email is invalid'
        }
    if not validate_password(password):
        return {
            'password': 'Password is invalid, Should be atleast 8 characters with upper and lower case letters, numbers and special characters'
        }
    return True

def validate_existing_data(**args):
    error_dict = {}
    mandatory_values = ['is_native_english_speaker','is_summer','instructor','course','class_attribute','class_size']
    provided_values= list(args.keys())
    remains= set(mandatory_values) - set(provided_values)
    for key in list(remains):
        error_dict.update({f'{key}': f'{key} is required!'})
    return error_dict


# Define the JSON schema for TA data
ta_schema = {
    "type": "object",
    "properties": {
        "is_native_english_speaker": {"type": "boolean"},
        "instructor": {"type": "integer", "minimum": 1, "maximum": 25},
        "course": {"type": "integer", "minimum": 1, "maximum": 26},
        "is_summer": {"type": "boolean"},
        "class_size": {"type": "integer", "minimum": 1, "maximum": 1000},
        "class_attribute": {"type": "number", "minimum": 1, "maximum": 3}
    },
    
}

# Define a validator function for TA data
def validate_ta(data,required=[]):
    try:
        ta_schema.update({"required": required})
        jsonschema.validate(data, ta_schema)
    except jsonschema.exceptions.ValidationError as e:
        error = {"error": e.message}
        return error
    
    