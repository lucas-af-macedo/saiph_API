from django.urls import include, path
from .oi import urlpatterns as oi_urlpatterns
from .user import urlpatterns as user_urlpatterns

urlpatterns = [
    path('', include(oi_urlpatterns)),
    path('', include(user_urlpatterns))
]