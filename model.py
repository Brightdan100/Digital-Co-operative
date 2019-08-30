from flask_marshmallow import Marshmallow
from marshmallow import fields
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(16), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    phone_number = db.Column(db.String(16), nullable=False)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(1))
    create_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, title, name, email, phone_number, age, sex):
        self.title = title
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.age = age
        self.sex = sex


class UserSchema(ma.Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone_number = fields.String(required=True)
    age = fields.Integer()
    sex = fields.String()
    created_date = fields.DateTime()


class GroupConfiguration(db.Model):
    __tablename__ = 'group_configuration'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
    searchable_status = db.Column(db.Boolean, nullable=True)
    max_members = db.Column(db.Integer, nullable=False, default=50)
    amount_per_week = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    user = db.relationship('User', backref=db.backref('group_configuration', lazy='dynamic'))

    def __init__(self, description, admin_id, status, searchable_status, max_members, amount_per_week):
        self.description = description
        self.admin_id = admin_id
        self.status = status
        self.searchable_status = searchable_status
        self.max_members = max_members
        self.amount_per_week = amount_per_week


class GroupConfigurationSchema(ma.Schema):
    id = fields.Integer()
    admin_id = fields.Integer(required=True)
    description = fields.String()
    status = fields.Boolean(default=False)
    searchable_status = fields.Boolean(default=True)
    max_member = fields.Integer(required=True)
    amount_per_week = fields.Integer(required=True)
    created_date = fields.DateTime()


class CooperativeTransaction(db.Model):
    __tablename__ = 'cooperative_transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group_configuration.id', ondelete='CASCADE'), nullable=False)
    amount_per_week = db.Column(db.Integer, nullable=False)
    current_amount = db.Column(db.Integer)
    membership_status = db.Column(db.String(16), default='MEMBER')
    status = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('cooperative_transactions', lazy='dynamic'))
    group = db.relationship('GroupConfiguration', backref=db.backref('cooperative_transactions', lazy='dynamic'))

    def __init__(self, user_id, group_id, amount_per_week, current_amount, membership_status, status):
        self.user_id = user_id
        self.group_id = group_id
        self.amount_per_week = amount_per_week
        self.current_amount = current_amount
        self.membership_status = membership_status
        self.status = status


class CooperativeTransactionsSchema(ma.Schema):
    id = fields.Integer()
    user_id = fields.Integer(required=True)
    group_id = fields.Integer(required=True)
    amount_per_week = fields.Integer(required=True)
    current_amount = fields.Integer(required=True)
    membership_status = fields.Integer(required=True)
    status = fields.Boolean(required=True)
