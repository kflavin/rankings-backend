import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from app.models import Ranking as RankingModel


class Ranking(SQLAlchemyObjectType):
    class Meta:
        model = RankingModel


class RankingQuery(object):
    rankings = graphene.List(Ranking)
    rankingsById = graphene.Int(id=graphene.Int())
    rankingsByWeek = graphene.List(Ranking, weekid=graphene.Int())

    def resolve_rankingsByWeek(self, info, weekid):
        return "hello, world %s" % weekid

    def resolve_rankingsById(self, info):
        return "rankingsById"

    # @graphene.resolve_only_args
    # def resolve_rankings(self, args, context, info):
    def resolve_rankings(self, info):
        print("resolve_ranking")
        return Ranking.get_query({}).all()

    # @graphene.resolve_only_args
    def resolve_name(self, info, name):
        # print(args)
        # print(context)
        # print(dir(context))
        # print(info)
        # print(dir(Ranking))
        # print(dir(Ranking.get_node(1, context, info)))
        # print(Ranking.get_node(1, context, info).team)
        # print(Ranking.get_node(2, context, info).team)
        return Ranking.get_query().all()


class Queries(RankingQuery, graphene.ObjectType):
    pass


# class Mutations(Mutation, graphene.ObjectType):
#     pass

schema = graphene.Schema(query=Queries)