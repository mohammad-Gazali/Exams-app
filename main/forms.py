from django import forms
from django.utils.translation import gettext_lazy as _
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox



attrs = {"class": "login-field"}


class SendingEmailForm(forms.Form):

    subject = forms.CharField(
        label=_("Subject"),
        widget=forms.TextInput(attrs=attrs)
    )

    message = forms.CharField(
        label=_("Message"),
        widget=forms.Textarea(attrs=attrs)
    )

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())