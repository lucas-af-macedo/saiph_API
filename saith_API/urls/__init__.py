from django.urls import include, path
from .user_url import urlpatterns as user_urlpatterns
from .certificate_url import urlpatterns as certificate_urlpatterns

urlpatterns = [
    path('', include(user_urlpatterns)),
    path('', include(certificate_urlpatterns)),
]