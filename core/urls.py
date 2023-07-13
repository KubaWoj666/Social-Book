from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("profile/<str:pk>", views.profile, name="profile"),
    # path("create-post", views.create_post, name="create-post"),
    path("account", views.account_view, name="account"),
    path("settings", views.settings_view, name="settings"),
    # path("follow", views.follow_view, name="follow"),



    
]