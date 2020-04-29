import graphene
from backend.models import Dataset, User
from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from graphene_django.types import DjangoObjectType
from rest_framework_jwt.serializers import (
  JSONWebTokenSerializer,
  RefreshJSONWebTokenSerializer,
  jwt_decode_handler
)
from backend.utils import (
    only_user,
    only_admin,
    only_requester,
    Message
)

class UserType(DjangoObjectType):
    class Meta:
        model = User

class Users(graphene.ObjectType):
    message = graphene.Field(Message)
    users = graphene.List(UserType)

"""
mutation {
  createAccount(
    isRequester:false
    email:"guest@gmail.com",
    password:"guest",
    username:"guest",
    phone: "01028858793"
  ) {
    message {
      status
      message
    }
  }
}
"""
class CreateAccount(graphene.Mutation):
    message = graphene.Field(Message)

    class Arguments:
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()
        phone = graphene.String()
        is_requester = graphene.Boolean()
        is_robot = graphene.Boolean()
        
    def mutate(self, info, username, email, password, phone, is_requester=False, is_robot=False):
        try:
            res = User.objects.exclude().get(username=username)
            return CreateAccount(message=Message(status=False, message="이미 존재하는 아이디입니다."))
        except:
            # new_user = User.objects.create_user(username=username, email=email, password=password, phone=phone, is_requester=is_requester, is_robot=is_robot)
            # message = "'%s'님 정상적으로 가입되었습니다."%(new_user.username)
            # return CreateAccount(message=Message(status=True, message=message))
            new_user = User(username=username, email=email, password=password, phone=phone, is_requester=is_requester, is_robot=is_robot)
            try:
                new_user.full_clean()
            except ValidationError as e:
                return CreateAccount(message=Message(status=False, message=str(e)))
            else:
                new_user.set_password(password)
                new_user.save()
                message = "'%s'님 정상적으로 가입되었습니다."%(new_user.username)
                return CreateAccount(message=Message(status=True, message=message))
"""
mutation {
  updateAccount(
    phone:"01000000000"
    email:"guest@gmail.com"
    token:"참여자/의뢰자/관리자"
    oldPassword:"guest"
    username: "guest"
    newPassword:"guest1"
  ){
    message{
      status
      message
    }
    jwt
  }
}
"""
class UpdateAccount(graphene.Mutation):
    message = graphene.Field(Message)
    jwt = graphene.String()

    class Arguments:
        username = graphene.String()
        email = graphene.String()
        old_password = graphene.String()
        new_password = graphene.String()
        phone = graphene.String()
        token = graphene.String()

    @only_user
    def mutate(self, info, username, email, old_password, new_password, phone, token):
        res = jwt_decode_handler(token)
        user = User.objects.get(username=res['username'])
        if check_password(old_password, user.password):
            update = User(username=username, email=email, password=new_password, phone=phone)
            try:
                update.clean()
            except ValidationError as e:
                    return UpdateAccount(message=Message(status=False, message=str(e)))
            else:
                user.username = username
                user.email = email
                user.phone = phone
                user.set_password(new_password)
                user.save()
                user = {
                    'username': username,
                    'password': new_password
                    }
                serializer = JSONWebTokenSerializer(data=user)
                if serializer.is_valid():
                    token = serializer.object['token']
                    user = serializer.object['user']
                message = "개인정보가 정상적으로 변경되었습니다."
                return UpdateAccount(
                    message=Message(status=True, message=message),
                    jwt=token
                )
        else:
            return UpdateAccount(message=Message(status=False, message="비밀번호가 일치하지 않습니다."))

"""
mutation {
  loginAccount(username: "guest", password: "guest") {
    message {
      status
      message
    }
    jwt
  }
}
"""
class LoginAccount(graphene.Mutation):
    message = graphene.Field(Message)
    jwt = graphene.String() # json web token

    class Arguments:
        username = graphene.String()
        password = graphene.String()

    def mutate(self, info, username, password):
        user = {
          'username': username,
          'password': password
        }
        serializer = JSONWebTokenSerializer(data=user)
        if serializer.is_valid():
            token = serializer.object['token']
            user = serializer.object['user']
            return LoginAccount(message=Message(status=True, message="정상적으로 로그인 되었습니다."), jwt=token)
        return LoginAccount(message=Message(status=False, message="아이디 또는 비밀번호가 올바르지 않습니다."))

class RefreshToken(graphene.Mutation):
    message = graphene.Field(Message)
    jwt = graphene.String()

    class Arguments:
        token = graphene.String()

    def mutate(self, info, token):
        serializer = RefreshJSONWebTokenSerializer(data={'token': token})
        if serializer.is_valid():
            token = serializer.object['token']
            return RefreshToken(message=Message(), jwt=token)
        return RefreshToken(message=Message(status=False, message="토큰 재발급에 실패하였습니다."))

"""
mutation{
  deleteUser(
    password:"requester"
  	token:""
  ){
    message{
      status
      message
    }
  }
}
"""
# DeleteUser는 회원계정을 삭제하는 함수이다.
# user가 foreign key로 쓰이는 해당 record 값이 null로 변경됨.
class DeleteUser(graphene.Mutation):
    message = graphene.Field(Message)
    
    class Arguments:
        password = graphene.String()
        token = graphene.String()

    @only_user
    def mutate(self, info, password, token):
        res = jwt_decode_handler(token)
        user = User.objects.get(username=res['username'])
        if check_password(password, user.password):
            username = user.username
            user.delete()
            message="'%s'님 정상적으로 탈퇴되었습니다."%(username)
            return DeleteUser(
                message=Message(status=True, message=message)
            )
        else:
            message = "비밀번호가 일치하지 않습니다."
            return DeleteUser(
                message=Message(status=False, message=message)
                )
        

class Query(graphene.ObjectType):
    """
    query {
        getAllUser(token:"관리자") {
            users{
                username
                email
                phone
                point
                reliability
                isRequester
            }
            message{
              status
              message
            }
        }
    }
    """
    # 모든 사용자 반환
    get_all_user = graphene.Field(Users, token=graphene.String())
    @only_user
    @only_admin
    def resolve_get_all_user(self, info, **kwargs):
        users = User.objects.all()
        for user in users:
            user.password = "*****"
            user.email = user.email.split("@")[0][0:3] + "****" + "@" + user.email.split("@")[1]
        return Users(message=Message(status=True, message=""), users=users)