from django import forms


class LoginForm(forms.Form):
    user_email = forms.CharField(required=True)
    password = forms.CharField(required=True, max_length=16, min_length=6)