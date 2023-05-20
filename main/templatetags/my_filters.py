from django.template import Library
from django.utils.translation import get_language
from exams.helpers import format_right_answer_essay
from exams.models import EssayQuestionKeyword
from django.db.models import QuerySet


register = Library()
current_langauge = get_language()


@register.filter("get_attr_lang")
def get_attr_lang(obj, attr: str):
    if current_langauge == "en":
        return getattr(obj, f"{attr}_english")
    else:
        return getattr(obj, f"{attr}_arabic")


@register.filter("get_result_colors")
def get_result_colors(num: int):
    number_one = "--progress-color: var(--secondary); --progress-color-light: var(--secondary-low-opacity)"
    number_two = "--progress-color: var(--primary-main); --progress-color-light: var(--primary-light-low-opacity)"
    number_three = "--progress-color: #ffc107; --progress-color-light: #ffe69c"
    number_four = "--progress-color: var(--danger-main); --progress-color-light: var(--danger-light)"
    if num > 90:
        return number_one
    elif num > 70:
        return number_two
    elif num > 40:
        return number_three
    else:
        return number_four


@register.filter("get_keywords")
def get_keywords(queryset: QuerySet[EssayQuestionKeyword]):
    # ? the huge number of queries in exam_result view solved here where I used normal list comprehension instead of values_list(..., flat=True) method
    if get_language() == "en":
        return [q.content_english for q in queryset]
    else:
        return [q.content_arabic for q in queryset]


register.filter("format_right_answer_essay", format_right_answer_essay)
