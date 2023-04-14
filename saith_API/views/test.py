from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from ..services import test_service
from ..middleware.authorization import AuthoizationMiddleware


class test(APIView):
    @AuthoizationMiddleware
    def post(request):
        data_user = request.body
        try:
            test_service.test(data_user)

            return JsonResponse({}, status=200)
        except ValueError as err:
            return HttpResponse(status=500)
