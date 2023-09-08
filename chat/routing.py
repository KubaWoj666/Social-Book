from django.urls import path
from .customers import ChatConsumer

websocket_urlpatterns = [
    path("ws/<int:id>/", ChatConsumer.as_asgi())
]