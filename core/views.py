from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Post, Profile, Followers, Likes
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
        form = CreatePostForm()
    
    if request.htmx:
        user = request.user
        post = Post.objects.get(id=request.POST.get("post_id"))
        
        if Likes.objects.filter(post=post, user=user, liked=True).exists():
            unlike = Likes.objects.get(user=user, post=post, liked=True)
            unlike.delete()
            return HttpResponseClientRefresh()
        else:
            like = Likes.objects.create(user=user, post=post, liked=True)
            like.save()
            return HttpResponseClientRefresh()
    
    user = request.user
    request_user_liked_posts = [post.id for post in posts if Likes.objects.filter(post=post, user=user, liked=True).exists()] 
    
    # liked_posts = Post.objects.filter(likes__liked=True)
    
    
    print(count_like)
        
    likes_by_meetup = {meetup.slug: meetup.like_set.filter(meetup=meetup, liked=True).count() for meetup in meetups }
    context = {
        "posts": posts,
        "form": form,
        "page": page,
        "request_user_liked_posts": request_user_liked_posts,
        # "liked_posts": liked_posts
    }
    return render(request, "core/home.html", context)

@login_required(login_url="account_login")
def profile(request, pk):
    user = User.objects.get(username=pk)
    profile = Profile.objects.get(user=user.id)
    posts = Post.objects.filter(user=user)
    followers = Followers.objects.filter(following=user)
    follow = Followers.objects.filter(follower=user)
    
    is_following = False

    if request.method == "POST":
        follower = User.objects.get(username=request.POST.get("user"))
        user_to_follow = request.POST.get("user_to_follow")
        following = User.objects.get(username=user_to_follow)
        if Followers.objects.filter(follower=follower, following=following).exists():
            unfollow = Followers.objects.get(follower=follower, following=following)
            unfollow.delete()
            return redirect("profile", pk=user_to_follow)
        else:
            nwe_follow = Followers.objects.create(follower=follower, following=following)
            nwe_follow.save()
            return redirect("profile", pk=user_to_follow)
    
    
    follower = request.user
    if Followers.objects.filter(follower=follower, following=user).exists():
        is_following = True

    context = {
        "profile": profile,
        "posts" : posts,
        "followers":followers,
        "follow":follow,
        "is_following": is_following
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


    
# def follow_view(request):
#     user = request.user
#     follower_exist = False
    
#     if request.method == "POST":
#         user = user
#         user_to_follow = request.POST["user_to_follow"]
#         following = User.objects.get(username=user_to_follow)
#         if Followers.objects.filter(follower=user, following=following).exists():
#             followers = Followers.objects.get(follower=user, following=following)
#             followers.delete()
#         else:
#             followers = Followers.objects.create(follower=user, following=following)
#             followers.save()
#             follower_exist = True
    
#     context={
#         "follower_exist": follower_exist
#     }
    
#     return redirect("profile", pk=user_to_follow)