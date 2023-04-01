import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory to the system path
sys.path.append(BASE_DIR)

import json

from base import BaseTestCase
from server import db

from auth.models import User
import logging


class TestRegisterAPI(BaseTestCase):
          
    def test_add_user(self):
        # Define test data
        data = {
                    "email": "hrushikesh.malpekar@email.com",
                    "password": "Abcd@123"
                } 
        
        # Make POST request to add the user
        with self.client:
            response = self.client.post('/register_user', json=data,content_type='application/json')
            
            response_data = json.loads(response.data)

            # Check that the response is successful and the user is added to the database
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_data['message'], 'Successfully Created new user')
            self.assertEqual(response_data['data']['Email Address'], 'hrushikesh.malpekar@email.com')

            # Try to add the same user again - this should result in a 409 Conflict response
            response = self.client.post('/register_user', json=data,content_type='application/json')     
            response_data = json.loads(response.data.decode())
           
            self.assertEqual(response.status_code, 409)
            self.assertEqual(response_data['message'], 'User already exists')


class TestLoginAPI(BaseTestCase):

    def test_valid_login(self):
        
        invalid_credentials = {
                        "email": "hrushikesh.malpekar@email.com",
                        "password": "Abcfh@123"
                    } 
        valid_credentials = {
            "email": "test@example.com", 
            "password": "Password@123"
            }
        
        # create a user with valid credentials if not existing
        try:
            user = User(email=valid_credentials["email"],password=valid_credentials["password"])
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.close()
        
        #login with valid credentials            
        with self.client:
            response = self.client.post('/login_user', data=json.dumps(valid_credentials), content_type='application/json')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertIn("auth_token", data)
        
        #login with invaid credentails
        with self.client:
            response = self.client.post('/login_user', data=json.dumps(invalid_credentials), content_type='application/json')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["error"], "Unauthorized")


if __name__ == "__main__":
    unittest.main()
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "SomeTest.testSomething" ).setLevel( logging.DEBUG )
    unittest.main()


