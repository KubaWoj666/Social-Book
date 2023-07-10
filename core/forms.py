from django import forms
from .models import Post, Profile


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["image", "title", "description"]


class CreateProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "bio", "location" ]