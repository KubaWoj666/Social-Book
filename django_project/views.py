from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from core.models import Profile
from allauth.account.views import SignupView

class CustomSignupView(SignupView):
    def form_invalid(self, form) -> HttpResponse:
        user = self.request.user
        super().form_invalid(form)

        profile = Profile.objects.create(user=user, location="warszawa")
        profile.save()

        return HttpResponse(status=200)