from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from ..middleware.user import UserMiddleware
from ..repository import get_user
from ..serializers.teste import UserSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core import serializers
from rest_framework.authtoken.models import Token
from ..token import my_user_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from ..models import Users

class sign_in(APIView):
    @UserMiddleware
    def post(request):
        user = request.data_user
        hashed_password = make_password(user['password'])
        
        a = get_user.main(user['email'])
        print(force_bytes(a.pk))
        token = my_user_token_generator.make_token(a)
        oi = token.split('-')[0]
        print(urlsafe_base64_decode(oi))
        uid = urlsafe_base64_encode(token.encode())
        print(token)
        data = UserSerializer(a)
        return JsonResponse(data.data,status=200)

def dicionario(lista):
    type_list = str(type(lista))
    object_list = {}
    if ('prisma.models' in type_list):
        for i in lista:
            if (type(i[1]) is list):
                sub_list = []
                for i2 in i[1]:
                    sub_list.append(dicionario(i2))
                object_list[i[0]] = sub_list
            else:
                object_list[i[0]] = i[1]
    return object_list
