from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from django.conf.global_settings import AUTH_USER_MODEL
from phonenumber_field.modelfields import PhoneNumberField
import uuid



class GenderChoices(models.IntegerChoices):
    MALE = 1, _("male")
    FAMALE = 2, _("famale")


class NormalUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gender = models.IntegerField(choices=GenderChoices.choices, verbose_name=_("gender"))
    nationality = models.CharField(max_length=127, verbose_name=_("nationality"))
    birthdate = models.DateField(verbose_name=_("birthdate"))
    phone_number = PhoneNumberField()
    user = models.OneToOneField(AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    class Meta:
        verbose_name = _("normal user")
        verbose_name_plural = _("normal users")


class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gender = models.IntegerField(choices=GenderChoices.choices, verbose_name=_("gender"))
    nationality = models.CharField(max_length=127, verbose_name=_("nationality"))
    birthdate = models.DateField(verbose_name=_("birthdate"))
    phone_number = PhoneNumberField()
    bio = models.TextField(validators=[MinLengthValidator(1300)], verbose_name=_("bio"))
    cv = models.FileField(verbose_name=_("CV"), upload_to="teachers_cvs", null=True, blank=True)
    certificate = models.FileField(verbose_name=_("certificate"), upload_to="teachers_certificates", null=True, blank=True)
    is_active = models.BooleanField(verbose_name=_("is active"), default=False)
    normal_user = models.OneToOneField(NormalUser, verbose_name=_("normal user"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("teacher")
        verbose_name_plural = _("teachers")


class Constants(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=127, unique=True)
    content_arabic = models.TextField(verbose_name=_("content arabic"))
    content_english = models.TextField(verbose_name=_("content english"))

    class Meta:
        verbose_name = _("constant")
        verbose_name_plural = _("constants")
