import datetime

from functools import wraps

from flask import g
from flask_restful import Resource, abort, reqparse, fields, marshal_with
from flask_jwt import jwt_required, current_identity

from .models import db, Subscription, Publication

publication_serializer = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'creator_id': fields.Integer,
    'date_created': fields.DateTime(dt_format='rfc822'),
    'date_modified': fields.DateTime(dt_format='rfc822')
}

subscription_serializer = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'publication': fields.Nested(publication_serializer),
    'date_created': fields.DateTime(dt_format='rfc822'),
    'date_modified': fields.DateTime(dt_format='rfc822')
}


@jwt_required
def login_required(f):
    @wraps(f)
    def func_wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return func_wrapper


@jwt_required
def get_publication(f):
    @wraps(f)
    def func_wrapper(*args, **kwargs):
        publication_id = kwargs['publication_id']
        publication = Publication.query.get(publication_id)
        if publication is None:
            abort(404, message="Could not find the selected publication")
        g.publication = publication
        return f(*args, **kwargs)
    return func_wrapper


@jwt_required
def get_subscription(f):
    @wraps(f)
    def func_wrapper(*args, **kwargs):
        user_id = kwargs['user_id']
        subscription_id = kwargs['subscription_id']
        subscription = Subscription.query.filter(
            Subscription.id == subscription_id and
            Subscription.user_id == user_id
        ).scalar()
        if subscription is None:
            abort(404, message="Could not find the selected subscription")
        g.subscription = subscription
        return f(*args, **kwargs)
    return func_wrapper


class PublicationsService(Resource):
    method_decorators = [marshal_with(publication_serializer)]

    def get(self):
        publications = Publication.query.all()
        return publications

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        req = parser.parse_args()
        title = req['title']
        description = req['description']
        creator_id = int(current_identity)
        try:
            publication = Publication(
                title=title,
                description=description,
                creator_id=creator_id
            )
            db.session.add(publication)
            db.session.commit()
            return publication, 201
        except Exception as e:
            abort(
                400,
                message="Error occured while saving publication :: {}".format(
                    e.message
                )
            )


class SinglePublicationService(Resource):
    method_decorators = [get_publication, marshal_with(publication_serializer)]

    def get(self, publication_id):
        publication = g.publication
        return publication

    def put(self, publication_id):
        publication = g.publication
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        req = parser.parse_arg()
        publication.title = req.get('title', publication.title)
        publication.description = req.get(
            'description',
            publication.description
        )
        publication.date_modified = datetime.datetime.utcnow
        db.session.add(publication)
        db.ssession.commit()


class SubscriptionsService(Resource):
    method_decorators = [marshal_with(subscription_serializer)]

    def get(self, user_id):
        subscriptions = Subscription.query.filter(
            Subscription.user_id == user_id
        ).all()
        return subscriptions

    @login_required
    def post(self, user_id):
        if user_id != int(current_identity):
            abort(401, message="You cannot subscribe for someone else")
        parser = reqparse.RequestParser()
        parser.add_argument('publication_id', type=int, required=True)
        req = parser.parse_args()
        publication_id = req['publication_id']
        subscription_exists = Subscription.query.filter(
            Subscription.publication_id == publication_id and
            Subscription.user_id == user_id
        ).scalar()

        if subscription_exists is not None:
            abort(
                400,
                message="You have already subscribed for this publication"
            )

        try:
            subscription = Subscription(
                user_id=user_id,
                publication_id=publication_id
            )
            db.session.add(subscription)
            db.session.commit()
            return subscription
        except Exception as e:
            abort(
                400,
                message="Could not complete your request :: {}".format(
                    e.message
                )
            )


class SingleSubscriptionService(Resource):
    method_decorators = [get_subscription, marshal_with(subscription_serializer)]

    def get(self, user_id, subscription_id):
        return g.subscription

    def put(self, user_id, subscription_id):
        pass

    def delete(self, user_id, subscription_id):
        pass
