import graphene
import datetime
from datetime import date, timedelta
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy import func, desc, and_, or_

from app.models import Ranking as RankingModel
from app.models import Submission as SubmissionModel
from app.models import Team as TeamModel
from app.models import Week as WeekModel
from app.models import User as UserModel

from flask import request

from app.schema.auth import User, CreateUser, LoginUser, get_user
from app.schema.submission import Submission, CreateSubmission, WeeklyRanking, get_submission

from app import db
session = db.session

# from app.utils import isActive

class Team(SQLAlchemyObjectType):
    class Meta:
        model = TeamModel


class Week(SQLAlchemyObjectType):
    class Meta:
        model = WeekModel

    active = graphene.Boolean()
    last = graphene.Boolean()

    def resolve_active(self, args, context, info):
        print("resolving active...")
        return self.active

    def resolve_last(self, args, context, info):
        print("resolving last...")
        return self.last


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
    weeks = graphene.List(Week, year=graphene.Int(), num=graphene.Int(default_value=0), id=graphene.Int(default_value=0))
    submissions = graphene.List(Submission, id=graphene.Int(), year=graphene.Int(), num=graphene.Int(), user=graphene.String())
    rankings = graphene.List(Ranking)
    current_week = graphene.Field(Week)
    my_submission = graphene.Field(Submission)
    week_ranking = graphene.Field(WeeklyRanking, weeknum=graphene.Int(), year=graphene.Int())
    all_years = graphene.List(graphene.Int)

    def resolve_all_years(self, args, context, info):
        print("getting all years")
        # wks = list(map(lambda w: w.date.year, WeekModel.query.group_by(func.extract('year', WeekModel.date)).all()))
        # db.session.query(func.extract('year', Week.date).label('h')).group_by('h').all()
        # wks.reverse()
        # Week.query.order_by(desc(func.extract('year', Week.date))).first().date.year
        # seem to need this form for postgres.  func.extract isn't working inside of a group_by
        wks = [ 
            i.date.year 
            # Exclude January months, as they count towards previous year
            # for i in WeekModel.query.distinct(func.extract('year', WeekModel.date)).order_by(desc(func.extract('year', WeekModel.date))).all() 
            for i in WeekModel.query.filter(func.extract('month', WeekModel.date) != 1).distinct(func.extract('year', WeekModel.date)).order_by(desc(func.extract('year', WeekModel.date))).all() 
            ]
        return wks


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
        num = args.get('weeknum')
        year = args.get('year')
        if not num:
            j = WeekModel.current_week_rankings()
        else:
            j = WeekModel.week_rankings(num, year)

        return WeeklyRanking(rankings=j)

    def resolve_current_week(self, args, context, info):
        # return WeekModel.query.order_by(WeekModel.date.desc()).first()
        return WeekModel.current_week()

    def resolve_submissions(self, args, context, info):
        num = args.get('num')
        year = args.get('year')
        user = args.get('user')
        id = args.get('id')

        if id:
            return SubmissionModel.query.filter_by(id=args.get('id')).all()
        else:
            # return SubmissionModel.query.all()
            user_id = UserModel.query.filter(UserModel.name.ilike(user)).first().id

            return SubmissionModel.query.join(WeekModel).\
                filter(func.extract('year', WeekModel.date) == year).\
                filter(WeekModel.num==num).join(UserModel).\
                filter(UserModel.id == user_id).all()

    @graphene.resolve_only_args
    def resolve_teams(self):
        return TeamModel.query.all()

    def resolve_weeks(self, args, context, info):
        year = args.get('year')
        num = args.get('num')

        if year and num:
            # return WeekModel.query.filter(WeekModel.num == num).all()
            return WeekModel.query.filter(WeekModel.num == num).filter(func.extract('year', WeekModel.date) == year).all()
        # if year and not num:
        #     allWeeks = WeekModel.query.filter(func.extract('year', WeekModel.date) == year).all()
        #     return addActive(allWeeks)
        else:
            # Replace this query with the one below, to exclude January.
            # year = year if year else session.query(func.max(WeekModel.date)).first()[0].year
            year = year if year else session.query(func.max(WeekModel.date)).filter(func.extract('month', WeekModel.date) != 1).first()[0].year

            # Use a query for allWeeks that also returns the following January
            # allWeeks =  WeekModel.query.filter(func.extract('year', WeekModel.date) == year).all()
            allWeeks = WeekModel.query.filter(or_(func.extract('year', WeekModel.date) == year, \
                    and_(func.extract('year', WeekModel.date) == year+1, func.extract('month', WeekModel.date) == 1))).all()
            for week in allWeeks:
                print("%s %s" % (week.date, week.active))
                if week.isActive():
                    print("setting to true")
                    week.active = True
                if week.isLast():
                    print("last is true")
                    week.last = True
            return allWeeks

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
        print("Looking for submissions from user %s" % user)
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