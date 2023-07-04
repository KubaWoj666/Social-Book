from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Post, Likes, Followers


class AdminProfile(admin.ModelAdmin):
    list_display = ["user"]

admin.site.register(Profile, AdminProfile)

class AdminPosts(admin.ModelAdmin):
    list_display = ["title"]

admin.site.register(Post, AdminPosts)

class AdminLikes(admin.ModelAdmin):
    list_display = ["user", "post", "liked"]

admin.site.register(Likes, AdminLikes)

class AdminFollowers(admin.ModelAdmin):
    list_display = ["follower", "following"]

admin.site.register(Followers, AdminFollowers)