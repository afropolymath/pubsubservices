from flask_restful import Api
from flask_jwt import JWT

from app import app
from app.resources import SubscriptionsService, SingleSubscriptionService, \
    PublicationsService, SinglePublicationService

'''
Endpoints

GET     /users/:id/subscriptions
        -> Get all subscriptions for this user

POST    /users/:id/subscriptions
        -> Create a new subscription for this user

GET     /users/:id/subscriptions/:id
        -> Get a single subscription

PUT     /users/:id/subscriptions/:id
        -> Update a single subscription

DELETE  /users/:id/subscriptions/:id
        -> Delete a single subscription
'''

api = Api(app)


def identity(payload):
    return payload['identity']


jwt = JWT(app, identity_handler=identity)

api.add_resource(
    SinglePublicationService,
    '/publications/<int:publication_id>'
)
api.add_resource(PublicationsService, '/publications')
api.add_resource(
    SingleSubscriptionService,
    '/users/<int:user_id>/subscriptions/<int:subscription_id>'
)
api.add_resource(SubscriptionsService, '/users/<int:user_id>/subscriptions')
