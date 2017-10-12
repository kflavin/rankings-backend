import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import Team as TeamModel
from models import User as UserModel
from models import Week as WeekModel
from models import Submission as SubmissionModel
from models import Ranking as RankingModel


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)


class Team(SQLAlchemyObjectType):
    class Meta:
        model = TeamModel
        interfaces = (relay.Node,)


class Week(SQLAlchemyObjectType):
    class Meta:
        model = WeekModel
        interfaces = (relay.Node,)


class Submission(SQLAlchemyObjectType):
    class Meta:
        model = SubmissionModel
        interfaces = (relay.Node,)


class Ranking(SQLAlchemyObjectType):
    class Meta:
        model = RankingModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_users = SQLAlchemyConnectionField(User)
    all_teams = SQLAlchemyConnectionField(Team)
    all_weeks = SQLAlchemyConnectionField(Week)
    all_submissions = SQLAlchemyConnectionField(Submission)
    all_rankings = SQLAlchemyConnectionField(Ranking)


schema = graphene.Schema(query=Query, types=[User, Team, Week, Submission, Ranking])