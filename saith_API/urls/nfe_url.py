from django.urls import path
from ..views import nfe

urlpatterns = [
    path('NFes/<int:user_document_value_id>/', nfe.get_nfes.as_view(), name='get_nfes'),
    path('NFe/<int:nfe_id>/', nfe.get_nfe.as_view(), name='get_nfe'),
    path('fullNFe/<int:nfe_id>/', nfe.get_full_nfe.as_view(), name='get_full_nfe'),
]