from django.conf.urls import url

from .views import LoginView, LogoutView, RegisterView, ActiveView, ForgetPasswordView, ForgetVerifyView, ChangePwdView, \
    UserCenterInformationView, AvatarUploadView, ArticleFavouriteListView, SourceFavouriteListView


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),

    url(r'^logout/$', LogoutView.as_view(), name="logout"),

    url(r'^register/$', RegisterView.as_view(), name="register"),

    url(r"^active/(?P<token>.*)/$", ActiveView.as_view(), name="user_active"),

    url(r"^forget_pwd/$", ForgetPasswordView.as_view(), name="forget_pwd"),

    url(r"^forget_verify/(?P<token>.*)/$", ForgetVerifyView.as_view(), name="forget_verify"),

    url(r"^change_pwd/$", ChangePwdView.as_view(), name="change_pwd"),

    url(r"^center/information/$", UserCenterInformationView.as_view(), name="user_information"),

    url(r"^center/articles/$", ArticleFavouriteListView.as_view(), name="favourite_articles"),

    url(r"^center/sources/$", SourceFavouriteListView.as_view(), name="favourite_sources"),

    url(r"^avatar_upload/$", AvatarUploadView.as_view(), name="avatar_upload")
]