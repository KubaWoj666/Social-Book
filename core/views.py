from django.shortcuts import render, redirect

from .models import Post
from .forms import CreatePostForm


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home_view(request):
    posts = Post.objects.all().order_by("-created")
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("home")
    else:
        form = CreatePostForm

    context = {
        "posts": posts,
        "form": form
    }
    return render(request, "core/home.html", context)


def profile(request):
    user = request.users
    context = {
        "uesr": user
    }
    return render(request, "core/profile.html")

# def create_post(request):
#     return render(request, "core/create_post.html")