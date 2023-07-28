from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("profile/<str:pk>", views.profile, name="profile"),
    # path("create-post", views.create_post, name="create-post"),
    path("account", views.account_view, name="account"),
    path("settings", views.settings_view, name="settings"),
    path("comment", views.comment, name="comment"),

    path("follow-suggestions", views.follow_suggestions, name="follow-suggestions"),
    path("post/<uuid:pk>", views.post_detail, name="post-detail"),
    # path("follow", views.follow_view, name="follow"),



    
]