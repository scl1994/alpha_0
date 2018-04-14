from django.conf.urls import url
from .views import ArticleDetailView


urlpatterns = [
    url(r"^detail/(?P<article_id>\d+)/$", ArticleDetailView.as_view(), name='article_detail'),
]