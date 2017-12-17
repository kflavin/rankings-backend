import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'database.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevConfig(Config):
    pass

class ProdConfig(Config):
    pass

config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig
}
    