from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from ..middleware.user import UserMiddleware
from ..services import user_service

class sign_in(APIView):
    @UserMiddleware
    def post(request):
        data_user = request.data_user
        try:
            user = user_service.get_user(data_user)

            return JsonResponse(user, status=200)
        except ValueError as err:
            return HttpResponse(status=500)

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
