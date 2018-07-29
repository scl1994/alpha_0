from django.conf.urls import url

from .views import LoginView, LogoutView, RegisterView, ConfirmView, ForgetPasswordView, ForgetVerifyView, ChangePwdView, \
    UserCenterInformationView, ArticleFavouriteListView, SourceFavouriteListView, ReconfirmView


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),

    url(r'^logout/$', LogoutView.as_view(), name="logout"),

    url(r'^register/$', RegisterView.as_view(), name="register"),

    url(r"^confirm/(?P<token>.*)/$", ConfirmView.as_view(), name="user_confirm"),

    url(r"^reconfirm/$", ReconfirmView.as_view(), name="user_reconfirm"),

    url(r"^forget_pwd/$", ForgetPasswordView.as_view(), name="forget_pwd"),

    url(r"^forget_verify/(?P<token>.*)/$", ForgetVerifyView.as_view(), name="forget_verify"),

    url(r"^change_pwd/$", ChangePwdView.as_view(), name="change_pwd"),

    url(r"^center/information/$", UserCenterInformationView.as_view(), name="user_information"),

    url(r"^center/articles/$", ArticleFavouriteListView.as_view(), name="favourite_articles"),

    url(r"^center/sources/$", SourceFavouriteListView.as_view(), name="favourite_sources"),
]