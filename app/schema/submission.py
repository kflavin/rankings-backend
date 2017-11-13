import graphene
from sqlalchemy import func
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from app.models import (Submission as SubmissionModel, Week as WeekModel, User as UserModel, Ranking as RankingModel,
                    Team as TeamModel)
from app.database import session


def get_submission(user):
    # submission = SubmissionModel.query.filter(UserModel.name == user.name).first()
    current_week = WeekModel.query.order_by(WeekModel.date.desc()).first()
    submission = SubmissionModel.query.join(WeekModel).filter(WeekModel.id == current_week.id).join(UserModel).filter(UserModel.name == user.name).first()
    return submission

class Submission(SQLAlchemyObjectType):
    class Meta:
        model = SubmissionModel


class CreateSubmission(graphene.Mutation):
    submission = graphene.Field(Submission)
    # active = graphene.Boolean()

    class Input:
        weekid = graphene.Int()
        teams = graphene.List(graphene.String)
        userid = graphene.Int()

    @staticmethod
    def mutate(cls, input, context, info):
        weekid = input.get('weekid')
        userid = input.get('userid')
        team_names = input.get('teams')

        print("Your teams are %s" % str(team_names))

        teams = []
        for team_name in team_names:
            team = TeamModel.query.filter(func.lower(TeamModel.name)==func.lower(team_name)).first()
            if team:
                teams.append(team)
            else:
                raise Exception("Team %s does not exist." % team_name)


        # filtering with func.date seems to be required to ignore "time" part added by func.now() in model
        # Week.query.filter(func.date(Week.date)==datetime.date(2017, 11, 8)).first()

        week = WeekModel.query.filter_by(id=weekid).first()
        user = UserModel.query.filter_by(id=userid).first()

        submission = SubmissionModel(week=week, user=user)
        session.add(submission)

        for index, team in enumerate(teams):
            r = RankingModel(position=index+1, submission=submission, team=team)
            session.add(r)

        session.commit()

        return CreateSubmission(submission=submission)
