from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from main.models import Teacher, NormalUser
import uuid






class MultipleChoiceQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_english = RichTextField(verbose_name=_("question english"))
    question_arabic = RichTextField(verbose_name=_("question arabic"))
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name=_("teacher"), null=True, blank=True)
    cause_english = RichTextField(verbose_name=_("cause english"))
    cause_arabic = RichTextField(verbose_name=_("cause arabic"))

    class Meta:
        verbose_name = "MCQ"
        verbose_name_plural = "MCQs"


class ChoiceAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_english = models.CharField(max_length=255, verbose_name=_("content english"))
    content_arabic = models.CharField(max_length=255, verbose_name=_("content arabic"))
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE, verbose_name=_("question"))
    is_right = models.BooleanField(default=False, verbose_name=_("is it right"))

    class Meta:
        verbose_name = _("choice")
        verbose_name_plural = _("choices")


class TrueFlaseAnswers(models.TextChoices):
    TRUE = "T", _("True")
    FALSE = "F", _("False")


class TrueFalseQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_english = RichTextField(verbose_name=_("question english"))
    question_arabic = RichTextField(verbose_name=_("question arabic"))
    right_answer = models.CharField(max_length=1, choices=TrueFlaseAnswers.choices, verbose_name=_("right answer"))
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name=_("teacher"), null=True, blank=True)
    cause_english = RichTextField(verbose_name=_("cause english"))
    cause_arabic = RichTextField(verbose_name=_("cause arabic"))


class EssayQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_english = RichTextField(verbose_name=_("question english"))
    question_arabic = RichTextField(verbose_name=_("question arabic"))
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name=_("teacher"), null=True, blank=True)
    right_answer_english = RichTextField(verbose_name=_("right answer english"))
    right_answer_arabic = RichTextField(verbose_name=_("right answer arabic"))

    class Meta:
        verbose_name = _("essay question")
        verbose_name_plural = _("essay questions")


class EssayQuestoionKeyword(models.Model):
    content_english = models.CharField(max_length=255, verbose_name=_("content english"))
    content_arabic = models.CharField(max_length=255, verbose_name=_("content arabic"))
    question = models.ForeignKey(EssayQuestion, on_delete=models.CASCADE, verbose_name=_("question"))

    class Meta:
        verbose_name = _("essay question keyword")
        verbose_name_plural = _("essay question keywords")


class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_english = models.CharField(max_length=511, verbose_name=_("name english"))
    name_arabic = models.CharField(max_length=511, verbose_name=_("name arabic"))
    description_english = models.TextField(verbose_name=_("description english"), null=True)
    description_arabic = models.TextField(verbose_name=_("description arabic"), null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name=_("teacher"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("price"))  # type: ignore
    is_demo = models.BooleanField(default=False, verbose_name=_("is demo"))
    is_active = models.BooleanField(default=False, verbose_name=_("is active"))
    students = models.ManyToManyField(NormalUser, verbose_name=_("students"))
    mcq_questions = models.ManyToManyField(MultipleChoiceQuestion, verbose_name=_("MCQ questions"))
    true_false_questions = models.ManyToManyField(TrueFalseQuestion, verbose_name=_("true-false questions"))
    essay_questions = models.ManyToManyField(EssayQuestion, verbose_name=_("essay questions"))

    class Meta:
        verbose_name = _("exam")
        verbose_name_plural = _("exams")


class ExamsGroup(models.Model):
    name_english = models.CharField(max_length=511, verbose_name=_("name english"))
    name_arabic = models.CharField(max_length=511, verbose_name=_("name arabic"))
    exams = models.ManyToManyField(Exam, verbose_name=_("exams"))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_("price"))  # type: ignore
    is_active = models.BooleanField(default=False, verbose_name=_("is active"))
    students = models.ManyToManyField(NormalUser, verbose_name=_("students"))

    class Meta:
        verbose_name = _("exams group")
        verbose_name_plural = _("exams groups")