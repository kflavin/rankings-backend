from datetime import date, timedelta
from random import shuffle

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

session=db_session

Base = declarative_base()
Base.query = session.query_property()

from app.models import Week, User, Team, Submission, Ranking

def init_db(start, weeks=13, num_positions=10):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # create fixtures

    # Top 10, Top 25, etc
    # num_positions = 10
    positions = list(range(num_positions))

    # Add weeks
    saturdays_2015 = gen_saturdays(weeks=weeks, start="2015-8-31")    
    saturdays_2016 = gen_saturdays(weeks=weeks, start="2016-9-1")    
    saturdays_2017 = gen_saturdays(weeks=weeks, start=start)
    
    # Week.new()

    # add users
    kyle = User(name="Kyle")
    frank = User(name="Frank")
    jeff = User(name="Jeff")
    matt = User(name="Matt")
    brian = User(name="Brian")

    kyle.set_password("kyle")
    frank.set_password("frank")
    jeff.set_password("jeff")
    matt.set_password("matt")
    brian.set_password("brian")

    users = [kyle, frank, jeff, matt, brian]
    session.add_all(users)

    add_teams()


    top_teams = Team.query.filter(Team.name.in_(['Alabama', 'Clemson', 'Miami (FL)', 'Oklahoma',
                                                 'Wisconsin', 'Auburn', 'Georgia', 'Notre Dame',
                                                 'Ohio State', 'Penn State', 'USC', 'TCU', 'Washington State',
                                                 ])).all()

    add_submissions(saturdays_2015, users, top_teams, positions)
    add_submissions(saturdays_2016, users, top_teams, positions)
    add_submissions(saturdays_2017, users, top_teams, positions, open=1)

    # for submission in submissions:
        # gen_rankings(top_teams, submission, positions)


def add_submissions(saturdays, users, teams, positions, open=0):
    # "open" is the number of weeks to leave available for testing (no rankings submitted for those weeks)
    submissions = []
    for num,saturday in enumerate(saturdays):
        if num >= len(saturdays) - open:
            break

        for user in users:
            submissions.append(Submission(week=saturday, user=user))

    session.add_all(submissions)
    session.commit()

    for submission in submissions:
        gen_rankings(teams, submission, positions)

    # return submissions


def add_teams(file="app/teams.txt"):
    # add teams
    f = open("app/teams.txt", 'r')
    contents = f.read()
    teams = []
    for team in contents.strip().split("\n"):
        print("Adding team: %s" % team)
        teams.append(Team(name=team))

    session.add_all(teams)
    session.commit()


def gen_rankings(teams, submission, positions=10):
    # positions = list(range(1, len(teams)+1))
    shuffle(teams)

    for position in positions:
        r = Ranking(position=position+1, submission=submission, team=teams[position])
        session.add(r)


    # shuffle(positions)
    #
    # for i in teams:
    #     print("Adding %s to submission %s" % (i, submission))
    #     r = Ranking(position=positions.pop(), submission=submission, team=i)
    #     session.add(r)

    session.commit()


def gen_saturdays(start="2017-9-2", weeks=13):
    args = list(map(lambda x: int(x), start.split("-")))
    start = date(*args)
    delta = timedelta(days=7)

    curr = start
    saturdays = []
    for i in range(weeks+1):
        saturdays.append(curr)
        curr += delta

    weeks = []
    for num,saturday in enumerate(saturdays):
        weeks.append(Week(date=saturday, num=num+1))

    session.add_all(weeks)
    session.commit()

    return weeks