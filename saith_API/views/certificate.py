from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from ..services import certificate_service

class insert_certificate(APIView):
    def post(self, request):
        uploaded_file = request.FILES['file'].read()
        password = request.POST.get('password')
        try:
            user = certificate_service.insert_certificate(uploaded_file, password)
            
            return HttpResponse(status=201)
        except ValueError as err:
            return HttpResponse(status=500)