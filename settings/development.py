from .base import *
from .security_dev import *

DEBUG = True

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
# STATIC_ROOT = os.path.join(BASE_DIR, "static")


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# 默认Gravatar头像风格
DEFAULT_GRAVATAR_STYLE = "identicon"


# 分页
PAGINATION_DEFAULT_PAGINATION = 10  # 默认每页个数

PAGINATION_DEFAULT_WINDOW = 2  # 当前页的前后显示的页数

DOMAIN = "http://127.0.0.1:8000"
