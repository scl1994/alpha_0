import json

from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.http import HttpResponse

from .forms import AddCommentForm, FavouriteAndLikeForm
from .models import Comments, UserFavourite, UserLike
from users.models import UserProfile


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': "fail", "message": "用户未登录"}),
                                content_type="application/json")
        comment_form = AddCommentForm(request.POST)
        if comment_form.is_valid():
            comment = Comments()
            comment.object_id = comment_form.cleaned_data.get("object_id")
            comment.comment_type = comment_form.cleaned_data.get("comment_type")
            comment.content = comment_form.cleaned_data.get("content")
            comment.user = UserProfile.objects.get(id=request.user.id)
            comment.save()
            return HttpResponse(json.dumps({"status": "success", "content": comment_form.cleaned_data.get("content")}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status': "fail", 'message': "评论长度应为5-500个字符"}),
                                content_type="application/json")


class FavouriteAndLikeView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': "fail", "message": "用户未登录"}),
                                content_type="application/json")
        f_l_form = FavouriteAndLikeForm(request.POST)
        if f_l_form.is_valid():
            object_id = f_l_form.cleaned_data.get("object_id")
            object_type = f_l_form.cleaned_data.get("object_type")
            request_type = f_l_form.cleaned_data.get("request_type")
            if request_type == 'favourite':
                # 判断当前用户是否已经收藏
                is_exist = UserFavourite.objects.filter(user=request.user, object_id=object_id,
                                                        favourite_type=object_type)
                if is_exist:
                    # 已经收藏，就取消收藏
                    is_exist.delete()
                    return HttpResponse(json.dumps({'status': "success-off", "message": "取消收藏成功"}),
                                        content_type="application/json")
                else:
                    # 没有收藏就添加收藏
                    user_favourite = UserFavourite()
                    user_favourite.object_id = object_id
                    user_favourite.favourite_type = object_type
                    user_favourite.user = request.user
                    user_favourite.save()
                    return HttpResponse(json.dumps({'status': "success-on", "message": "收藏成功"}),
                                        content_type="application/json")

            else:
                # 由于已经使用form清洗了数据，所以不是favourite肯定就是like
                # 判断当前用户是否已经点赞
                is_exist = UserLike.objects.filter(user=request.user, object_id=object_id, like_type=object_type)
                if is_exist:
                    # 已经点赞，就取消点赞
                    is_exist.delete()
                    return HttpResponse(json.dumps({'status': "success-off", "message": "取消点赞成功"}),
                                        content_type="application/json")
                else:
                    # 没有点赞就添加点赞
                    user_like = UserLike()
                    user_like.object_id = object_id
                    user_like.like_type = object_type
                    user_like.user = request.user
                    user_like.save()
                    return HttpResponse(json.dumps({'status': "success-on", "message": "点赞成功"}),
                                        content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status': "fail", "message": "用户未登录"}),
                                content_type="application/json")






def page_not_found(request):
    """全局404页面处理函数"""
    response = render_to_response("404.html", {})
    response.status_code = 404
    return response


def server_error(request):
    """全局500页面处理函数"""
    response = render_to_response("500.html", {})
    response.status_code = 500
    return response
