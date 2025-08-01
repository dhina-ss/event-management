from django.urls import path
from .views import EventAPIView, EventAttendeesAPIView, EventAttendeesRegisterAPIView

urlpatterns = [
    path('events/', EventAPIView.as_view(), name='events-list'),
    path('events/<str:event_id>/register/', EventAttendeesRegisterAPIView.as_view(), name='attendees-register'),
    path('events/<str:event_id>/attendees/', EventAttendeesAPIView.as_view(), name='attendees-list'),
]