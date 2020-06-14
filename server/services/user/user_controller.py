from flask import request
from flask_restful import Resource
from services.user.middleware.user_handler import UserHandler


class User(Resource):
    @classmethod
    def post(cls):
        user_payload = request.get_json()
        username = user_payload.get('username')
        # Check the good practices of sending the username and password
        # over the wire. 
        password = user_payload.get('password')
        user_handler = UserHandler()
        return user_handler.GetUserBasicInformation(username, password) 

# 1> Login
    # Request username:, password:
    # Response {
    # user_role: Student/Teacher/Parent/Admin
    # json_webtoken: To be saved as cookie (Used to verify user and it's role.)
    # name: ''
    # class: ''
    # is_class_teacher: ''
    # }