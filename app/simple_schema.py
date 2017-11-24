import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from app.models import Ranking as RankingModel
from app.models import Submission as SubmissionModel
from app.models import Team as TeamModel
from app.models import Week as WeekModel

from flask import request

from app.schema.auth import User, CreateUser, LoginUser, get_user
from app.schema.submission import Submission, CreateSubmission, WeeklyRanking, get_submission


class Team(SQLAlchemyObjectType):
    class Meta:
        model = TeamModel


class Week(SQLAlchemyObjectType):
    class Meta:
        model = WeekModel


# class Submission(SQLAlchemyObjectType):
#     class Meta:
#         model = SubmissionModel


class Ranking(SQLAlchemyObjectType):
    class Meta:
        model = RankingModel


class Mutation(graphene.AbstractType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
    create_submission = CreateSubmission.Field()


class Person(graphene.ObjectType):
    name = graphene.String()
    age = graphene.Int()
    height = graphene.Int()

    def resolve_name(self, args, context, info):
        print("resolving name...")
        return self.name

    def resolve_age(self, args, context, info):
        print("resolving age")
        print(args)
        return self.age

    def resolve_height(self, args, context, info):
        print("resolving height")
        print("now your height is " + str(args.get('height')))
        print(args)
        return self.height

class MyJson(graphene.ObjectType):
    json = graphene.types.json.JSONString()
    week = graphene.Int(default_value=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Initialize...")
        print(args)
        print(kwargs)

    

    def resolve_json(self, args, context, info):
        print("resolve json")
        print(args)
        self.json = {
            "1": ["Alabama"],
            "3": ["Clemson"],
            "5": ["Miami"]
        }
        return self.json


class Query(graphene.AbstractType):
    teams = graphene.List(Team)
    weeks = graphene.List(Week, id=graphene.Int())
    submissions = graphene.List(Submission, id=graphene.Int())
    rankings = graphene.List(Ranking)
    current_week = graphene.Field(Week)
    my_submission = graphene.Field(Submission)
    week_ranking = graphene.Field(WeeklyRanking, weekid=graphene.Int(default_value=0))

    my_person = graphene.Field(Person, height=graphene.Argument(graphene.Int, default_value=71, description="height in inches!"),
                                age=graphene.Int(default_value=23),
                                name=graphene.String(default_value="Kyle"))

    my_json = graphene.Field(MyJson)

    def resolve_my_json(self, args, context, info):
        import json
        j = {
            "1": ["Alabama"],
            "2": ["Clemson"],
            "3": ["Miami"]
        }
        return MyJson(week=1, json=j)

    def resolve_my_person(self, args, context, info):
        print("resolving person...")
        print(args)
        print("Your height is " + str(args.get('height')))
        p= Person(name=args.get('name'), height=args.get('height'), age=args.get('age'))
        print(p.name + " " + str(p.age) + " " + str(p.height))
        return p

    def resolve_week_ranking(self, args, context, info):
        weekid = args.get('weekid')
        if weekid == 0:
            j = WeekModel.current_week_rankings()
        else:
            j = WeekModel.week_rankings(weekid)

        return WeeklyRanking(rankings=j)

    def resolve_current_week(self, args, context, info):
        return WeekModel.query.order_by(WeekModel.date.desc()).first()

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

    # def resolve_my_submission(self, args, context, info):
    def resolve_my_submission(self, args, context, info):
        user = get_user(context)
        if user:
            print("User is : " + str(user))
            submission = get_submission(user)
            return submission
            
            # if submission:
            #     print("Submission is : " + str(submission))
            #     return submission
            # else:
            #     raise Exception("Could not find submission for user")
        else:
            raise Exception("User not logged in")


class Queries(Query, graphene.ObjectType):
    pass


class Mutations(Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Queries, mutation=Mutations)