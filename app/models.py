import datetime
from calendar import timegm

import jwt
import operator
from collections import defaultdict
from sqlalchemy import *
from sqlalchemy.orm import (relationship, backref)
from flask import current_app

from app import bcrypt
from app.database import Base
from app.database import session


class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __str__(self):
        return "<Team: {}>".format(self.name)

    def __repr__(self):
        return "<Team: {}>".format(self.name)


class Week(Base):
    __tablename__ = 'week'
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=func.now())

    @staticmethod
    def new():
        w = Week()
        session.add(w)
        session.commit()
        return w

    @staticmethod
    def current_week_rankings():
        w = Week.query.order_by(Week.date.asc()).first()
        return Week.week_rankings(w.id)

    @staticmethod
    def week_rankings(weekid):
        """
        Given a week id, calculate the overall ranking for that week

        Return a dictionary of lists, with keys corresponding to ranks
        """

        w = Week.query.filter_by(id = weekid).first()
        submissions = Submission.query.filter(Submission.week_id == w.id).all()

        if not submissions:
            return []

        positions = len(submissions[0].rankings)
        points = list(range(positions, 0, -1))
        # print(points)

        teams = defaultdict(lambda: 0)

        for submission in submissions:
            for ranking in submission.rankings:
                # print("%s position %s, gets %s points" % (ranking.team.name,
                #                                     ranking.position,
                #                                     points[ranking.position-1]))
                teams[ranking.team.name] += points[ranking.position-1]


        # print(teams)

        top_teams = sorted(teams.items(), key=operator.itemgetter(1), reverse=True)
        # print(top_teams)

        # for top_team in top_teams:
            # print("%s: %s" % (top_team[0], top_team[1]))

        rank = 1
        rankings = []
        print("top teams")
        print(top_teams)
        while rank < 11:
            ranked_teams = [rank]
            pos = rank-1
            # s = "rank: %s" % (str(rank))
            # s += " %s" % top_teams[pos][0]
            ranked_teams.append(top_teams[pos][0])
            # print("rank %s and %s" % (str(rank), top_teams[pos][0]))
            rankings.append(ranked_teams)

            curr = 0

            while not rank >= 10 and top_teams[pos][1] == top_teams[pos+1][1]:
                ranked_teams = [""]
                # s += "\n\t %s" % top_teams[pos+1][0]
                ranked_teams.append(top_teams[pos+1][0])
                # print ("rank %s include %s " % (str(rank), top_teams[pos+1][0]))
                pos += 1
                curr += 1
                rankings.append(ranked_teams)

            if pos >= rank:
                # rank = ((pos + 1) - rank) + rank + 1
                rank = pos + 2
            else:
                rank += 1

            # print(s)
        print("rankings...")
        print(rankings)
        return rankings

    def __str__(self):
        return "<Week: {}>".format(self.date)

    def __repr__(self):
        return "<Week: {}>".format(self.date)


class Submission(Base):
    __tablename__ = 'submission'
    id = Column(Integer, primary_key=True)

    week_id = Column(Integer, ForeignKey('week.id'))
    week = relationship("Week", backref=backref('submissions', uselist=True,
                                              cascade='delete,all'))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", backref=backref('submissions', uselist=True,
                                              cascade='delete,all'))

    def display(self):
        if self.rankings:
            print("Week: %s, User: %s" % (self.week.date, self.user.name))
            for ranking in self.rankings:
                print("Ranking: %s, Team: %s" % (ranking.position, ranking.team.name))


    def __str__(self):
        return "<Submission: {} {} {}>".format(self.id, self.user, self.week)

    def __repr__(self):
        return "<Submission: {} {} {}>".format(self.id, self.user, self.week)


class Ranking(Base):
    __tablename__ = 'ranking'
    id = Column(Integer, primary_key=True)
    position = Column(Integer)
    submission_id = Column(Integer, ForeignKey('submission.id'))
    submission = relationship(Submission, backref=backref('rankings', uselist=True,
                                              cascade='delete,all'))
    team_id = Column(Integer, ForeignKey('team.id'))
    team = relationship(Team, backref=backref('rankings', uselist=True,
                                              cascade='delete,all'))

    def __str__(self):
        return "<Ranking: {} {} {}>".format(self.position,
                                               self.team, self.submission)

    def __repr__(self):
        return "<Ranking: {} {} {}>".format(self.position,
                                               self.team, self.submission)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String(255))
    active = Column(Boolean())

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password, 13).decode()
        print("Password set to %s" % self.password)
        session.add(self)
        session.commit()

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    # def encode_auth_token(self, user_id, exp=86400):
    def encode_auth_token(self, exp=86400):
        # user = User.query.filter_by(id=user_id).first()
        user_id = self.id
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=exp),
                'iat': datetime.datetime.utcnow(),
                'id': user_id
            }
            return jwt.encode(payload, "secret-key", algorithm="HS256")
        except Exception as e:
            print("error: %s" % e)

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decode auth token
        :param auth_token:
        :return: user id (int) or error string
        """
        try:
            # payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
            payload = jwt.decode(auth_token, "secret-key")
            user_id = payload.get('id')

            if user_id:
                user = User.query.filter_by(id=user_id).first()
                # last_reported_password_change = payload.get('last_password_change')
                # last_actual_password_change = timegm(user.last_password_change.utctimetuple())
                # if user and (last_reported_password_change >= last_actual_password_change):
                #     return user_id
                return user_id

            return 'Signature expired.  Please log in again.'
        except jwt.ExpiredSignature:
            return 'Signature expired.  Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token.  Please log in again'

    def __str__(self):
        return "<User: {}>".format(self.name)

    def __repr__(self):
        return "<User: {}>".format(self.name)




