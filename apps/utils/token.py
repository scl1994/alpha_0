import base64

from itsdangerous import TimedJSONWebSignatureSerializer as JsonSerializer
from itsdangerous import BadData
from django.conf import settings


class Token:
    def __init__(self, expires_in=7200, security_key=settings.SECRET_KEY):
        self.salt = base64.b64encode(bytes(security_key, encoding="utf-8"))
        self.serializer = JsonSerializer(security_key, expires_in=expires_in)

    def generate_token(self, data):
        return str(self.serializer.dumps(data, self.salt), encoding="utf8")

    def confirm_token(self, token):
        """确认token是否合法，是否在有效期之内"""
        token = bytes(token, "utf8")
        res = {"data": None, "success": False, "error": None}
        try:
            res["data"] = self.serializer.loads(token, salt=self.salt)
            res["success"] = True
        except BadData as e:
            res["error"] = e
        return res


default_token = Token()
