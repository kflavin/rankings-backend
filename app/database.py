from datetime import date
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

def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # create fixtures

    # Top 10, Top 25, etc
    num_positions = 10
    positions = list(range(num_positions))

    # Add week
    week1 = Week(date=date(2017, 9, 1))
    week2 = Week(date=date(2017, 10, 1))
    week3 = Week(date=date(2017, 11, 1))
    session.add_all([week1, week2, week3])

    # add users
    kyle = User(name="Kyle")
    frank = User(name="Frank")
    jeff = User(name="Jeff")
    matt = User(name="Matt")
    brian = User(name="Brian")

    session.add_all([kyle, frank, jeff])

    # add w1 submissions
    w1s1 = Submission(week=week1, user=kyle)
    w1s2 = Submission(week=week1, user=frank)
    w1s3 = Submission(week=week1, user=jeff)
    w1s4 = Submission(week=week1, user=matt)
    w1s5 = Submission(week=week1, user=brian)
    w2s1 = Submission(week=week2, user=kyle)
    w2s2 = Submission(week=week2, user=frank)
    w2s3 = Submission(week=week2, user=jeff)
    w2s4 = Submission(week=week2, user=matt)
    w2s5 = Submission(week=week2, user=brian)
    w3s1 = Submission(week=week3, user=kyle)
    w3s2 = Submission(week=week3, user=frank)
    w3s3 = Submission(week=week3, user=jeff)
    w3s4 = Submission(week=week3, user=matt)
    w3s5 = Submission(week=week3, user=brian)

    session.add_all([w1s1, w1s2, w1s3, w1s4, w1s5,
                     w2s1, w2s2, w2s3, w2s4, w2s5,
                     w3s1, w3s2, w3s3, w3s4, w3s5])

    # add teams
    # session.add_all(list(map(lambda x: Team(name=x), list("abcdefg"))))

    # add teams
    f = open("app/teams.txt", 'r')
    contents = f.read()
    teams = []
    for team in contents.strip().split("\n"):
        print("Adding team: %s" % team)
        teams.append(Team(name=team))

    session.add_all(teams)


    session.commit()

    # establish some rankings
    teams = Team.query.all()
    print("Your teams are %s" % teams)
    # positions = list(range(1, len(teams)+1))

    # shuffle(positions)
    # for i in teams:
    #     print("Adding %s to s1" % i)
    #     r = Ranking(position=positions.pop(), submission=s1, team=i)
    #     session.add(r)
    #
    # positions = list(range(1, len(teams)+1))
    # shuffle(positions)
    # for i in teams:
    #     print("Adding %s to s2" % i)
    #     r = Ranking(position=positions.pop(), submission=s2, team=i)
    #     session.add(r)
    #
    # positions = list(range(1, len(teams)+1))
    # shuffle(positions)
    # for i in teams:
    #     print("Adding %s to s3" % i)
    #     r = Ranking(position=positions.pop(), submission=s3, team=i)
    #     session.add(r)

    # session.commit()

    gen_rankings(teams, w1s1, positions)
    gen_rankings(teams, w1s2, positions)
    gen_rankings(teams, w1s3, positions)
    gen_rankings(teams, w1s4, positions)
    gen_rankings(teams, w1s5, positions)
    gen_rankings(teams, w2s1, positions)
    gen_rankings(teams, w2s2, positions)
    gen_rankings(teams, w2s3, positions)
    gen_rankings(teams, w2s4, positions)
    gen_rankings(teams, w2s5, positions)
    gen_rankings(teams, w3s1, positions)
    gen_rankings(teams, w3s2, positions)
    gen_rankings(teams, w3s3, positions)
    gen_rankings(teams, w3s4, positions)
    gen_rankings(teams, w3s5, positions)


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