from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

# Custom class to redirect after signup user
class MyAccountAdapter(DefaultAccountAdapter):
    def get_signup_redirect_url(self, request):
        path = "/account"
        return path