"""发送邮箱"""
from threading import Thread

from django.core.mail import send_mail
from django.template import loader
from django.conf import settings
from django.shortcuts import reverse


class EmailMessage:
    def __init__(self, user, token, send_type):
        self.user = user
        self.send_type = send_type
        self.token = token
        self.success = True

    def send(self):
        thread = Thread(target=self._send, args=[])
        thread.start()

    def _send(self):
        if self.send_type == "confirm":
            email_title = "Alpha-用户激活邮箱验证"
            html_content = loader.render_to_string("email/confirm.html", {
                "username": self.user.username,
                "confirm_url": settings.DOMAIN + reverse("account:user_confirm", kwargs={"token": self.token}),
                "reconfirm_url": settings.DOMAIN + reverse("account:user_reconfirm"),
            })
            text_content = loader.render_to_string("email/confirm.txt", {
                "username": self.user.username,
                "confirm_url": settings.DOMAIN + reverse("account:user_confirm", kwargs={"token": self.token}),
                "reconfirm_url": settings.DOMAIN + reverse("account:user_reconfirm"),
            })
            send_mail(subject=email_title, message=text_content, html_message=html_content,
                      from_email=settings.EMAIL_FROM, recipient_list=[self.user.email])
        elif self.send_type == "forget_pwd":
            email_title = "Alpha-重置密码邮箱验证"
            html_content = loader.render_to_string("email/forget_pwd.html", {
                "username": self.user.username,
                "verify_url": settings.DOMAIN + reverse("account:forget_verify", kwargs={"token": self.token}),
                "forget_url": settings.DOMAIN + reverse("account:forget_pwd"),
            })
            text_content = loader.render_to_string("email/forget_pwd.txt", {
                "username": self.user.username,
                "verify_url": settings.DOMAIN + reverse("account:forget_verify", kwargs={"token": self.token}),
                "forget_url": settings.DOMAIN + reverse("account:forget_pwd"),
            })
            send_mail(subject=email_title, message=text_content, html_message=html_content,
                      from_email=settings.EMAIL_FROM, recipient_list=[self.user.email])
