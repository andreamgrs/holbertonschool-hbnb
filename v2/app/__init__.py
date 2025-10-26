from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from app.api.v1.users import api as users_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns


db = SQLAlchemy()


def create_app(): # create multiple indendepent instances of app for test/stage
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # register the users namespace, allowing the route defined in api/v1/users to be accessible through /api/v1/users
    api.add_namespace(users_ns, path='/api/v1/users')
    # register the places namespace, allowing the route defined in api/v1/places to be accessible through /api/v1/places
    api.add_namespace(places_ns, path='/api/v1/places')
    # register the amenities namespace, allowing the route defined in api/v1/amenities to be accessible through /api/v1/amenities
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    # register reviews namespace, allowing the route defined in api/v1/reviews to be accessible through /api/v1/reviews
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    return app