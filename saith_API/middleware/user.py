from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from ..serializers import user_serializer
from rest_framework.exceptions import ValidationError
import json

class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/sign-in/':
            try:
                data = JSONParser().parse(request)
                allowed_fields = set(['email', 'password'])
                received_fields = set(data.keys())
                invalid_fields = received_fields - allowed_fields
                if invalid_fields:
                    raise ValidationError(f'Campos inválidos: {invalid_fields}')
                serializer = user_serializer.UserSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                request.data_user = data
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        response = self.get_response(request)
        # Código que será executado depois da view
        return response

class SignUpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/sign-up/':
            try:
                data = JSONParser().parse(request)
                allowed_fields = set(['name', 'email', 'password', 'confirmPassword'])
                received_fields = set(data.keys())
                invalid_fields = received_fields - allowed_fields
                if invalid_fields:
                    raise ValidationError(f'Campos inválidos: {invalid_fields}')
                serializer = user_serializer.SignUpSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                request.data_user = data
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        response = self.get_response(request)
        return response
    
