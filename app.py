from flask_restful import Api
from flask import Blueprint

from resources.GroupConfiguration import Group, GroupById
from resources.Users import UserById, Users

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

# Route
api.add_resource(Users, '/users', )
api.add_resource(UserById, '/user/<int:id>')
api.add_resource(Group, '/groups')
api.add_resource(GroupById, '/group/<int:id>')
