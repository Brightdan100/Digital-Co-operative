from flask import request
from flask_restful import Resource

from model import GroupConfigurationSchema, GroupConfiguration, User, db

group_configuration_schema = GroupConfigurationSchema()
group_configurations_schema = GroupConfigurationSchema(many=True)


class Group(Resource):

    def get(self):
        groups = GroupConfiguration.query.all()
        groups = group_configuration_schema.dump(groups)
        return {
                   "message": "success",
                   "data": groups
               }, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {
                       "message": "No input data provided"
                   }, 400

        data = group_configuration_schema.load(json_data)
        if data['admin_id'] not in User.query.all('id'):
            return {
                       "message": "only registered users can be admins"
                   }, 401

        if data['admin_id'] in GroupConfiguration.query.all('admin_id'):
            return {
                       "message": "A user can only be admin of a group"
                   }, 500

        # confirm if the admin is eligible to own a group
        # if data['admin_id'] in User.query.all('id') and data['admin_id'] not in GroupConfiguration.query.all('admin_id'):
        group = GroupConfiguration(
            description=data['description'],
            admin_id=data['user_id'],
            status=data['status'],
            searchable_status=data['searchable_status'],
            max_menbers=data['max_members'],
            amount_per_week=data['amount_per_week']
        )
        db.session.add(group)
        db.session.commit()

        result = group_configuration_schema.dump(group)

        return {
                   "message": "Group successfully created",
                   "data": result
               }, 200


class GroupById(Resource):

    def get(self, id):
        group = GroupConfiguration.query.filter_by(id=id).first()
        if group:
            group = group_configuration_schema.dump(group)

            return {
                       "message": "Group found",
                       "data": group
                   }, 200
        return {
                    "message": "Group doesn't exist"
               }, 401

    def delete(self, id):
        group = GroupConfiguration.query.filter_by(id=id).first()
        if not group:
            return {
                        "message": "Group doesn't exist"
                   }, 400
        GroupConfiguration.query.filter_by(id=id).delete()
        db.session.commit()
        return {
                    "message": "group successfully deleted"
               }, 200

