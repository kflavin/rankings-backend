import os
from app import create_app, init_db

app = create_app("default")

from flask_script import Manager, Shell

manager = Manager(app)

@manager.command
def init():
    init_db()

if __name__ == "__main__":
    # init_db()
    manager.run()
