from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from ..middleware.authorization import AuthoizationMiddleware


class get_nfes(APIView):
    def get(request):
        data_user = request.body
        try:
            return HttpResponse(status=501)
        except ValueError as err:
            return HttpResponse(status=500)
        
class get_nfe(APIView):
    def get(request, nfe_id):
        data_user = request.body
        try:
            return HttpResponse(status=501)
        except ValueError as err:
            return HttpResponse(status=500)
        
class get_full_nfe(APIView):
    def get(request, nfe_id):
        data_user = request.body
        try:
            return HttpResponse(status=501)
        except ValueError as err:
            return HttpResponse(status=500)
        

        

