from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from ..serializers import user_serializer
import json

class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/sign-in/':
            try:
                data = JSONParser().parse(request)
                serializer = user_serializer.UserSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                request.data_user = data
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        response = self.get_response(request)
        # Código que será executado depois da view
        return response