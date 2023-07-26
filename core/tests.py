from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.urls import reverse
from django.utils import timezone

from .models import Profile, Post, Likes, Followers
from .forms import CreatePostForm, CreateProfile

import datetime


class SocialAppTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="test", email="test@email", password="testpassword")
        cls.user2 = get_user_model().objects.create_user(username="test2", email="test2@email", password="testpassword")

        cls.post = Post.objects.create(user=cls.user, image="image", title="test title", description="test description")

        cls.profile = Profile.objects.create(user=cls.user, image="image", bio="test bio", location="test location")

        cls.likes = Likes.objects.create(user=cls.user, post=cls.post, liked=True)

        cls.followers = Followers.objects.create(follower=cls.user, following=cls.user2)

    def test_post_model(self):
        post = Post.objects.first()
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post.title, "test title")
        self.assertEqual(post.description, "test description")
        self.assertEqual(post.user, self.user)
        self.assertAlmostEqual(post.created, timezone.now(), delta=datetime.timedelta(seconds=1))
        self.assertEqual(post.image.field.upload_to, "post_image")
    

    def test_profile_model(self):
        profile = Profile.objects.first()
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(profile.bio, "test bio")
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.location, "test location")
        self.assertEqual(profile.image.field.upload_to, "profile_image")

    def test_like_model(self):
        like = Likes.objects.first()
        self.assertEqual(Likes.objects.count(), 1)
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.post, self.post)
        self.assertEqual(like.liked, True)

    
    def test_follower_model(self):
        follower = Followers.objects.first()
        self.assertEqual(Followers.objects.count(), 1)
        self.assertEqual(follower.follower, self.user)
        self.assertEqual(follower.following, self.user2)



    def test_home_view(self):
        self.client.login(username="test", password="testpassword")
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post)
        self.assertTemplateUsed(response, "core/home.html")
        self.assertEqual(response.context["request_user_liked_post"], [self.post.id])
        self.assertIsInstance(response.context["form"], CreatePostForm)

    
        form_data = {
            "user":self.user.pk,
            "image": "new image",
            "title": "new post",
            "description": "new description"
        }

        response = self.client.post(url, data=form_data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "new post")
        self.assertEqual(Post.objects.count(), 1)
        self.assertTemplateUsed(response, "core/home.html")


    def test_profile_view(self):
        self.client.login(username="test", password="testpassword")
        url = reverse("profile", args=[self.user.username])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/profile.html")
        self.assertContains(response, self.user.username)
    
    def test_profile_view_not_authenticated(self):
        url = reverse("profile", args=[self.user.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    
    def test_account_view(self):
        self.client.login(username="test", password="testpassword")
        url = reverse("account")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/account.html")
        self.assertIsInstance(response.context["form"], CreateProfile)

        form_data = {
            "user": self.user.id,
            "bio": "test bio",
            "image": "image",
            "location": "test location"
        }

        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)

        response = self.client.post(url, {"post_id": self.post.id}, HTTP_HX=True)
        self.assertEqual(response.status_code, 200)

       
    
    def test_settings_view(self):
        self.client.login(username="test", password="testpassword")
        profile = Profile.objects.get(user=self.user)
        url = reverse("settings")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], CreateProfile)
        self.assertTemplateUsed(response, "core/settings.html")
        self.assertContains(response, "test bio")

        form_data = {
            "image":"updated_image",
            "bio": "updated bio",
            "location": "updated location"
        }

        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 302)
        
    
    def test_post_detail_view(self):
        self.client.login(username="test", password="testpassword")
        url = reverse("post-detail", args=[self.post.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/post_detail.html")
        self.assertContains(response, self.post)