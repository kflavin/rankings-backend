import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from app.models import User as UserModel
from app import db

from app.utils import sendMail

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


class ConfirmUser(graphene.Mutation):
    # This is what we're returning
    user = graphene.Field(User)

    class Arguments:
        email = graphene.String()
        token = graphene.String()

    @staticmethod
    def mutate(root, info, **args):
        print("performing confirm mutation")
        email = args.get('email').strip()
        token = args.get('token').strip()
        user = UserModel.query.filter_by(email=email).first()

        if not user:
            raise Exception("Error with confirmation.")
        
        if user.confirmation_token == token:
            user.confirmation_token = "confirmed"
            user.active = True
            session.add(user)
            session.commit()
        else:
            raise Exception("Could not confirm user.")

        return ConfirmUser(user=user)


class CreateUser(graphene.Mutation):
    user = graphene.Field(User)
    # active = graphene.Boolean()

    class Arguments:
        email = graphene.String()
        name = graphene.String()
        password = graphene.String()

    @staticmethod
    def mutate(root, info, **args):
        print("Create user...")
        if UserModel.query.filter_by(name = args.get('name')).first():
            raise Exception("User already exists.")

        user = UserModel(name=args.get('name'),
                         email=args.get('email'),
                         password=args.get('password'),
                         active=False)

        user.set_password(args.get('password'))

        sendMail("Kyle@kyle-flavin.com", user.email, "Rankings Registration", "Click this link to register... (add link here)", "html stuff here")

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
                if user.active:
                    return LoginUser(token=user.encode_auth_token().decode(), userid=user.id)
                else:
                    raise Exception("Please activate your account.")

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