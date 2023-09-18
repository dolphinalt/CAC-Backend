import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.users import User

users_api = Blueprint('users_api', __name__,
                   url_prefix='/api/cac')

api = Api(users_api)

class CACAPI:
    class _CRUD(Resource):
        def post(self):
            body = request.get_json()

            uid = body.get('uid')
            name = body.get('name')
            pfp = body.get('pfp')
            about = body.get('about')
            password = body.get('password')
            allergies = body.get('allergies')
            isResturuant = body.get('isResturuant')

            if uid is None:
                return {'message': f'User ID is missing'}, 400
            if name is None:
                return {'message': f'Name is missing'}, 400
            if password is None:
                return {'message': f'Password is missing'}, 400
            if isResturuant is None:
                return {'message': f'isResturuant is missing'}, 400

            userObj = User(name=name, uid=uid, pfp=pfp, about=about, allergies=allergies, isResturuant=isResturuant)

            if password is not None:
                userObj.set_password(password)
        
            user = userObj.create()

            if user:
                return jsonify(user.read())
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400
        
        def get(self):
            users = User.query.all()
            json_ready = [user.read() for user in users]
            return jsonify(json_ready)
        
    class _Security (Resource):
        def post(self):
            body=request.get_json()

            uid = body.get('uid')
            password = body.get('password')

            if uid is None:
                return {'message': f'User ID is missing'}, 400
            
            user = User.query.filter_by(_uid=uid).first()
            if user is None or not user.is_password(password):
                return {'message': f"Invalid user id or password"}, 400
            
            return jsonify(user.read())
    
    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')