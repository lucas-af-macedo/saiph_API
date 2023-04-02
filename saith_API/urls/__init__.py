from django.urls import include, path
from .user_url import urlpatterns as user_urlpatterns

urlpatterns = [
    path('', include(user_urlpatterns))
]