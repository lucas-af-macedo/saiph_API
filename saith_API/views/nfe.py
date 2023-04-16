from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from ..middleware.authorization import AuthoizationMiddleware
from ..services import nfe_service


class get_nfes(APIView):
    def get(self, request, user_document_value_id):
        user_id = request.user_id
        try:
            teste = nfe_service.get_nfes(user_id, user_document_value_id)

            return JsonResponse(teste, safe=False, status=200)
        except ValueError as err:
            return HttpResponse(err, status=500)
        
class get_nfe(APIView):
    def get(request, nfe_id):
        user_id = request.user_id
        try:
            teste = nfe_service.get_nfe(user_id, nfe_id)

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
        

        

