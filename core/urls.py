from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("profile/<int:pk>", views.profile, name="profile"),
    # path("create-post", views.create_post, name="create-post"),
    path("account/<int:pk>", views.account_view, name="account")
]