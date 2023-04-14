from ..models import Sessions

def get_session(token):
    user = Sessions.objects.get(token=token)

    return user