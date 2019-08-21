from flask_restful import Resource

from model import GroupConfigurationSchema

group_configuration_schema = GroupConfigurationSchema()


class GroupConfigurationResource(Resource):
    pass
