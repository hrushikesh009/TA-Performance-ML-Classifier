import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory to the system path
sys.path.append(BASE_DIR)

import datetime
import pickle

import jwt
import numpy as np
import pandas as pd
from flask import Blueprint, jsonify, make_response, render_template, request
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sqlalchemy.exc import IntegrityError

from auth.auth_middleware import token_authenication
from auth.models import TeachingAssisstant, User
from auth.validate import (validate_email_and_password, validate_ta,
                           validate_user)
from server import app, db

auth_blueprint = Blueprint('auth', __name__)


def home():
    return render_template('index.html')


def predict_score():
    try:
        #validate data
        request_form = request.form.to_dict()
        if request_form['is_native_english_speaker'] == 1:
            request_form.update({'is_native_english_speaker':True})
        else:
            request_form.update({'is_native_english_speaker':False})

        if request_form['is_summer'] == 1:
            request_form.update({'is_summer':True})
        else:
            request_form.update({'is_summer':False})
        
        request_form['instructor'] = int(request.form['instructor'])
        request_form['course'] = int(request.form['course'])
        request_form['class_size'] = int(int(request.form['class_size']))

        
        is_validated = validate_ta(request_form,required = ["is_native_english_speaker", "instructor", "course", "is_summer", "class_size"])
        if is_validated is not None:
            return make_response (jsonify({"message":'Invalid data', "data":None, "error":is_validated}), 400)
        
        if request_form['is_native_english_speaker'] == True:
            request_form.update({'is_native_english_speaker':1})
        else:
            request_form.update({'is_native_english_speaker':2})

        if request_form['is_summer'] == True:
            request_form.update({'is_summer':1})
        else:
            request_form.update({'is_summer':2})
        request_form['score'] = 0
        data_dir = os.path.join(BASE_DIR, 'data.csv')
        data = pd.read_csv(data_dir, header=None)
        data.rename(columns={0:'is_native_english_speaker', 1:'instructor', 2:'course', 3:'is_summer', 4:'class_size', 5:'score'},inplace = True)
        new_data = pd.DataFrame([request_form])
        data = data.append(new_data)


        # converting categorical variables to numerical variables using one-hot encoding
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(sparse_output = False), [1, 2])], remainder='passthrough')
        data = ct.fit_transform(data)

        # converting to numpy array
        data = np.array(data)

        # normalizing the numerical variables
        sc = StandardScaler()
        data[:, -2:-1] = sc.fit_transform(data[:, -2:-1])

    
        # Load the pre-trained model from file
        model_dir = os.path.join(BASE_DIR, 'models/model.pkl')

        with open(model_dir, 'rb') as f:
            model = pickle.load(f)

        data = np.array([data[:, :-1][-1]])

        predicted_score = model.predict(data)


        # Render the output template with the predicted score
        return render_template('output.html', predicted_score=int(predicted_score[0]))
    except Exception as e:
        predicted_score = 2
        return render_template('output.html', predicted_score=predicted_score)
        

def add_user():
    try:
        data = request.get_json() 
        if not data:
            return make_response (jsonify({
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }), 400)
        is_validated = validate_user(**data)
        if is_validated is not True:
            return make_response (jsonify({"message":'Invalid data', "data":None, "error":is_validated}), 400)
        
        #User object
        try:
            user = User(email=data['email'],password=data['password'],admin=data.get('admin',None))
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return make_response (jsonify({
                "message": "User already exists",
                "error": "Conflict",
                "data": None
            }), 409)

        return make_response (jsonify({
            "message": "Successfully Created new user",
            "data": {
                "Email Address": user.email
            } 
        }), 200)
    except Exception as e:
        return make_response (jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500)


def login():
    try:
        # import pdb;pdb.set_trace();
        data = request.get_json() 
        if not data:
            return make_response (jsonify({
                "message": "Please provide user Credentails",
                "data": None,
                "error": "Bad request"
            }), 400)
        
        is_validated = validate_email_and_password(**data)
        if is_validated is not True:
            return make_response (jsonify({"message":'Invalid data', "data":None, "error":is_validated}), 400)
        
        user = User.query.filter_by(email=data['email']).first()
        
        if user is not None and user.authenticate_user(user=user,user_enterd_password=data['password']):
            try:
                auth_token = jwt.encode({"email": user.email,
                                        "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
                                        app.config["SECRET_KEY"],
                                         algorithm="HS256"
                )
                return make_response (jsonify({
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token
                        }),200)
            
            except Exception as e:
                return make_response (jsonify({
                    "error": "Something went wrong",
                    "message": str(e)
                }), 500)
            
        return make_response (jsonify({
            "message": "Error fetching auth token!, invalid email or password",
            "data": None,
            "error": "Unauthorized"
        }), 404)
    except Exception as e:
        return make_response (jsonify ({
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
        }), 500)


@token_authenication
def add_ta(user):
    try:
        data = request.get_json()
        if not data:
            return make_response (jsonify({
                "message": "Please provide user Credentails",
                "data": None,
                "error": "Bad request"
            }), 400)
        
        
        is_validated = validate_ta(data,required = ["is_native_english_speaker", "instructor", "course", "is_summer", "class_size", "class_attribute"])
        if is_validated is not None:
            return make_response (jsonify({"message":'Invalid data', "data":None, "error":is_validated}), 400)
        
        try:
            ta_object = TeachingAssisstant(**data)
            db.session.add(ta_object)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return make_response (jsonify({
            "message": "Something Went Wrong!",
            "data": None,
            "Error": e
        }), 500)

        return make_response (jsonify({
            "message": "Successfully Add new Entry!",
            "user":user.email
        }), 200)
        
    except Exception as e:
        return make_response (jsonify({
            "message": "Failed to Update!",
            "error": str(e),
            "data": None
        }), 400)


@token_authenication
def retrieve_ta(user,id):
    try:
        ta_object = TeachingAssisstant.query.filter_by(id=id).first()
        if ta_object is None:
            return make_response (jsonify({'message': f'Teaching Assisstant data against the {id} not found!'}))
        return make_response (jsonify({"message": "Successfully Retrived Data!",
                       "data": {
                        'id': ta_object.id,
                        'is_native_english_speaker': ta_object.is_native_english_speaker,
                        'course_instructor': ta_object.instructor,
                        'course': ta_object.course,
                        'semester': ta_object.is_summer,
                        'class_size': ta_object.class_size,
                        'class_attribute': ta_object.class_attribute
                       },"user":user.email
                        }),200)
        
    except Exception as e:
        return make_response (jsonify({
            "message": "Failed to Retrive Data! Something went Wrong",
            "error": str(e),
            "data": None
        }), 400)
    

@token_authenication
def update_ta(user,id):
    try:
        data = request.get_json()
        if not data:
            return make_response (jsonify({
                "message": "Please Provide Data!",
                "data": None,
                "error": "Bad request"
            }), 400)
        
        
        is_validated = validate_ta(data)
        if is_validated is not None:
            return make_response (jsonify({"message":'Invalid data', "data":None, "error":is_validated}), 400)
        
        ta_object = TeachingAssisstant.query.filter_by(id=id).first()
        if ta_object is None:
            return make_response (jsonify({'message': f'Teaching Assisstant data against the {id} not found!'}))
        else:
            for key, value in data.items():
                setattr(ta_object, key, value)
            db.session.commit()
            return make_response (jsonify({"message": f"Successfully Updated the {id} Entry!","user":user.email}),200)
    except Exception as e:
        return make_response (jsonify({
            "message": "Failed to Retrive Data! Something went Wrong",
            "error": str(e),
            "data": None
        }), 400)


@token_authenication
def delete_ta(user,id):
    try:
        ta_object = TeachingAssisstant.query.filter_by(id=id).first()
        if ta_object is None:
            return make_response (jsonify({'message': f'Teaching Assisstant data against the {id} not found!'}))
        db.session.delete(ta_object)
        db.session.commit()
        return make_response (jsonify({"message": f"Successfully Deleted the {id} Entry!","user":user.email}),200)
        
    except Exception as e:
        return make_response (jsonify({
            "message": "Failed to Delete Data! Something went Wrong",
            "error": str(e),
            "data": None
        }), 400)
    

#url encoder

auth_blueprint.add_url_rule('/',view_func=home,methods=['GET'])
auth_blueprint.add_url_rule('/register_user',view_func=add_user,methods=['POST'])
auth_blueprint.add_url_rule('/predict_score',view_func=predict_score,methods=['POST'])
auth_blueprint.add_url_rule('/login_user',view_func=login,methods=['POST'])
auth_blueprint.add_url_rule('/add_TA',view_func=add_ta,methods=['POST'])
auth_blueprint.add_url_rule('/update_ta/<int:id>', view_func=update_ta, methods=['PUT'])
auth_blueprint.add_url_rule('/retrieve_ta/<int:id>',view_func=retrieve_ta,methods=['GET'])
auth_blueprint.add_url_rule('/delete_ta/<int:id>',view_func=delete_ta,methods=['DELETE'])
    
