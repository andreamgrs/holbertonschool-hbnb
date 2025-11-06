from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .. import config


bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()


def create_app(config_class="config.DevelopmentConfig"):# create multiple indendepent instances of app for test/stage
    
    app = Flask(__name__)
    if config_class is None:
        config_class = config.DevelopmentConfig
    app.config.from_object(config_class)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    from .api.v1.users import api as users_ns
    from .api.v1.reviews import api as reviews_ns
    from .api.v1.places import api as places_ns
    from .api.v1.amenities import api as amenities_ns
    from .api.v1.auth import api as auth_ns
    from .api.v1.admin import api as admin_ns

    # register the users namespace, allowing the route defined in api/v1/users to be accessible through /api/v1/users
    api.add_namespace(users_ns, path='/api/v1/users')
    # register the places namespace, allowing the route defined in api/v1/places to be accessible through /api/v1/places
    api.add_namespace(places_ns, path='/api/v1/places')
    # register the amenities namespace, allowing the route defined in api/v1/amenities to be accessible through /api/v1/amenities
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    # register reviews namespace, allowing the route defined in api/v1/reviews to be accessible through /api/v1/reviews
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    # register auth namespace, allowing the route defined in api/v1/auth to be accessible through /api/v1/auth
    api.add_namespace(auth_ns, path='/api/v1/auth')
    # register admin namespace, allowing the route defined in api/v1 to be accessible through /api/v1
    api.add_namespace(admin_ns, path='/api/v1')
    return app