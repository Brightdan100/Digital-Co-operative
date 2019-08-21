from flask import request, app
from flask_restful import Resource

from model import UserSchema, User, db

users_schema = UserSchema(many=True)
user_schema = UserSchema()


class UserResource(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {
                       "message": "No input data provided"
                   }, 400

        data, errors = user_schema.load(json_data)
        if errors:
            return {
                       "status": "error",
                       "data": errors
                   }, 422

        user = User.query.filter_by(name=data['name']).first()
        if user:
            return {
                       "message": "user already exist"
                   }, 400

        user = User(
            title=data['title'],
            name=data['name'],
            email=data['email'],
            phone_number=data['phone_number'],
            age=data['age'],
            sex=data['sex'],
        )

        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user).data

        return {
                   "status": "success",
                   "data": result
               }, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {
                       "message": "No input data provided"
                   }, 400

        data, errors = user_schema.load(json_data)
        if errors:
            return {
                       "status": "error",
                       "data": errors
                   }, 422
