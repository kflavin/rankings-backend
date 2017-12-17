import os
from flask import g
from app.models import Week, Ranking, Submission, User, Team

from app import create_app, db
from app.database import init_db, gen_saturdays, gen_data

app = create_app(os.environ.get("FLASK_CONFIG") or "default")
# with app.app_context():
#     g.myVar = "hello, world"
#     print(g.get('myVar'))
# app.config['user_reloader'] = False

from flask_script import Manager, Shell

manager = Manager(app)

# configure shell and migration commands
def make_shell_context():
    return dict(app=app, db=db, Week=Week, Ranking=Ranking, Submission=Submission, User=User, Team=Team)
manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def init():
    init_db()

@manager.command
def init_all(start="2017-12-1", weeks=4):
    init_db()
    gen_data()
    gen_saturdays(start=start, weeks=weeks)


# Pass in date="YYYY-M-D"
# @manager.command
@manager.option('-s', '--start', dest='start', default="2017-9-2")
@manager.option('-w', '--weeks', dest='weeks', default=13, type=int)
def start_season(start, weeks):
    gen_saturdays(start=start, weeks=weeks)


@manager.option('-w', '--weeks', dest='weeks', default=13, type=int)
@manager.option('-p', '--positions', dest='positions', default=10, type=int)
def populate(weeks, positions):
    gen_data(weeks=weeks, num_positions=positions)


@manager.command
def create_db():
    db.metadata.create_all(bind=db.engine)


@manager.command
def drop_db():
    db.metadata.drop_all(bind=db.engine)


@app.before_first_request
def before_first_request():
    # init_db(start="2017-9-2")
    pass

if __name__ == "__main__":
    # init_db()
    manager.run()
else:
    print("Starting app on Heroku")