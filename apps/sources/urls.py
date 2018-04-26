from django.conf.urls import url

from .views import SourcesDetailView, SourcesAllView

urlpatterns = [
    url(r"^detail/(?P<source_id>\d+)/$", SourcesDetailView.as_view(), name='source_detail'),

    url(r"^all/$", SourcesAllView.as_view(), name='sources_list'),
]