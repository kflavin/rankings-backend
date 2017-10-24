from flask import Flask
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask_graphql import GraphQLView
from app.database import db_session, init_db
from app.schema import schema


def create_app(config_name):
    app = Flask(__name__)
    bcrypt.init_app(app)
    app.debug = True

    app.add_url_rule('/graphql',
                     view_func=GraphQLView.as_view(
                         'graphql',
                         schema=schema,
                         graphiql=True
                     ))

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app