import hashlib
from urllib import parse
from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()


# 只返回url
# 使用 {{ user|gravatar_url:150 }}
@register.filter
def gravatar_url(user, size=50):
    if user.avatar_hash is None:
        # 如果user对象的avatar_hash为空，调用save(),save中包含了生成avatar_hash的代码
        user.save()
    return "https://www.gravatar.com/avatar/{0}?{1}".format(user.avatar_hash, parse.urlencode(
        {"d": settings.DEFAULT_GRAVATAR_STYLE, 's': str(size)}))


@register.filter
def gravatar(user, size=50):
    if user.avatar_hash is None:
        # 如果user对象的avatar_hash为空，调用save(),save中包含了生成avatar_hash的代码
        user.save()
    url = gravatar_url(user, size)
    return mark_safe('<img src="%s" height="%d" width="%d">' % (url, size, size))