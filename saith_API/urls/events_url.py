from django.urls import path
from ..views import events

urlpatterns = [
    path('events/<int:event_id>/', events.get_events.as_view(), name='events'),
    path('event/<int:event_id>/NFe/<int:nfe_id>/', events.post_nfe_event.as_view(), name='get_full_nfe'),
]