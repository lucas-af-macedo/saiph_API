from django.contrib import admin
from django.urls import path
from ..views import oi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oi/', oi.get_oi, name='oi')
]
