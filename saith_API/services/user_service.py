from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from ..repository import user_repository
from ..serializers.user_serializer import UserOnlyIdAndName
from datetime import datetime
import jwt
import os

def get_user(data_user):
    password = data_user['password']
    email = data_user['email']
    user = get_user_by_email(email)

    if(not len(user)):
        raise ValueError('user or password are wrong')
    
    if(not check_password(password, user[0].password)):
        raise ValueError('user or password are wrong')
    
    user_object = UserOnlyIdAndName(user[0]).data

    token = get_token(user_object['id'])
    user_object['token'] = token
    
    return user_object

def sign_up(data_user):
    email = data_user['email']
    password = data_user['password']
    confirm_password = data_user['confirmPassword']
    name = data_user['name']

    if password != confirm_password:
        raise ValueError('The password dont match!')
    
    user = get_user_by_email(email)
    if(len(user)):
        raise ValueError('This email is in use!')
    
    password_hashed = make_password(password)

    user_repository.insert_user(name=name, email=email, password=password_hashed)

    return None


def get_user_by_email(email):
    user = user_repository.get_user(email)

    return user
    

def get_token(user_id):
    payload = {'user_id': user_id, 'iat': datetime.now()}
    secret_key = os.getenv('SECRET_KEY')

    token = jwt.encode(payload, secret_key, algorithm='HS256')

    user_repository.insert_token(user_id, token)
    
    return token
