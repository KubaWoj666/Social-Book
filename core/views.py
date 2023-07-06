from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Post, Profile
from .forms import CreatePostForm, CreateProfile


from django.contrib.auth.models import User


from allauth.account.views import SignupView

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
    user = User.objects.get(username=pk)
    print(user)
    profile = Profile.objects.get(user=user.id)
    context = {
        "profile": profile
    }
    return render(request, "core/profile.html", context)

# def create_post(request):
#     return render(request, "core/create_post.html")


def account_view(request):
    user = request.user
    if request.method == "POST":
        form = CreateProfile(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect("profile", pk=user.username)
    else:
        form = CreateProfile()
    
    context = {
        "user": user,
        "form": form
    }
    return render(request, "core/account.html", context)
    

def settings_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == "POST":
        form = CreateProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile", pk=user.username)
    else:
        form = CreateProfile(instance=profile)
    
    context = {
        "form":form
    }

    return render(request, "core/settings.html", context)


    
