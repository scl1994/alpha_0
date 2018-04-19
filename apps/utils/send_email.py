"""发送邮箱"""

from django.core.mail import send_mail

from alpha_0.settings import EMAIL_FROM


def send_email(email, token, send_type="register"):
    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "Alpha--用户邮箱激活"
        email_body = "请点击以下链接激活你的邮箱（有效时间2小时）：http://127.0.0.1:8000/account/active/{0}".format(token)
        send_status = send_mail(subject=email_title, message=email_body, from_email=EMAIL_FROM, recipient_list=[email])
        if send_status:
            pass
    elif send_type == "forget_pwd":
        email_title = "Alpha--修改密码邮箱验证"
        email_body = "请点击以下链接验证你的邮箱（有效时间1小时）：http://127.0.0.1:8000/account/forget_verify/{0}".format(token)
        send_status = send_mail(subject=email_title, message=email_body, from_email=EMAIL_FROM, recipient_list=[email])
        if send_status:
            pass