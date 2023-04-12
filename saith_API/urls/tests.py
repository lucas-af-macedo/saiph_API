from django.urls import path
from ..views import test
from rest_framework.decorators import api_view

urlpatterns = [
    path('test/', test.test.as_view(), name='test')
]