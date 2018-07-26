import hashlib
from urllib import parse

from django.conf import settings


def generate_avatar_hash(email):
    """根据邮箱生成Gravatar全球头像的哈希值"""
    return hashlib.md5(bytes(email.lower(), "utf8")).hexdigest()


def get_gravatar_url(user, size=50):
    if user:
        return "https://www.gravatar.com/avatar/{0}?{1}".format(user.avatar_hash, parse.urlencode(
            {"d": settings.DEFAULT_GRAVATAR_STYLE, 's': str(size)}))
    return "https://www.gravatar.com/avatar/{0}?{1}".format("0", parse.urlencode(
        {"d": settings.DEFAULT_GRAVATAR_STYLE, 's': str(size)}))
