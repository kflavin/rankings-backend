import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from app.models import User as UserModel
from app.database import session


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
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

        user.set_password(input.get('password'))

        # user = User(name="kyle2", password="password", active=input.get('active'))

        session.add(user)
        session.commit()
        # return CreateUser(id=user.id, name=user.name, password=user.password, active=user.active)
        return CreateUser(user=user)


class LoginUser(graphene.Mutation):
    token = graphene.String()

    class Input:
        username = graphene.String()
        password = graphene.String()

    @staticmethod
    def mutate(cls, input, context, info):
        user = UserModel.query.filter_by(name=input.get('username')).first()
        if user:
            if user.verify_password(input.get('password')):
                return LoginUser(token=user.encode_auth_token())

        raise Exception("Invalid User")

# class LoginUser(graphene.Mutation):
#     user = graphene.Field()
#
#     class Input:
#         username = graphene.String()
#         password = graphene.String()
#
#     @staticmethod
#     def mutate(root, input, context, info):
#         user = "blah"