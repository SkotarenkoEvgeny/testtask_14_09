from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer())
    stories = db.relationship("Stories")


class Stories(db.Model):
    __tablename__ = "stories"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User")


class StoriesSchema(Schema):
    id = fields.Integer()
    title = fields.String()


class UserSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()


