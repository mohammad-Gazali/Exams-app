from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


attrs = {"class": "login-field"}


class LoginCustomForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs=attrs)
    )

    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs=attrs)
    )

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


class SignUpCustomForm(UserCreationForm):
    first_name = forms.CharField(
        label=_('First Name'),
        widget= forms.TextInput(attrs=attrs),
        required=False
    )

    last_name = forms.CharField(
        label=_('Last Name'),
        widget= forms.TextInput(attrs=attrs),
        required=False
    )

    username = forms.CharField(
        label=_('Username'),
        widget= forms.TextInput(attrs=attrs)
    )

    email = forms.EmailField(
        label=_('Email'),
        widget= forms.TextInput(attrs=attrs),
    )

    password1 = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs=attrs)
    )
    
    password2 = forms.CharField(
        label=_('Password Confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs=attrs)
    )

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta(UserCreationForm.Meta):
        fields = ['first_name', 'last_name', 'username', 'email']