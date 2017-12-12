import os
from app import create_app, init_db

from app.database import gen_saturdays

app = create_app("default")
# app.config['user_reloader'] = False

from flask_script import Manager, Shell

manager = Manager(app)

@manager.command
def init():
    init_db()

# Pass in date="YYYY-M-D"
# @manager.command
@manager.option('-s', '--start', dest='start', default="2017-9-2")
@manager.option('-w', '--weeks', dest='weeks', default=13, type=int)
def start_season(start, weeks):
    gen_saturdays(start=start, weeks=weeks)



@app.before_first_request
def before_first_request():
    # init_db(start="2017-9-2")
    pass

if __name__ == "__main__":
    # init_db()
    manager.run()
else:
    print("Starting app on Heroku")