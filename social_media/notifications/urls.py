from django.urls import path
from .views import get_notifications
from .views import mark_notifications_as_read

urlpatterns = [
    path('', get_notifications, name='notifications-list'),

    path('mark-as-read/', mark_notifications_as_read, name='mark-notifications-as-read'),
]