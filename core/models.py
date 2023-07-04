from django.db import models
from django.contrib.auth import get_user_model

import uuid


User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_image", default="avatar.svg")
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.user.username



class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post_image")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created= models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user


class Followers(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self) -> str:
        return self.follower