from django import forms
from django.core.exceptions import ValidationError


class AddCommentForm(forms.Form):
    object_id = forms.IntegerField(required=True)
    comment_type = forms.IntegerField(required=True)
    content = forms.CharField(required=True, min_length=5, max_length=500)


class FavouriteAndLikeForm(forms.Form):
    object_id = forms.IntegerField(required=True)
    object_type = forms.CharField(required=True)
    request_type = forms.CharField(required=True)

    def clean_object_type(self):
        object_type = self.cleaned_data.get("object_type")
        if object_type == "article":
            return 1
        elif object_type == "source":
            return 2
        elif object_type == "comment":
            return 3
        else:
            raise ValidationError("非法的数据类型，无法收藏或者点赞")

    def clean_request_type(self):
        request_type = self.cleaned_data.get("request_type")
        if request_type in ("favourite", "like"):
            return request_type
        else:
            raise ValidationError("非法的操作类型，无法收藏或者点赞")