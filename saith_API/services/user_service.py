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
    user = user_repository.get_user(email)

    if(not len(user)):
        raise ValueError('user or password are wrong')
    
    if(not check_password(password, user[0].password)):
        raise ValueError('user or password are wrong')
    
    user_object = UserOnlyIdAndName(user[0]).data

    token = get_token(user_object['id'])
    user_object['token'] = token
    
    return user_object

    

def get_token(user_id):
    payload = {'user_id': user_id, 'iat': datetime.utcnow()}
    secret_key = os.getenv('SECRET_KEY')

    token = jwt.encode(payload, secret_key, algorithm='HS256')

    user_repository.insert_token(user_id, token)
    
    return token
