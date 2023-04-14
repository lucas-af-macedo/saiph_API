from django.urls import include, path
from .user_url import urlpatterns as user_urlpatterns
from .certificate_url import urlpatterns as certificate_urlpatterns
from .tests import urlpatterns as tests_urlpatterns
from .documents_url import urlpatterns as documents_urlpatterns
from .events_url import urlpatterns as events_urlpatterns
from .nfe_url import urlpatterns as nfe_urlpatterns

urlpatterns = [
    path('', include(user_urlpatterns)),
    path('auth/', include(certificate_urlpatterns)),
    path('auth/', include(tests_urlpatterns)),
    path('auth', include(documents_urlpatterns)),
    path('auth/', include(events_urlpatterns)),
    path('auth/', include(nfe_urlpatterns)),
]