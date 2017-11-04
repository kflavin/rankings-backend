import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from app.models import Ranking as RankingModel





class Ranking(SQLAlchemyObjectType):
    class Meta:
        model = RankingModel


class RankingQuery(graphene.AbstractType):
    rankings = graphene.List(Ranking)
    rankingsById = graphene.Int(id=graphene.Int())

    def resolve_rankingsById(self, args, context, info):
        return "hello"


    @graphene.resolve_only_args
    # def resolve_rankings(self, args, context, info):
    def resolve_rankings(self):
        return Ranking.get_query({}).all()

    # @graphene.resolve_only_args
    def resolve_name(self, args, context, info):
        # print(args)
        # print(context)
        # print(dir(context))
        # print(info)
        print(dir(Ranking))
        print(dir(Ranking.get_node(1, context, info)))
        print(Ranking.get_node(1, context, info).team)
        print(Ranking.get_node(2, context, info).team)
        return Ranking.get_query(args).all()


# # class Mutation(graphene.AbstractType):
# #     create_user = CreateUser.Field()
# #     login_user = LoginUser.Field()
#
#
# class Query(graphene.AbstractType):
#     teams = graphene.List(Team)
#     weeks = graphene.List(Week, id=graphene.Int())
#     submissions = graphene.List(Submission, id=graphene.Int())
#     rankings = graphene.List(Ranking)
#
#     def resolve_submissions(self, args, context, info):
#         id = args.get('id')
#         if id:
#             return SubmissionModel.query.filter_by(id=args.get('id')).all()
#         else:
#             return SubmissionModel.query.all()
#
#     @graphene.resolve_only_args
#     def resolve_teams(self):
#         return TeamModel.query.all()
#
#     def resolve_weeks(self, args, context, info):
#         id = args.get('id')
#         if id:
#             return WeekModel.query.filter_by(id=args.get('id')).all()
#         else:
#             return WeekModel.query.all()
#
#     # @graphene.resolve_only_args
#     # def resolve_submissions(self):
#     #     return SubmissionModel.query.all()
#
#     # @graphene.resolve_only_args
#     # def resolve_rankings(self):
#     #     return RankingModel.query.all()
#
#     def resolve_rankings(self, args, context, info):
#         return RankingModel.query.all()


class Queries(RankingQuery, graphene.ObjectType):
    pass


# class Mutations(Mutation, graphene.ObjectType):
#     pass

schema = graphene.Schema(query=Queries)