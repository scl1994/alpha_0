from django.conf.urls import url

from .views import AddCommentView, FavouriteAndLikeView


urlpatterns = [
    url(r"^add_comment/$", AddCommentView.as_view(), name='add_comment'),

    url(r"^favourite_like/$", FavouriteAndLikeView.as_view(), name='favourite_like'),

]