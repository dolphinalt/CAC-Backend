import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.users import User
from model.resturuant import Resturuant

users_api = Blueprint('users_api', __name__,
                   url_prefix='/api/cac')

api = Api(users_api)

class AllergieAPI:
    class _userCRUD(Resource):
        def post(self):
            body = request.get_json()

            username = body.get('username')
            name = body.get('name')
            pfp = body.get('pfp')
            about = body.get('about')
            password = body.get('password')
            allergies = body.get('allergies')
            isResturuant = body.get('isResturuant')

            if username is None:
                return {'message': f'username is missing'}, 400
            if name is None:
                return {'message': f'Name is missing'}, 400
            if password is None:
                return {'message': f'Password is missing'}, 400
            if isResturuant is None:
                return {'message': f'isResturuant is missing'}, 400

            userObj = User(username=username, name=name, isResturuant=isResturuant, password=password, pfp=pfp, about=about, allergies=allergies)

            if password is not None:
                userObj.set_password(password)
        
            user = userObj.create()

            if user:
                return jsonify(user.read())
            return {'message': f'Processed {name}, either a format error or username {username} is duplicate'}, 400
        
        def get(self):
            users = User.query.all()
            json_ready = [user.read() for user in users]
            return jsonify(json_ready)
        
    class _Security (Resource):
        def post(self):
            body=request.get_json()

            username = body.get('username')
            password = body.get('password')

            if username is None:
                return {'message': f'username is missing'}, 400
            
            user = User.query.filter_by(_username=username).first()
            print(user)
            print(password)
            print(user.is_password(password))
            if user is None or not user.is_password(password):
                return {'message': f"Invalid username or password"}, 400
            
            return jsonify(user.read())

    class _resturuantCRUD(Resource):
        def post(self):
            body = request.get_json()

            username = body.get('username')
            name = body.get('name')
            pfp = body.get('pfp')
            about = body.get('about')
            menu = body.get('menu')

            if username is None:
                return {'message': f'username is missing'}, 400
            if name is None:
                return {'message': f'Name is missing'}, 400

            resturuantObj = Resturuant(name=name, username=username, pfp=pfp, about=about, menu=menu)
        
            resturuant = resturuantObj.create()

            if resturuant:
                return jsonify(resturuant.read())
            return {'message': f'Processed {name}, either a format error or Resturant username {username} is duplicate'}, 400
        
        def get(self):
            resturuants = Resturuant.query.all()
            json_ready = [resturuant.read() for resturuant in resturuants]
            return jsonify(json_ready)
    
    api.add_resource(_userCRUD, '/users')
    api.add_resource(_resturuantCRUD, '/resturants')
    api.add_resource(_Security, '/authenticate')