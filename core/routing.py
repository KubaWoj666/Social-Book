from django.urls import path
from . import consumers


core_websocket_urlpatterns = [
    path("ws/notification/", consumers.LikeNotificationConsumer.as_asgi()),
]