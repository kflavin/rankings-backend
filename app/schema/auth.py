import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from app.models import User as UserModel
from app import db
session = db.session

def get_user(context):
    header = context.headers.get('Authorization')
    print("header is")
    print(header)

    print("header is: " + header)
    if header:

        tokenized_header = header.split(" ")
        if len(tokenized_header) < 2:
            raise Exception("Auth token is either invalid or not present")
        _,token = tokenized_header

        print("token is " + token)

        userid = UserModel.decode_auth_token(token)
        if isinstance(userid, int) and userid > 0:
            print("Decoded user id: " + str(userid))
            user = UserModel.query.filter_by(id=userid).first()
            if user:
                print("found user: " + str(user))
                return user
        else:
            print("userid not found " + str(userid))
            raise Exception("Not logged in")
    else:
        print("not found")
        raise Exception("Not logged in")
    return None

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)


class CreateUser(graphene.Mutation):
    user = graphene.Field(User)
    # active = graphene.Boolean()

    class Arguments:
        name = graphene.String()
        password = graphene.String()
        active = graphene.Boolean()

    @staticmethod
    def mutate(root, info, **args):
        if UserModel.query.filter_by(name = args.get('name')).first():
            raise Exception("User already exists.")

        user = UserModel(name=args.get('name'),
                         password=args.get('password'),
                         active=args.get('active'))

        user.set_password(args.get('password'))

        # user = User(name="kyle2", password="password", active=input.get('active'))

        session.add(user)
        session.commit()
        # return CreateUser(id=user.id, name=user.name, password=user.password, active=user.active)
        return CreateUser(user=user)


class LoginUser(graphene.Mutation):
    token = graphene.String()
    userid = graphene.Int()

    class Arguments:
        username = graphene.String()
        password = graphene.String()

    @staticmethod
    def mutate(root, info, **args):
        user = UserModel.query.filter_by(name=args.get('username')).first()
        if user:
            if user.verify_password(args.get('password')):
                return LoginUser(token=user.encode_auth_token().decode(), userid=user.id)

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