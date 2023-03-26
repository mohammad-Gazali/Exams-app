from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox



class LoginCustomForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput()
    )

    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput()
    )

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


class SignUpCustomForm(UserCreationForm):
    first_name = forms.CharField(
        label=_('First Name'),
        widget= forms.TextInput(),
        required=False
    )

    last_name = forms.CharField(
        label=_('Last Name'),
        widget= forms.TextInput(),
        required=False
    )

    username = forms.CharField(
        label=_('Username'),
        widget= forms.TextInput()
    )

    email = forms.EmailField(
        label=_('Email'),
        widget= forms.TextInput(),
    )

    password1 = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput()
    )
    
    password2 = forms.CharField(
        label=_('Password Confirmation'),
        strip=False,
        widget=forms.PasswordInput()
    )

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta(UserCreationForm.Meta):
        fields = ['first_name', 'last_name', 'username', 'email']