import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory to the system path
sys.path.append(BASE_DIR)

import json

from base import BaseTestCase
import logging

class TestAddTA(BaseTestCase):

    def test_add_ta_with_invalid_token(self):
        valid_credentials = {
                        "email": "hrushikesh.malpekar@email.com",
                        "password": "Abcd@123"
                    }       
        with self.client:
            resp_register = self.client.post('/login_user', data=json.dumps(valid_credentials), content_type='application/json')
            data = {
                "is_native_english_speaker": True,
                "instructor": 15,
                "course": 12,
                "is_summer": False,
                "class_size": 30,
                "class_attribute": 1
            }
            response = self.client.post('/add_TA', data= json.dumps(data),headers=dict(
                    Authorization='Token ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                ),content_type='application/json')
            self.assertEqual(response.status_code, 200)


    def test_add_ta_with_missing_data(self):
        valid_credentials = {
                        "email": "hrushikesh.malpekar@email.com",
                        "password": "Abcd@123"
                    }       
        with self.client:
            resp_register = self.client.post('/login_user', data=json.dumps(valid_credentials), content_type='application/json')
            
            data = {}
            response = self.client.post('/add_TA', data= json.dumps(data),headers=dict(
                    Authorization='Token ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                ),content_type='application/json')
            self.assertEqual(response.status_code, 400)

    
    def test_add_ta_with_valid_data(self):
        with self.client:
            data = {
                "is_native_english_speaker": True,
                "instructor": 15,
                "course": 20,
                "is_summer": False,
                "class_size": 30,
                "class_attribute": 1
            }
            
            response = self.client.post('/add_TA',data = json.dumps(data),content_type='application/json',headers={"Authorization": "Token random"})
            self.assertEqual(response.status_code, 500)

#Rest Test Case for Update,Retrive,Delete can be build using the above Testcase as blueprint

if __name__ == "__main__":
    unittest.main()
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "SomeTest.testSomething" ).setLevel( logging.DEBUG )
    unittest.main()


