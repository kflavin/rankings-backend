from random import shuffle

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import date

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

session=db_session

Base = declarative_base()
Base.query = session.query_property()


def init_db():
    from models import Week, User, Team, Submission, Ranking
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # create fixtures

    # Add week
    week1 = Week(date=date(2017, 10, 7))
    session.add(week1)

    # add users
    kyle = User(name="Kyle")
    frank = User(name="Frank")
    jeff = User(name="Jeff")

    session.add_all([kyle, frank, jeff])

    # add submissions
    s1 = Submission(week=week1, user=kyle)
    s2 = Submission(week=week1, user=frank)
    s3 = Submission(week=week1, user=jeff)
    session.add_all([s1, s2, s3])

    # add teams
    session.add_all(list(map(lambda x: Team(name=x), list("abcdefg"))))

    session.commit()

    # establish some rankings
    teams = Team.query.all()
    print("Your teams are %s" % teams)
    positions = list(range(1, len(teams)+1))
    shuffle(positions)
    for i in teams:
        print("Adding %s to s1" % i)
        r = Ranking(position=positions.pop(), submission=s1, team=i)
        session.add(r)

    positions = list(range(1, len(teams)+1))
    shuffle(positions)
    for i in teams:
        print("Adding %s to s2" % i)
        r = Ranking(position=positions.pop(), submission=s2, team=i)
        session.add(r)

    positions = list(range(1, len(teams)+1))
    shuffle(positions)
    for i in teams:
        print("Adding %s to s3" % i)
        r = Ranking(position=positions.pop(), submission=s3, team=i)
        session.add(r)

    session.commit()