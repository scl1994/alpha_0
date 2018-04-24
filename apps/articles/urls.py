from django.conf.urls import url

from .views import ArticleDetailView, ArticleAllView, SeriesAllView, SeriesDetailView, SpecialAllView, \
    SpecialDetailView


urlpatterns = [
    url(r"^detail/(?P<article_id>\d+)/$", ArticleDetailView.as_view(), name='article_detail'),

    url(r"^all/$", ArticleAllView.as_view(), name='articles_list'),

    url(r"^series/$", SeriesAllView.as_view(), name='series_list'),

    url(r"^series/(?P<series_id>\d+)/$", SeriesDetailView.as_view(), name='series_detail'),

    url(r"^special/$", SpecialAllView.as_view(), name='special_list'),

    url(r"^special/(?P<special_id>\d+)/$", SpecialDetailView.as_view(), name='special_detail'),
]