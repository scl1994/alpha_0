"""alpha_0 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.conf import settings

from users.views import IndexView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),

    # 关闭debug模式之后，django不再自动代理静态文件，需要手动为其配置服务
    url(r'static/(?P<path>.*)$', serve, {"document_root": settings.STATIC_ROOT}),

    url(r'^articles/', include('articles.urls', namespace='articles')),

    url(r'^account/', include("users.urls", namespace="account")),

    url(r'^sources/', include("sources.urls", namespace="sources")),

    url(r'^$', IndexView.as_view(), name="index"),

    url(r'^operations/', include("user_operations.urls", namespace="operations")),
]


# 全局404页面及500页面配置
handler404 = "user_operations.view.page_not_found"
handler500 = "user_operations.views.server_error"
