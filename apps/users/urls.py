from django.conf.urls import url

from .views import LoginView, RegisterView, ActiveView


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),

    url(r'^register/$', RegisterView.as_view(), name="register"),

    url(r"^active/(?P<token>.*)/$", ActiveView.as_view(), name="user_active"),
]