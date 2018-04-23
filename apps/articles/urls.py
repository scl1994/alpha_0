from django.conf.urls import url

from .views import ArticleDetailView, ArticleAllView


urlpatterns = [
    url(r"^detail/(?P<article_id>\d+)/$", ArticleDetailView.as_view(), name='article_detail'),
    url(r"^all/$", ArticleAllView.as_view(), name='articles_list')
]