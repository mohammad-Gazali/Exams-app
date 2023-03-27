from django import forms
from exams.models import Exam


class CreateExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        exclude = [
            "teacher",
            "students",
            "mcq_questions",
            "true_false_questions",
            "essay_questions",
            "is_active"
        ]