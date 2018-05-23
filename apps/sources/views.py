from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .models import Sources
from user_operations.models import UserLike, UserFavourite, Comments


class SourcesDetailView(View):
    def get(self, request, source_id):
        has_favourite = False
        has_like = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, object_id=source_id, favourite_type=2):
                has_favourite = True
            if UserLike.objects.filter(user=request.user, object_id=source_id, like_type=2):
                has_like = True
        source = get_object_or_404(Sources, id=source_id)

        source.click_number += 1
        source.save()

        comments_list = Comments.objects.filter(object_id=source_id, comment_type=2).order_by("-add_time")

        hot_sources = Sources.objects.all().order_by("-click_number")[:5]
        recent_sources = Sources.objects.all().order_by("-add_time")[:5]
        return render(request, "source.html", {"source": source, "has_favourite": has_favourite, "has_like": has_like,
                                               "comments_list": comments_list, "hot_sources": hot_sources,
                                               "recent_sources": recent_sources})


class SourcesAllView(View):
    def get(self, request):
        sources_list = Sources.objects.all()
        hot_sources = Sources.objects.all().order_by("-click_number")[:5]
        recent_sources = Sources.objects.all().order_by("-add_time")[:5]
        return render(request, "source-list.html", {"sources_list": sources_list, "hot_sources": hot_sources,
                                                    "recent_sources": recent_sources})