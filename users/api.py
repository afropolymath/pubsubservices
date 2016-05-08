from flask_restful import Api

from app import app
from app.models import User
from app.resources import UsersService, SingleUserService

from flask_jwt import JWT

'''
Endpoints

GET     /users      -> Get all the users
POST    /users      -> Create a new user
GET     /users/:id  -> Get a single user profile
PUT     /users/:id  -> Update a single user profile
DELETE  /users/:id  -> Delete a single user profile

POST    /auth       -> Login the user using username and password
'''

api = Api(app)


def authenticate(username, password):
    user = User.query.filter(User.username == username).first()
    if user and user.check_password(password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.filter(User.id == payload['identity']).scalar()

jwt = JWT(app, authenticate, identity)

api.add_resource(UsersService, '/users')
api.add_resource(SingleUserService, '/users/<int:user_id>')
