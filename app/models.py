import datetime
from calendar import timegm

import jwt
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




