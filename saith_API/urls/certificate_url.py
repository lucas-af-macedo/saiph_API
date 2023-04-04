from django.urls import path
from ..views import certificate
from rest_framework.decorators import api_view

urlpatterns = [
    path('certificate/', certificate.insert_certificate.as_view(), name='certificate')
]