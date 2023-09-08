from django.urls import path
from . import views


urlpatterns = [
    path("<str:username>/", views.chat, name='main_chat')
]