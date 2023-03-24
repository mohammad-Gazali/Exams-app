from django.db import models
from django.utils.translation import gettext_lazy as _
from main.models import Teacher, NormalUser
import uuid



# class Option(models.Model):

#     class Meta:
#         verbose_name = _("Question")
#         verbose_name_plural = _("Questions") 

# class Question(models.Model):
#     class Meta:
#         verbose_name = _("Question")
#         verbose_name_plural = _("Questions")


# class EssayQuestion(models.Model):
#     class Meta:
#         verbose_name = _("Essay Question")
#         verbose_name_plural = _("Essay Questions")


class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name=_("teacher"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    price = models.IntegerField(verbose_name=_("price"))
    is_demo = models.BooleanField(default=False, verbose_name=_("is demo"))
    is_active = models.BooleanField(default=False, verbose_name=_("is active"))
    students = models.ManyToManyField(NormalUser, verbose_name=_("students"))

    class Meta:
        verbose_name = _("exam")
        verbose_name_plural = _("exams")