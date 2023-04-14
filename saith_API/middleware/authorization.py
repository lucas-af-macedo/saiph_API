from django.http import JsonResponse
import jwt
import os

class AuthoizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            data = request.headers.get('Authorization').strip().split(' ')[1].strip()
            secret_key = os.getenv('SECRET_KEY')
            user = jwt.decode(data, secret_key, algorithms=['HS256'], verify=False)
            if user['user_id'] == None:
                raise Exception()
            request.user_id = user['user_id']
        except:
            return JsonResponse({}, status=401)
        response = self.get_response(request)
        return response
    def process_request(self, request):
        if not request.path.startswith('/auth/'):
            return None