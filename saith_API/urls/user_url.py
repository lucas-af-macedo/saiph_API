from django.urls import path
from ..views import user
from rest_framework.decorators import api_view

urlpatterns = [
    path('sign-in/', user.sign_in.as_view(), name='sign_in'),
    path('sign-up/', user.sign_up.as_view(), name='sign_up'),
]
