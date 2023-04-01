from django.http import JsonResponse

def get_oi(request):
    a = {"response": "oi"}
    print(a)
    return JsonResponse(a, status=200)