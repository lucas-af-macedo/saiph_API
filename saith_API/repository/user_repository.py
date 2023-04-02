from ..models import Users, Sessions

def get_user(email):
    user = Users.objects.filter(email=email)

    return user

def insert_token(user_id, token):
    session = Sessions.objects.create(user_id=user_id, token=token)

    return session

