import random
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Prefetch

from .models import Post, Profile, Followers, Likes, Comment
from .forms import CreatePostForm, CreateProfile
from django.contrib.auth.models import User

from django_htmx.http import HttpResponseClientRefresh, HttpResponseClientRedirect

# Create your views here.

@login_required(login_url="account_login")
def home_view(request):
    page = "home"
    posts = Post.objects.all().order_by("-created")
    profile = Profile.objects.get(user=request.user)
    
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
        try:
            post = Post.objects.get(id=request.POST.get("post_id"))
            
            if Likes.objects.filter(post=post, user=user, liked=True).exists():
                unlike = Likes.objects.get(user=user, post=post, liked=True)
                unlike.delete()
                return HttpResponseClientRefresh()
            else:
                like = Likes.objects.create(user=user, post=post, liked=True)
                like.save()
                return HttpResponseClientRefresh()
        except:
            return redirect("home")
    
    user = request.user
    request_user_liked_post = [post.id for post in posts if Likes.objects.filter(post=post, user=user, liked=True).exists()] 
            
    user_following = Followers.objects.filter(follower=user).values_list('following__id', flat=True)

    user_suggestions = Profile.objects.exclude(user=user.id).exclude(user__in=user_following)
    
    try:
        user_suggestions = random.sample(list(user_suggestions), 3)
    except:
        user_suggestions = user_suggestions

    post_comments = {}
    for post in posts:
        comments = Comment.objects.filter(post=post)
        post_comments[post.id] = comments
    
   
    context = {
        "posts": posts,
        "form": form,
        "page": page,
        "profile": profile,
        "request_user_liked_post": request_user_liked_post,
        "user_suggestions": user_suggestions,
        "post_comments": post_comments 
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
        "form":form,
        "profile": profile
    }
    return render(request, "core/settings.html", context)

@login_required(login_url="account_login")
def follow_suggestions(request):
    user = request.user
    if request.method == "POST":
        follow_suggestion_username = request.POST.get("follow_suggestion_username")
        print(follow_suggestion_username)
        user_to_follow = User.objects.get(username=follow_suggestion_username)
        follow = Followers.objects.create(follower=user, following=user_to_follow)
        follow.save()
        return HttpResponseClientRefresh()

    return render(request, "core/partials/follow_suggestions.html")

@login_required(login_url="account_login")
def post_detail(request, pk):
    user = request.user
    post = get_object_or_404(Post, id=pk)
    profile = get_object_or_404(Profile, user=user)

    likes = Likes.objects.filter(post=post, liked=True)
    
    is_post_liked = Likes.objects.filter(user=user, post=post, liked=True).exists

    comments = post.comment_set.filter(post=post)

    context={
        "post":post,
        "is_post_liked":is_post_liked,
        "likes": likes,
        "comments": comments,
        "profile":profile
    }

    return render(request, "core/post_detail.html", context)


@login_required(login_url="account_login")
def update_post(request, pk):
    post = Post.objects.get(id=pk)

    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("home")
    
    else:
        form = CreatePostForm(instance=post)
    
    context = {
        "post": post,
        "form": form
    }

    return render(request, "core/update-post.html", context )

@login_required(login_url="account_login")
def delete_post(request, pk):
    user = request.user
    post = get_object_or_404(Post, id=pk, user=user)
    next_url = request.GET.get("next")

    post.delete()
    
    if next_url:
        return HttpResponseClientRedirect(next_url)
    
    return HttpResponseClientRefresh()
    

@login_required(login_url="account_login")
def comment(request):
    user = request.user
    next_url = request.GET.get("next")
   
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id=post_id)
        body = request.POST.get("body")
        comment = Comment.objects.create(owner=user, post=post, body=body)
        comment.save()
        if next_url:
            return redirect(next_url)
        
    return render(request, "core/home.html")
   
@login_required(login_url="account_login")
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    comment.delete()
    return HttpResponseClientRefresh()