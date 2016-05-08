from functools import wraps

from flask import g, request
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flask_jwt import jwt_required, current_identity

from .models import db, User

user_serializer = {
    'id': fields.Integer,
    'name': fields.String,
    'username': fields.String,
    'email': fields.String,
    'date_created': fields.DateTime(dt_format='rfc822'),
    'date_modified': fields.DateTime(dt_format='rfc822'),
}


@jwt_required
def is_admin(f):
    @wraps(f)
    def func_wrapper(*args, **kwargs):
        if current_identity and current_identity.username == 'admin':
            abort(401, message="You are not authorized to view this resource")
        return f(*args, **kwargs)
    return func_wrapper


@jwt_required
def get_user(f):
    @wraps(f)
    def func_wrapper(*args, **kwargs):
        user_id = kwargs['user_id']
        if current_identity and current_identity.id == user_id:
            g.user = User.query.get(user_id)
        return f(*args, **kwargs)
    return func_wrapper


class UsersService(Resource):
    method_decorators = [marshal_with(user_serializer)]

    @is_admin
    def get(self):
        users = User.query.all()
        return users

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('name', type=str)

        req = parser.parse_args()

        try:
            user = User(
                username=req['username'],
                email=req['email'],
                password=req['password'],
                name=req['name']
            )
            db.session.add(user)
            db.session.commit()
            return user, 201
        except Exception as e:
            abort(400, message=e.message)


class SingleUserService(Resource):
    method_decorators = [get_user, marshal_with(user_serializer)]

    def get(self, user_id):
        try:
            return g.user
        except Exception:
            abort(401, message="You are not authorized to view this resource")

    def put(self, user_id):
        pass

    def delete(self, user_id):
        pass
