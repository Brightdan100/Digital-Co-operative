from flask_restful import Api
from flask import Blueprint

from resources.Users import UserResource

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

#Route

api.add_resource(UserResource, '/user')
