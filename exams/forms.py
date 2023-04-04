from django import forms
from exams.models import Exam, MultipleChoiceQuestion, ChoiceAnswer



class CreateExamForm(forms.ModelForm):

    is_demo = forms.CharField(
        widget=forms.CheckboxInput(attrs={"class": "checkbox"}),
        required=False
    )

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


class UpdateExamForm(forms.ModelForm):

    is_demo = forms.CharField(
        widget=forms.CheckboxInput(attrs={"class": "checkbox"}),
        required=False
    )

    is_finish = forms.CharField(
        widget=forms.CheckboxInput(attrs={"class": "checkbox"}),
        required=False
    )

    class Meta:
        model = Exam
        exclude = [
            "teacher",
            "students",
            "mcq_questions",
            "true_false_questions",
            "essay_questions",
            "is_active",
        ]


class CreateMultipleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceQuestion
        exclude = ["teacher"]


class CreateChoiceAnswerForm(forms.ModelForm):
    class Meta:
        model = ChoiceAnswer
        exclude = ["question"]