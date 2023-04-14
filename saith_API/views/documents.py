from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from ..services import document_service


class documents(APIView):
    def get(self, request):
        user_id = request.user_id
        try:
            document_list = document_service.get_documents(user_id)
            
            return JsonResponse(document_list, safe=False, status=200)
        except ValueError as err:
            return HttpResponse(status=500)
