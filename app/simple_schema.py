import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from app.models import Ranking as RankingModel
from app.models import Submission as SubmissionModel
from app.models import Team as TeamModel
from app.models import Week as WeekModel

from app.schema.auth import User, CreateUser, LoginUser


class Team(SQLAlchemyObjectType):
    class Meta:
        model = TeamModel


class Week(SQLAlchemyObjectType):
    class Meta:
        model = WeekModel


class Submission(SQLAlchemyObjectType):
    class Meta:
        model = SubmissionModel


class Ranking(SQLAlchemyObjectType):
    class Meta:
        model = RankingModel


class Mutation(graphene.AbstractType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()


class Query(graphene.AbstractType):
    teams = graphene.List(Team)
    weeks = graphene.List(Week, id=graphene.Int())
    submissions = graphene.List(Submission, id=graphene.Int())
    rankings = graphene.List(Ranking)

    def resolve_submissions(self, args, context, info):
        id = args.get('id')
        if id:
            return SubmissionModel.query.filter_by(id=args.get('id')).all()
        else:
            return SubmissionModel.query.all()

    @graphene.resolve_only_args
    def resolve_teams(self):
        return TeamModel.query.all()

    def resolve_weeks(self, args, context, info):
        id = args.get('id')
        if id:
            return WeekModel.query.filter_by(id=args.get('id')).all()
        else:
            return WeekModel.query.all()

    # @graphene.resolve_only_args
    # def resolve_submissions(self):
    #     return SubmissionModel.query.all()

    # @graphene.resolve_only_args
    # def resolve_rankings(self):
    #     return RankingModel.query.all()

    def resolve_rankings(self, args, context, info):
        return RankingModel.query.all()


class Queries(Query, graphene.ObjectType):
    pass


class Mutations(Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Queries, mutation=Mutations)