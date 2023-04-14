from django.urls import path
from ..views import documents

urlpatterns = [
    path('documents/', documents.documents.as_view(), name='documents')
]