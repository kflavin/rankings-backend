from flask import Flask

from flask_cors import CORS
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask_graphql import GraphQLView
from app.database import db_session, init_db
from app.relay_schema import schema as relay_schema
from app.simple_schema import schema as simple_schema


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    bcrypt.init_app(app)
    app.debug = True

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

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app