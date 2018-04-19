from django.conf.urls import url

from .views import LoginView, RegisterView, ActiveView, ForgetPasswordView, ForgetVerifyView, ChangePwdView


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),

    url(r'^register/$', RegisterView.as_view(), name="register"),

    url(r"^active/(?P<token>.*)/$", ActiveView.as_view(), name="user_active"),

    url(r"^forget_pwd/$", ForgetPasswordView.as_view(), name="forget_pwd"),

    url(r"^forget_verify/(?P<token>.*)/$", ForgetVerifyView.as_view(), name="forget_verify"),

    url(r"^change_pwd/$", ChangePwdView.as_view(), name="change_pwd"),
]