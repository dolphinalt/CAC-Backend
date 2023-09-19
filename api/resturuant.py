import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.users import User

users_api = Blueprint('resturuant_api', __name__,
                   url_prefix='/api/cac')

api = Api(users_api)

class resturuantAPI:
    class _CRUD(Resource):
        def post(self):
            body = request.get_json()

            rid = body.get('rid')
            name = body.get('name')
            pfp = body.get('pfp')
            about = body.get('about')
            menu = body.get('menu')

            if rid is None:
                return {'message': f'RID is missing'}, 400
            if name is None:
                return {'message': f'Name is missing'}, 400

            resturuantObj = Resturuant(name=name, rid=rid, pfp=pfp, about=about, menu=menu)
        
            resturuant = resturuantObj.create()

            if resturuant:
                return jsonify(resturuant.read())
            return {'message': f'Processed {name}, either a format error or Resturant ID {rid} is duplicate'}, 400
        
        def get(self):
            resturuants = Resturuant.query.all()
            json_ready = [resturuant.read() for resturuant in resturuants]
            return jsonify(json_ready)
    
    api.add_resource(_CRUD, '/')