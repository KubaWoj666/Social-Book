from django.shortcuts import render


from core.models import User, Profile

# Create your views here.

def chat(request, username):
    user = request.user
    request_user_profile = Profile.objects.get(user=user)

    user_obj = Profile.objects.get(user__username = username)

    users = Profile.objects.exclude(user=user)

    context = {
        "request_user": user,
        "request_user_profile": request_user_profile,
        "user_obj": user_obj,
        "users": users

    }

    return render(request, "chat/main_chat.html", context)