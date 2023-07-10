from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Post, Profile, Followers
from .forms import CreatePostForm, CreateProfile

from django.contrib.auth.models import User

from allauth.account.views import SignupView
from django_htmx.http import HttpResponseClientRefresh

# Create your views here.

@login_required(login_url="account_login")
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

@login_required(login_url="account_login")
def profile(request, pk):
    user = User.objects.get(username=pk)
    profile = Profile.objects.get(user=user.id)
    posts = Post.objects.filter(user=user)
    followers = Followers.objects.filter(following=user)
    follow = Followers.objects.filter(follower=user)
    context = {
        "profile": profile,
        "posts" : posts,
        "followers":followers,
        "follow":follow
    }
    return render(request, "core/profile.html", context)


@login_required(login_url="account_login")
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
    
@login_required(login_url="account_login")
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


    
def follow_view(request):
    user = request.user
    follower_exist = False
    
    if request.method == "POST":
        user = user
        user_to_follow = request.POST["user_to_follow"]
        following = User.objects.get(username=user_to_follow)
        if Followers.objects.filter(follower=user, following=following).exists():
            followers = Followers.objects.get(follower=user, following=following)
            followers.delete()
        else:
            followers = Followers.objects.create(follower=user, following=following)
            followers.save()
            follower_exist = True
    
    context={
        "follower_exist": follower_exist
    }
    
    return redirect("profile", pk=user_to_follow)