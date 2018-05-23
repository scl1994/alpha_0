from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .models import Articles, Series, SpecialColumn
from user_operations.models import Comments, UserFavourite, UserLike


class ArticleDetailView(View):
    def get(self, request, article_id):
        has_favourite = False
        has_like = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, object_id=article_id, favourite_type=1):
                has_favourite = True
            if UserLike.objects.filter(user=request.user, object_id=article_id, like_type=1):
                has_like = True
        article = get_object_or_404(Articles, id=article_id)

        # 点击量增加一
        article.click_number += 1
        article.save()

        tags = article.tags.all()
        hot_articles = Articles.objects.all().order_by("-click_number")[:5]
        recent_articles = Articles.objects.all().order_by("-add_time")[:5]
        comments_list = Comments.objects.filter(comment_type=1, object_id=article_id).order_by("-add_time")
        return render(request, 'article.html', {"article": article, "tags": tags, "comments_list": comments_list,
                                                "has_favourite": has_favourite, "has_like": has_like,
                                                "hot_articles": hot_articles, "recent_articles": recent_articles})


class ArticleAllView(View):
    def get(self, request):
        articles_list = Articles.objects.all().order_by("-add_time")
        recent_articles = Articles.objects.all().order_by("-add_time")[:5]
        hot_articles = Articles.objects.all().order_by("-click_number")[:5]
        return render(request, 'article-list.html', {"articles_list": articles_list, "hot_articles": hot_articles,
                                                     "recent_articles": recent_articles})


class SeriesAllView(View):
    def get(self, request):
        series = Series.objects.all().order_by("-add_time")
        hot_articles = Articles.objects.all().order_by("-click_number")[:5]
        recent_series = series[:5]
        return render(request, "series-list.html", {"series_list": series, "hot_articles": hot_articles,
                                                    "recent_series_list": recent_series})


class SeriesDetailView(View):
    def get(self, request, series_id):
        series = get_object_or_404(Series, id=series_id)
        articles = series.get_articles().order_by("-add_time")
        hot_articles = Articles.objects.all().order_by("-click_number")[:5]
        recent_articles = Articles.objects.all().order_by("-add_time")[:5]
        return render(request, "article-list.html", {"articles_list": articles, "hot_articles": hot_articles,
                                                     "recent_articles": recent_articles})


class SpecialAllView(View):
    def get(self, request):
        special_list = SpecialColumn.objects.all().order_by("-add_time")
        hot_articles = Articles.objects.all().order_by("-click_number")[:5]
        recent_special_column = special_list[:5]
        return render(request, "special-list.html", {"special_list": special_list, "hot_articles": hot_articles,
                                                     "recent_special_column": recent_special_column})


class SpecialDetailView(View):
    def get(self, request, special_id):
        special = get_object_or_404(SpecialColumn, id=special_id)
        articles = special.get_articles().order_by("-add_time")
        hot_articles = Articles.objects.all().order_by("-click_number")[:5]
        recent_articles = Articles.objects.all().order_by("-add_time")[:5]
        return render(request, "article-list.html", {"articles_list": articles, "hot_articles": hot_articles,
                                                     "recent_articles": recent_articles})
