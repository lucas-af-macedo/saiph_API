from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView

class get_events(APIView):
    def get(request):
        data_user = request.body
        try:
            return HttpResponse(status=501)
        except ValueError as err:
            return HttpResponse(status=500)

class post_nfe_event(APIView):
    def post(self, request, event_id, nfe_id):
        try:
            print(event_id)
            print(nfe_id)
            return HttpResponse(status=501)
        except ValueError as err:
            return HttpResponse(status=500)