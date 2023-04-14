from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView


class documents(APIView):
    def get(request):
        data_user = request.body
        try:
            return HttpResponse(status=501)
        except ValueError as err:
            return HttpResponse(status=500)
