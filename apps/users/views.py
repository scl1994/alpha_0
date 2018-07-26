from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import UserProfile
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ChangePwdForm
from sources.models import Sources
from articles.models import Articles
from utils.send_email import send_email
from utils.token import token_confirm
from user_operations.models import UserFavourite


class CustomBackends(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(email=username)
            if user.check_password(password):
                return user
            else:
                return None
        except Exception:
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
                    # 注意这里由于首页需要各种数据，如果直接render跳转的首页，页面将缺少各种信息
                    #  所以应该使用重定向，让处理index的view来处理这个跳转
                    next_url = request.POST.get("next", "") \
                        if request.POST.get("next", "") is not "" else reverse("index")
                    return HttpResponseRedirect(next_url)
                else:
                    return render(request, "login.html", {"message": "邮箱尚未激活，进检查邮件，进入对应链接进行激活"})
            else:
                return render(request, "login.html", {"message": "邮箱或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


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
            return render(request, "login.html", {})
        else:
            return render(request, "register.html", {"register_form": register_form})


class ActiveView(View):
    def get(self, request, token):
        try:
            email = token_confirm.confirm_validate_token(token)
        except Exception:
            try:
                email = token_confirm.remove_validate_token(token)
                user = UserProfile.objects.get(email=email)
                if user.is_activated:
                    return render(request, "login.html", {})
                else:
                    user.delete()
                    return render(request, "register.html", {"message": "激活信息已过期，请重新注册"})
            except Exception:
                return render(request, "register.html", {"message": "激活信息有误，请重新注册"})
        try:
            user = UserProfile.objects.get(email=email)
        except Exception:
            return render(request, "register.html", {"message": "激活用户不存在，请重新注册"})
        user.is_activated = True
        user.save()
        return render(request, "login.html", {})


class ForgetPasswordView(View):
    def get(self, request):
        return render(request, "forget-pwd.html", {})

    def post(self, request):
        forget_pwd_form = ForgetPwdForm(request.POST)
        if forget_pwd_form.is_valid():
            email = request.POST.get("email", "")

            email_token = token_confirm.generate_validate_token(email)
            send_email(email=email, token=email_token, send_type="forget_pwd")
            return render(request, "send-success.html", {})
        return render(request, "forget-pwd.html", {"forget_pwd_form": forget_pwd_form})


class ForgetVerifyView(View):
    def get(self, request, token):
        try:
            email = token_confirm.confirm_validate_token(token, expiration=3600)
        except:
            return render(request, "forget-pwd.html", {"message": "邮箱验证信息有误或者已过期，请重新验证"})
        return render(request, "change-pwd.html", {"user_email": email})


class ChangePwdView(View):
    def post(self, request):
        change_pwd_form = ChangePwdForm(request.POST)
        if change_pwd_form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password_1")
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            return render(request, "login.html", {})
        else:
            email = request.POST.get("email", "")
            return render(request, "change-pwd.html", {"change_pwd_form": change_pwd_form, "user_email": email})


class IndexView(View):
    def get(self, request):
        hot_sources = Sources.objects.all().order_by("-click_number")[:4]
        recent_sources = Sources.objects.all().order_by("-add_time")[:5]
        recent_articles = Articles.objects.all().order_by("-add_time")[:15]
        hot_articles = Articles.objects.all().order_by("-click_number")[:5]

        return render(request, "index.html", {"hot_sources": hot_sources, "recent_sources": recent_sources,
                                              "recent_articles": recent_articles, "hot_articles": hot_articles})


class UserCenterInformationView(LoginRequiredMixin, View):
    # 如果没登录重定向到登录地址
    login_url = '/account/login'

    def get(self, request):
        return render(request, "user-information.html", {})


class ArticleFavouriteListView(LoginRequiredMixin, View):
    login_url = '/account/login'

    def get(self, request):
        favourite_articles_ids = UserFavourite.objects.filter(user=request.user, favourite_type=1)
        favourite_articles = [
            Articles.objects.filter(id=x.object_id).first() for x in favourite_articles_ids
        ]

        return render(request, "user-favourite-article.html", {"favourite_articles": favourite_articles})


class SourceFavouriteListView(LoginRequiredMixin, View):
    login_url = '/account/login'

    def get(self, request):
        favourite_sources_ids = UserFavourite.objects.filter(user=request.user, favourite_type=2)
        favourite_sources = [
            Sources.objects.filter(id=x.object_id).first() for x in favourite_sources_ids
        ]

        return render(request, "user-favourite-source.html", {"favourite_sources": favourite_sources})

