from django.shortcuts import render
from django.views.generic import View

from .models import Articles


class ArticleDetailView(View):
    def get(self, request, article_id):
        article = Articles.objects.get(id=article_id)
        tags = article.tags.all()
        return render(request, 'article.html', {"article": article, "tags": tags})
