from functools import wraps

import jwt
from flask import current_app, request

from auth import models


def token_authenication(request_function):
    @wraps(request_function)
    def validate_token(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            user = models.User.query.filter_by(email=data['email']).first()
            if user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return request_function(user, *args, **kwargs)

    return validate_token