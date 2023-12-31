from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from core.models import User, Profile, Followers
from .models import ChatModel

# Create your views here.
@login_required(login_url="account_login")
def chat(request, username):
    user = request.user
    request_user_profile = Profile.objects.get(user=user)

    user_obj = Profile.objects.get(user__username = username)
    

    # users = Profile.objects.exclude(user=user)

    if user.id > user_obj.user.id:
        thread_name = f"chat_{user.id}-{user_obj.user.id}"
    else:
        thread_name = f"chat_{user_obj.user.id}-{user.id}"
    
    messages = ChatModel.objects.filter(thread_name=thread_name)

    user_following = Followers.objects.filter(follower=user).values_list('following__id', flat=True)
    users = Profile.objects.filter(user__in=user_following)


    context = {
        "request_user": user,
        "request_user_profile": request_user_profile,
        "user_obj": user_obj,
        "users": users,
        "messages": messages,
        # "chat_suggestions" :chat_suggestions
    }

    return render(request, "chat/main_chat.html", context)