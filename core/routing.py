from django.urls import path
from . import consumers


core_websocket_urlpatterns = [
    path("ws/notifications/", consumers.NotificationConsumer.as_asgi()),
    path("ws/like-notification/", consumers.LikeNotificationConsumer.as_asgi()),
]