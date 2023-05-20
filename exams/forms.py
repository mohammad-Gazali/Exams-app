from django import forms
from django.utils.translation import gettext_lazy as _
from exams.models import (
    Exam,
    MultipleChoiceQuestion,
    ChoiceAnswer,
    TrueFalseQuestion,
    EssayQuestion,
)


class ExamForm(forms.ModelForm):

    is_demo = forms.CharField(
        widget=forms.CheckboxInput(attrs={"class": "checkbox"}), required=False
    )

    price = forms.CharField(label=_("Price In Dollars $"))

    class Meta:
        model = Exam
        exclude = [
            "teacher",
            "students",
            "mcq_questions",
            "true_false_questions",
            "essay_questions",
            "is_active",
            "is_finish",
        ]


class MultipleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceQuestion
        exclude = ["teacher", "is_finish"]


class ChoiceAnswerForm(forms.ModelForm):
    class Meta:
        model = ChoiceAnswer
        exclude = ["question"]


class TrueFalseQuestionForm(forms.ModelForm):
    class Meta:
        model = TrueFalseQuestion
        exclude = ["teacher", "is_finish"]


class EssayQuestionForm(forms.ModelForm):
    class Meta:
        model = EssayQuestion
        exclude = ["teacher", "is_finish"]
