from django import forms
from django.utils.translation import gettext_lazy as _
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from main.models import NormalUser




class SendingEmailForm(forms.Form):

    subject = forms.CharField(
        label=_("Subject"),
        widget=forms.TextInput()
    )

    message = forms.CharField(
        label=_("Message"),
        widget=forms.Textarea()
    )

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


class CreateNormalUserForm(forms.ModelForm):

    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(
        country_attrs={"class": "phone_number_select"},
        number_attrs={"class": "phone_number_input", "pattern": r"[-\d]+"}
        ),
    )

    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = NormalUser
        fields = ["gender", "nationality", "birthdate", "phone_number", "personal_image"]