from django.shortcuts import render, redirect

from .models import Post, Profile
from .forms import CreatePostForm


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home_view(request):
    page = "home"
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
        "form": form,
        "page": page
    }
    return render(request, "core/home.html", context)


def profile(request, pk):
    profile = Profile.objects.get(user_id=pk)
    context = {
        "profile": profile
    }
    return render(request, "core/profile.html", context)

# def create_post(request):
#     return render(request, "core/create_post.html")


def account_view(request, pk):
    user = User.objects.get(id=pk)

    context={
        "user": user
    }

    return render(request, "core/account.html", context)