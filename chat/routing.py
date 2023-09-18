from django.urls import path
from .customers import ChatConsumer, OnlineStatusConsumer

websocket_urlpatterns = [
    path("ws/<int:id>/", ChatConsumer.as_asgi()),
    path("ws/online/", OnlineStatusConsumer.as_asgi()),
]