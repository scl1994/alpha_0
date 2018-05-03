from django import forms
from django.core.exceptions import ValidationError

from users.models import UserProfile


class LoginForm(forms.Form):
    user_email = forms.EmailField(required=True)
    password = forms.CharField(required=True, max_length=16, min_length=6)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password_1 = forms.CharField(required=True, max_length=16, min_length=6, error_messages={"required": "邮箱为必填字段"})
    password_2 = forms.CharField(required=True, max_length=16, min_length=6, error_messages={"required": "邮箱为必填字段"})

    def clean_username(self):
        # 对username的扩展验证，查找用户是否已经存在
        username = self.cleaned_data.get('username')
        users = UserProfile.objects.filter(username=username).count()
        if users:
            raise ValidationError('用户已经存在！')
        return username

    def clean_email(self):
        # 对email的扩展验证，查找用户是否已经存在
        email = self.cleaned_data.get('email')
        email_count = UserProfile.objects.filter(email=email).count()  # 从数据库中查找是否用户已经存在
        if email_count:
            raise ValidationError('该邮箱已经注册！')
        return email

    def clean_password_2(self):
        password_1 = self.cleaned_data.get("password_1")
        password_2 = self.cleaned_data.get("password_2")
        if password_1 and password_2:
            if password_1 != password_2:
                raise ValidationError("两次密码不相同")
            return password_2


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)

    def clean_email(self):
        # 对email的扩展验证，查找用户是否已经存在
        email = self.cleaned_data.get('email')
        email_count = UserProfile.objects.filter(email=email).count()  # 从数据库中查找是否用户已经存在
        if email_count == 0:
            raise ValidationError('邮箱尚未注册！')
        return email


class ChangePwdForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={"required": "邮箱为必须字段(请通过邮箱验证后再修改密码)"})
    password_1 = forms.CharField(required=True, max_length=16, min_length=6)
    password_2 = forms.CharField(required=True, max_length=16, min_length=6)

    def clean_email(self):
        # 对email的扩展验证，查找用户是否已经存在
        email = self.cleaned_data.get('email')
        email_count = UserProfile.objects.filter(email=email).count()  # 从数据库中查找是否用户已经存在
        if email_count == 0:
            raise ValidationError('邮箱尚未注册！')
        return email

    def clean_password_2(self):
        password_1 = self.cleaned_data.get("password_1")
        password_2 = self.cleaned_data.get("password_2")
        if password_1 and password_2:
            if password_1 != password_2:
                raise ValidationError("两次密码不相同")
            return password_2


class AvatarUploadForm(forms.ModelForm):
    def clean_user_avatar(self):
        avatar = self.cleaned_data.get("user_avatar")
        file_size = avatar.size

        # 文件等格式有ImageField进行验证，这里只是检验文件的大小
        if file_size > 1024 * 1024:
            raise ValidationError("图片大小必须小于1M")
        else:
            return avatar

    class Meta:
        model = UserProfile
        fields = ["user_avatar"]
