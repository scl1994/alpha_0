from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password

from .models import UserProfile
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ChangePwdForm
from utils.send_email import send_email
from utils.token import token_confirm


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
                if user.is_activated:
                    login(request, user)
                    return render(request, "index.html", {})
                else:
                    return render(request, "login.html", {"message": "邮箱尚未激活，进检查邮件，进入对应链接进行激活"})
            else:
                return render(request, "login.html", {"message": "邮箱或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html", {})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = request.POST.get("email", "")
            username = request.POST.get("username", "")
            password = request.POST.get("password_1", "")
            # 将用户保存到数据库
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = user_email
            user_profile.password = make_password(password)
            user_profile.save()

            email_token = token_confirm.generate_validate_token(user_email)
            send_email(email=user_email, token=email_token, send_type="register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class ActiveView(View):
    def get(self, request, token):
        try:
            email = token_confirm.confirm_validate_token(token)
        except:
            try:
                email = token_confirm.remove_validate_token(token)
                user = UserProfile.objects.get(email=email)
                if user.is_activated:
                    return render(request, "login.html")
                else:
                    user.delete()
                    return render(request, "register.html", {"message": "激活信息已过期，请重新注册"})
            except:
                return render(request, "register.html", {"message": "激活信息有误，请重新注册"})
        try:
            user = UserProfile.objects.get(email=email)
        except:
            return render(request, "register.html", {"message": "激活用户不存在，请重新注册"})
        user.is_activated = True
        user.save()
        return render(request, "login.html")


class ForgetPasswordView(View):
    def get(self, request):
        return render(request, "forget-pwd.html")

    def post(self, request):
        forget_pwd_form = ForgetPwdForm(request.POST)
        if forget_pwd_form.is_valid():
            email = request.POST.get("email", "")

            email_token = token_confirm.generate_validate_token(email)
            send_email(email=email, token=email_token, send_type="forget_pwd")
            return render(request, "send-success.html")
        return render(request, "forget-pwd.html", {"forget_pwd_form": forget_pwd_form})


class ForgetVerifyView(View):
    def get(self, request, token):
        try:
            email = token_confirm.confirm_validate_token(token, expiration=3600)
        except:
            return render(request, "forget-pwd.html", {"message": "邮箱验证信息有误或者已过期，请重新验证"})
        return render(request, "change-pwd.html", {"user_email": email})


class ChangePwdView(View):
    def get(self, request):
        return render(request, "change-pwd.html")

    def post(self, request):
        change_pwd_form = ChangePwdForm(request.POST)
        if change_pwd_form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password_1")
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "change-pwd.html", {"change_pwd_form": change_pwd_form, "user_email": email})