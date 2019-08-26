from flask import request
from flask_restful import Resource

from model import UserSchema, User, db

users_schema = UserSchema(many=True)
user_schema = UserSchema()


class Users(Resource):

    # register a new user
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {
                       "message": "No input data provided"
                   }, 400

        data = user_schema.load(json_data)

        # if errors:
        #     return {
        #                "status": "error",
        #                "data": errors
        #            }, 422

        user = User.query.filter_by(name=data['name']).first()
        if user and (user.email == data['email'] or user.phone_number == data['phone_number'] or user.name == data['name']):
            return {
                       "message": "username already exist"
                   }, 400

        user = User(
            title=data['title'],
            name=data['name'],
            email=data['email'],
            phone_number=data['phone_number'],
            age=data['age'],
            sex=data['sex']
        )

        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user)

        return {
                   "message": "New User successfully added",
                   "data": result
               }, 201

    # @app.route('/users')
    def get(self):
        users = User.query.all()
        users = users_schema.dump(users)
        return {
                   "message": "success",
                   "data": users
               }, 200


class UserById(Resource):

    # @app.route('/update-user-info/<id>', method=['PUT'])
    def put(self, id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {
                       "message": "No input data provided"
                   }, 400

        data = user_schema.load(json_data)

        user = User.query.filter_by(id=id).first()
        if not user:
            return {
                       "message": "User doesn't exist"
                   }, 400

        user.email = data['email']
        user.phone_number = data['phone_number']

        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user)
        return {
                   "message": "User successfully updated",
                   "data": result
               }, 201

    # @route('/user/<id>')
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            user = user_schema.dump(user)
            return {
                        "message": "found",
                        "data": user
                    }, 200
        else:
            return {
                       "message": "user doesn't exist"
                   }, 401

    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return {
                        "message": "User does not exist"
                   }, 400

        User.query.filter_by(id=id).delete()
        db.session.commit()
        return {
                    "message": "User successfully deleted"
               }, 204
