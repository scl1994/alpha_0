from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend

from .models import UserProfile
from .forms import LoginForm


class CustomBackends(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(email=username)
            if user.check_password(password):
                return user
            else:
                return None
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = request.POST.get("user_email", "")
            password = request.POST.get("password", "")
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return render(request, "index.html", {})
            else:
                return render(request, "login.html", {"message": "邮箱或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})
