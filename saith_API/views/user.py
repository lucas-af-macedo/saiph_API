from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from ..middleware.user import UserMiddleware, SignUpMiddleware
from ..services import user_service
from rest_framework.parsers import JSONParser

class sign_in(APIView):
    @UserMiddleware
    def post(request):
        data_user = request.data_user
        try:
            user = user_service.get_user(data_user)

            return JsonResponse(user, status=200)
        except ValueError as err:
            return HttpResponse(status=500)


class sign_up(APIView):
    @SignUpMiddleware
    def post(request):
        data_user = request.data_user
        try:
            user = user_service.sign_up(data_user)
            
            return HttpResponse(status=201)
        except ValueError as err:
            return HttpResponse(status=500)
        
class teste(APIView):
    def post(self, request):
        uploaded_file = request.FILES['file']
        password = request.POST.get('password')
        try:
            user = user_service.teste(uploaded_file, password)
            
            return HttpResponse(status=201)
        except ValueError as err:
            return HttpResponse(status=500)