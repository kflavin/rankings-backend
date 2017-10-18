import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from app.models import Ranking as RankingModel
from app.models import Submission as SubmissionModel
from app.models import Team as TeamModel
from app.models import User as UserModel
from app.models import Week as WeekModel

from app.database import session

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


class CreateUser(graphene.Mutation):
    user = graphene.Field(User)
    # active = graphene.Boolean()

    class Input:
        name = graphene.String()
        password = graphene.String()
        active = graphene.Boolean()

    @staticmethod
    def mutate(cls, input, context, info):


        user = UserModel(name=input.get('name'),
                    password=input.get('password'),
                    active=input.get('active'))

        # user = User(name="kyle2", password="password", active=input.get('active'))

        session.add(user)
        session.commit()
        # return CreateUser(id=user.id, name=user.name, password=user.password, active=user.active)
        return CreateUser(user=user)


class Mutation(graphene.AbstractType):
    # name = "Mutations"
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_users = SQLAlchemyConnectionField(User)
    all_teams = SQLAlchemyConnectionField(Team)
    all_weeks = SQLAlchemyConnectionField(Week)
    all_submissions = SQLAlchemyConnectionField(Submission)
    all_rankings = SQLAlchemyConnectionField(Ranking)


class Mutations(Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutations, types=[User, Team, Week, Submission, Ranking])
# schema = graphene.Schema(query=Query, mutation=Mutation)