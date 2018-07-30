import json

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import UserProfile
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ChangePwdForm, ReconfirmForm
from sources.models import Sources
from articles.models import Articles
from utils.send_email import EmailMessage
from utils.token import default_token, Token
from user_operations.models import UserFavourite


class CustomBackends(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(email=username)
            if user.check_password(password):
                return user
            else:
                return None
        except ObjectDoesNotExist:
            # 没有找到或者找到多个
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
                if user.confirmed:
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

            token = default_token.generate_token({"email": user_email, "token_type": "confirm"})

            message = EmailMessage(user=user_profile, token=token, send_type="confirm")
            message.send()

            return redirect("account:login")
        else:
            return render(request, "register.html", {"register_form": register_form})


class ConfirmView(View):
    def get(self, request, token):
        validate_result = default_token.confirm_token(token)
        if validate_result["success"]:
            data = validate_result["data"]
            if data["token_type"] == "confirm":
                try:
                    user = UserProfile.objects.get(email=data.get("email"))
                except ObjectDoesNotExist:
                    return redirect("account:register")
                if not user.confirmed:
                    user.confirmed = True
                    user.save()
                return redirect("account:login")
            else:
                # token类型不对，重新请求
                return redirect("account:user_reconfirm")
        else:
            # token解析失败
            return redirect("account:user_reconfirm")


class ReconfirmView(View):
    def get(self, request):
        return render(request, "reconfirm.html", {})

    def post(self, request):
        reconfirm_form = ReconfirmForm(request.POST)
        if reconfirm_form.is_valid():

            email = reconfirm_form.cleaned_data["email"]
            user = UserProfile.objects.get(email=email)
            if not user.confirmed:
                token = default_token.generate_token({"email": email, "token_type": "confirm"})

                message = EmailMessage(user=user, token=token, send_type="confirm")
                message.send()
                return_msg = "已向{}用户发送激活邮件，邮件有效时间为两小时，请注意查收。".format(email)
                return HttpResponse(json.dumps({'status': "success", "message": return_msg}),
                                    content_type="application/json")
            else:
                return HttpResponse(json.dumps({'status': "is_confirmed"}),
                                    content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status': "error_email"}),
                                content_type="application/json")


class ForgetPasswordView(View):
    def get(self, request):
        return render(request, "forget-pwd.html", {})

    def post(self, request):
        forget_pwd_form = ForgetPwdForm(request.POST)
        if forget_pwd_form.is_valid():
            email = forget_pwd_form.cleaned_data.get("email")
            user = UserProfile.objects.get(email=email)

            token_generator = Token(expires_in=1800)
            token = token_generator.generate_token({"email": email, "token_type": "forget_pwd"})

            message = EmailMessage(user=user, token=token, send_type="forget_pwd")
            message.send()
            return_msg = "已向{}用户发送验证邮件，邮件有效时间为0.5小时，请注意查收。".format(email)
            return HttpResponse(json.dumps({'status': "success", "message": return_msg}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status': "error_email"}),
                                content_type="application/json")


class ForgetVerifyView(View):
    def get(self, request, token):
        validate_result = default_token.confirm_token(token)
        if validate_result["success"]:
            data = validate_result["data"]
            if data["token_type"] == "forget_pwd":
                try:
                    UserProfile.objects.get(email=data.get("email"))
                except ObjectDoesNotExist:
                    return redirect("account:register")
                return render(request, "change-pwd.html", {"user_email": data["email"]})
            else:
                # token类型不对，重新请求
                return redirect("account:forget_pwd")
        else:
            # token解析失败
            return redirect("account:forget_pwd")


class ChangePwdView(View):
    def post(self, request):
        change_pwd_form = ChangePwdForm(request.POST)
        if change_pwd_form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password_1")
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            return HttpResponse(json.dumps({'status': "success"}), content_type="application/json")
        else:
            return_msg = "请确保两次密码相同并且长度不小于6位"
            return HttpResponse(json.dumps({'status': "fail", "message": return_msg}),
                                content_type="application/json")


class IndexView(View):
    def get(self, request):
        hot_sources = Sources.objects.all().order_by("-click_number")[:4]
        recent_sources = Sources.objects.all().order_by("-add_time")[:5]
        recent_articles = Articles.objects.all().order_by("-add_time")[:15]
        hot_articles = Articles.objects.all().order_by("-click_number")[:5]

        return render(request, "index.html", {"hot_sources": hot_sources, "recent_sources": recent_sources,
                                              "recent_articles": recent_articles, "hot_articles": hot_articles})


class UserCenterInformationView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "user-information.html", {})


class ArticleFavouriteListView(LoginRequiredMixin, View):
    def get(self, request):
        favourite_articles_ids = UserFavourite.objects.filter(user=request.user, favourite_type=1)
        favourite_articles = [Articles.objects.filter(id=x.object_id).first() for x in favourite_articles_ids]

        return render(request, "user-favourite-article.html", {"favourite_articles": favourite_articles})


class SourceFavouriteListView(LoginRequiredMixin, View):
    def get(self, request):
        favourite_sources_ids = UserFavourite.objects.filter(user=request.user, favourite_type=2)
        favourite_sources = [Sources.objects.filter(id=x.object_id).first() for x in favourite_sources_ids]

        return render(request, "user-favourite-source.html", {"favourite_sources": favourite_sources})

