from flask import Flask

from flask_cors import CORS
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_graphql import GraphQLView

from app.relay_schema import schema as relay_schema
from app.simple_schema import schema as simple_schema
from app.schema.rankings import schema as exp_schema
from app.authmiddleware import AuthMiddleware

from config import config

def create_app(config_name="default"):
    app = Flask(__name__)
    app.wsgi_app = AuthMiddleware(app.wsgi_app)
    CORS(app)
    bcrypt.init_app(app)
    app.debug = True
    app.config.from_object(config[config_name])

    print("your url is: " + app.config['SQLALCHEMY_DATABASE_URI'])

    db.init_app(app)

    app.add_url_rule('/graphql',
                     view_func=GraphQLView.as_view(
                         'graphql',
                         schema=relay_schema,
                         graphiql=True
                     ))

    app.add_url_rule('/simple',
                     view_func=GraphQLView.as_view(
                         'simple',
                         schema=simple_schema,
                         graphiql=True
                     ))
    app.add_url_rule('/exp',
                     view_func=GraphQLView.as_view(
                         'exp',
                         schema=exp_schema,
                         graphiql=True
                     ))

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app