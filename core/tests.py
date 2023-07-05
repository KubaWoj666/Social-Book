from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from .models import Profile, Post, Likes, Followers
from .forms import CreatePostForm

import datetime


class SocialAppTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username="test", email="test@email", password="testpassword")

        cls.post = Post.objects.create(user=cls.user, image="image", title="test title", description="test description")

    def test_post_model(self):
        post = Post.objects.first()
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post.title, "test title")
        self.assertEqual(post.description, "test description")
        self.assertEqual(post.user, self.user)
        self.assertAlmostEqual(post.created, timezone.now(), delta=datetime.timedelta(seconds=1))
        self.assertEqual(post.image.field.upload_to, "post_image")


    def test_home_view(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post)
        self.assertTemplateUsed(response, "core/home.html")
        

        form = response.context["form"]
        self.assertTrue(form is CreatePostForm)

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



        

