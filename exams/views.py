from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)
from django.utils.translation import get_language, gettext_lazy as _
from django.utils import timezone
from django.db.models import Q
from exams.models import (
    Exam,
    MultipleChoiceQuestion,
    TrueFalseQuestion,
    EssayQuestion,
    ChoiceAnswer,
    EssayQuestionKeyword,
    TakingExamSession,
)
from exams.forms import (
    ExamForm,
    MultipleChoiceQuestionForm,
    ChoiceAnswerForm,
    TrueFalseQuestionForm,
    EssayQuestionForm,
)
from exams.helpers import format_right_answer_essay
from main.models import NormalUser, Teacher
from main.user_tests import teacher_user_test, normal_user_test
from uuid import UUID
from typing import Literal
from datetime import timedelta
import json


# * ================= Exams =================


@user_passes_test(teacher_user_test, "teacher")
def create_exam(request: HttpRequest) -> HttpResponse:

    if request.method == "POST":
        form = ExamForm(request.POST)
        current_normal_user = NormalUser.objects.get(user=request.user)
        current_teacher = Teacher.objects.get(normal_user=current_normal_user)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.teacher = current_teacher
            instance.save()

            return redirect("teacher")

    form = ExamForm()

    return render(request, "teacher/exams/create_exam.html", {"form": form})


@user_passes_test(teacher_user_test, "teacher")
def edit_exam(request: HttpRequest, exam_id: UUID) -> HttpResponse:

    exam = get_object_or_404(Exam, id=exam_id)
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if exam.teacher != current_teacher or exam.is_active:
        return HttpResponseForbidden("<h1>403<h1/><h1>Forbidden</h1>")

    form = ExamForm(instance=exam)

    if request.method == "POST":

        form = ExamForm(request.POST, instance=exam)

        if form.is_valid():
            form.save()
            return redirect("teacher")

    return render(request, "teacher/exams/edit_exam.html", {"form": form})


@user_passes_test(teacher_user_test, "teacher")
def delete_exam(request: HttpRequest, exam_id: UUID) -> HttpResponse:
    exam = get_object_or_404(Exam, id=exam_id)
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if exam.teacher != current_teacher or exam.is_active:
        return HttpResponseForbidden("<h1>403<h1/><h1>Forbidden</h1>")

    exam.delete()

    return redirect("teacher")


@user_passes_test(teacher_user_test, "teacher")
def finish_exam(request: HttpRequest, exam_id: UUID) -> HttpResponse:
    exam = get_object_or_404(
        Exam.objects.prefetch_related(
            "mcq_questions__choiceanswer_set",
            "true_false_questions",
            "essay_questions__essayquestionkeyword_set",
        ),
        id=exam_id,
    )
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if exam.teacher != current_teacher or exam.is_finish:
        return HttpResponseForbidden("<h1>403<h1/><h1>Forbidden</h1>")

    if request.method == "POST":
        problems = []
        extra_info = {
            "essay": [],
            "no_choices": [],
            "no_enough_choices": [],
            "no_right_choice": [],
        }

        # check number of questions
        if (
            exam.mcq_questions.all().count()
            + exam.true_false_questions.all().count()
            + exam.essay_questions.all().count()
            == 0
        ):
            problems.append("zero questions")
            return render(
                request,
                "teacher/exams/handle_finish_exam_problem.html",
                {"problems": problems},
            )

        # check essay questions
        for question in exam.essay_questions.all():
            if not question.essayquestionkeyword_set.all():
                problems.append("essay keyword")
                extra_info["essay"].append(question)

        # check if there is enough choices and if there is a right choice
        for question in exam.mcq_questions.all():
            if not question.choiceanswer_set.all():
                problems.append("no choices")
                extra_info["no_choices"].append(question)

            if question.choiceanswer_set.all().count() == 1:
                problems.append("no enough choices")
                extra_info["no_enough_choices"].append(question)

            for choice in question.choiceanswer_set.all():
                if choice.is_right:
                    break
            else:
                problems.append("no right choice")
                extra_info["no_right_choice"].append(question)

        # get unique problems
        problems = list(set(problems))

        if problems:
            return render(
                request,
                "teacher/exams/handle_finish_exam_problem.html",
                {"problems": problems, "extra_info": extra_info},
            )
        else:

            exam.is_finish = True
            exam.save()

            exam.mcq_questions.all().update(is_finish=True)
            exam.true_false_questions.all().update(is_finish=True)
            exam.essay_questions.all().update(is_finish=True)

            return redirect("teacher_exams")

    return render(request, "teacher/exams/finish_exam.html", {"exam": exam})


@user_passes_test(teacher_user_test, "teacher")
def exam_details(request: HttpRequest, exam_id: UUID) -> HttpResponse:
    exam = get_object_or_404(
        Exam.objects.prefetch_related(
            "mcq_questions", "true_false_questions", "essay_questions"
        ),
        id=exam_id,
    )
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if exam.teacher != current_teacher:
        return HttpResponseForbidden("<h1>403<h1/><h1>Forbidden</h1>")

    return render(request, "teacher/exams/exam_details.html", {"exam": exam})


@user_passes_test(normal_user_test, "profile")
def take_exam(request: HttpRequest, exam_id: UUID) -> HttpResponse:
    exam = get_object_or_404(
        Exam.objects.prefetch_related(
            "mcq_questions__choiceanswer_set",
            "true_false_questions",
            "essay_questions__essayquestionkeyword_set",
        ),
        id=exam_id,
    )
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.filter(normal_user=current_normal_user).first()

    if (current_teacher == exam.teacher) or (request.user.is_superuser) or (current_normal_user in exam.students.all()):  # type: ignore
        if not exam.is_finish:
            return HttpResponseBadRequest(
                "<h1>400<h1/><h1>This Exam Is Not Finish</h1>"
            )

        if request.method == "POST":
            finish_time = timezone.datetime.now().timestamp()
            start_time = request.POST.get("start-time")

            if start_time is None:
                return HttpResponseBadRequest(
                    "<h1>400<h1/><h1>Start time is required</h1>"
                )

            start = timedelta(seconds=int(float(start_time)))
            end = timedelta(seconds=int(finish_time))
            exam_duration = str(end - start)

            mcq_result = 0
            true_false_result = 0

            mcq_questions_number = 0
            true_false_questions_number = 0

            keywords_number = 0
            matched_keywords_number = 0

            for key, answer in request.POST.items():
                if key == "csrfmiddlewaretoken" or key == "start-time":
                    continue

                question_type = key.split("_")[0]
                question_id = key.split("_")[1]

                if question_type == "mcq":
                    # check if the question is in the exam's questions
                    if question := exam.mcq_questions.filter(id=question_id).first():
                        mcq_questions_number += 1
                        if choice := question.choiceanswer_set.filter(id=answer).first():  # type: ignore
                            if choice.is_right:  # type: ignore
                                mcq_result += 1

                elif question_type == "true-false":
                    # check if the question is in the exam's questions
                    if question := exam.true_false_questions.filter(
                        id=question_id
                    ).first():
                        true_false_questions_number += 1
                        if answer == question.get_right_answer_display():
                            true_false_result += 1

                else:
                    # check if the question is in the exam's questions
                    if question := exam.essay_questions.filter(id=question_id).first():
                        user_answer_list = list(
                            map(lambda x: x.lower(), format_right_answer_essay(answer))
                        )
                        if get_language() == "en":
                            keywords_list = (
                                question.essayquestionkeyword_set.all().values_list(
                                    "content_english", flat=True
                                )
                            )
                            keywords_list = list(
                                map(lambda x: x.lower(), keywords_list)
                            )
                        else:
                            keywords_list = (
                                question.essayquestionkeyword_set.all().values_list(
                                    "content_arabic", flat=True
                                )
                            )
                            keywords_list = list(
                                map(lambda x: x.lower(), keywords_list)
                            )

                        keywords_number += len(keywords_list)

                        for word in user_answer_list:
                            if word in keywords_list:
                                matched_keywords_number += 1
                                keywords_list.remove(word)

            mcq_result /= mcq_questions_number  # get the ratio
            mcq_result *= 100  # get the percent ration

            true_false_result /= true_false_questions_number  # get the ratio
            true_false_result *= 100  # get the percent ration

            essay_result = matched_keywords_number / keywords_number  # get the ratio
            essay_result *= 100  # get the percent ration

            final_result = (mcq_result + true_false_result + essay_result) / 3

            # rounding the pecent ratios
            mcq_result = int(round(mcq_result, 2))
            true_false_result = int(round(true_false_result, 2))
            essay_result = int(round(essay_result, 2))
            final_result = int(round(final_result, 2))

            if current_teacher != exam.teacher and not request.user.is_superuser:  # type: ignore
                TakingExamSession.objects.create(
                    exam=exam,
                    student=current_normal_user,
                    mcq_result=mcq_result,
                    true_false_result=true_false_result,
                    essay_result=essay_result,
                    final_result=final_result,
                    duration=exam_duration,
                )

            return render(
                request,
                "exams/exam_result.html",
                {
                    "exam": exam,
                    "mcq_result": mcq_result,
                    "true_false_result": true_false_result,
                    "essay_result": essay_result,
                    "final_result": final_result,
                    "duration": exam_duration,
                },
            )

        return render(
            request,
            "exams/take_exam.html",
            {"exam": exam, "start_time": timezone.datetime.now().timestamp()},
        )
    else:
        return HttpResponseForbidden("<h1>403<h1/><h1>Forbidden</h1>")


# * ================= Questions =================


@user_passes_test(teacher_user_test, "teacher")
def create_question(
    request: HttpRequest, q_type: Literal["mcq", "true-false", "essay"]
) -> HttpResponse:

    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if q_type == "mcq":
        CurrentForm = MultipleChoiceQuestionForm
    elif q_type == "true-false":
        CurrentForm = TrueFalseQuestionForm
    else:
        CurrentForm = EssayQuestionForm

    if request.method == "POST":
        form = CurrentForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.teacher = current_teacher
            instance.save()

            if q_type == "mcq":
                return redirect("exam_add_mcq_choices", question_id=instance.id)
            elif q_type == "essay":
                return redirect("exam_add_essay_keywords", question_id=instance.id)

    form = CurrentForm()

    return render(
        request, "teacher/exams/create_question.html", {"form": form, "type": q_type}
    )


@user_passes_test(teacher_user_test, "teacher")
def add_questions(
    request: HttpRequest, exam_id: UUID, q_type: Literal["mcq", "true-false", "essay"]
) -> HttpResponse:

    # exam and user data
    exam = get_object_or_404(
        Exam.objects.prefetch_related(
            "mcq_questions", "true_false_questions", "essay_questions"
        ),
        id=exam_id,
    )
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)
    questions_number = (
        exam.mcq_questions.all().count()
        + exam.true_false_questions.all().count()
        + exam.essay_questions.all().count()
    )

    # user validation
    if exam.teacher != current_teacher or exam.is_finish:
        return HttpResponseForbidden("<h1>403<h1/><h1>Forbidden</h1>")

    # setting the form and the determining the question we want to add to
    if q_type == "mcq":
        CurrentForm = MultipleChoiceQuestionForm
        exam_questions = exam.mcq_questions
    elif q_type == "true-false":
        CurrentForm = TrueFalseQuestionForm
        exam_questions = exam.true_false_questions
    else:
        CurrentForm = EssayQuestionForm
        exam_questions = exam.essay_questions

    # common form logic
    if request.method == "POST":

        form = CurrentForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.teacher = current_teacher
            instance.save()

            exam_questions.add(instance)

            if q_type == "mcq":
                return redirect("exam_add_mcq_choices", question_id=instance.id)
            elif q_type == "essay":
                return redirect("exam_add_essay_keywords", question_id=instance.id)

    form = CurrentForm()

    return render(
        request,
        "teacher/exams/add_questions.html",
        {
            "exam": exam,
            "questions_number": questions_number,
            "form": form,
            "type": q_type,
        },
    )


@user_passes_test(teacher_user_test, "teacher")
def add_questions_created_before(request: HttpRequest, exam_id: UUID) -> HttpResponse:
    exam = get_object_or_404(
        Exam.objects.prefetch_related(
            "mcq_questions", "true_false_questions", "essay_questions"
        ),
        id=exam_id,
    )
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)
    questions_number = (
        exam.mcq_questions.all().count()
        + exam.true_false_questions.all().count()
        + exam.essay_questions.all().count()
    )

    if exam.teacher != current_teacher or exam.is_finish:
        return HttpResponseForbidden("<h1>403<h1/><h1>Forbidden</h1>")

    if request.method == "POST":
        new_questions = list(request.POST)[1:]

        mcq_adding_questions = []
        true_false_adding_questions = []
        essay_adding_questions = []

        for question in new_questions:
            if question.split("_")[0] == "mcq":
                mcq_adding_questions.append(question.split("_")[1])
            elif question.split("_")[0] == "true-false":
                true_false_adding_questions.append(question.split("_")[1])
            else:
                essay_adding_questions.append(question.split("_")[1])

        exam.mcq_questions.add(*mcq_adding_questions)
        exam.true_false_questions.add(*true_false_adding_questions)
        exam.essay_questions.add(*essay_adding_questions)

    before_mcq_questions_ids = [
        question["id"] for question in exam.mcq_questions.all().values("id")
    ]
    before_true_false_questions_ids = [
        question["id"] for question in exam.true_false_questions.all().values("id")
    ]
    before_essay_questions_ids = [
        question["id"] for question in exam.essay_questions.all().values("id")
    ]

    mcq_questions = MultipleChoiceQuestion.objects.filter(
        ~Q(id__in=before_mcq_questions_ids), teacher=current_teacher  # ~ <==> not
    )

    true_false_questions = TrueFalseQuestion.objects.filter(
        ~Q(id__in=before_true_false_questions_ids),  # ~ <==> not
        teacher=current_teacher,
    )

    essay_questions = EssayQuestion.objects.filter(
        ~Q(id__in=before_essay_questions_ids), teacher=current_teacher  # ~ <==> not
    )

    return render(
        request,
        "teacher/exams/add_questions_created_before.html",
        {
            "exam": exam,
            "questions_number": questions_number,
            "mcq_questions": mcq_questions,
            "true_false_questions": true_false_questions,
            "essay_questions": essay_questions,
        },
    )


@user_passes_test(teacher_user_test, "teacher")
def add_mcq_quastion_choices(request: HttpRequest, question_id: UUID) -> HttpResponse:
    question = get_object_or_404(
        MultipleChoiceQuestion.objects.prefetch_related("choiceanswer_set"),
        id=question_id,
    )
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if question.teacher != current_teacher or question.is_finish:
        return HttpResponseForbidden("<h1>403<h1/><h1>Forbidden</h1>")

    form = ChoiceAnswerForm()

    return render(
        request,
        "teacher/exams/add_mcq_choices.html",
        {"form": form, "question": question},
    )


@user_passes_test(teacher_user_test, "teacher")
def add_essay_question_keyword(request: HttpRequest, question_id: UUID) -> HttpResponse:
    question = get_object_or_404(
        EssayQuestion.objects.prefetch_related("essayquestionkeyword_set"),
        id=question_id,
    )
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if question.teacher != current_teacher or question.is_finish:
        return HttpResponseForbidden("<h1>403<h1/><h1>Forbidden</h1>")

    edited_english_list = format_right_answer_essay(question.right_answer_english)
    edited_arabic_list = format_right_answer_essay(question.right_answer_arabic)

    return render(
        request,
        "teacher/exams/add_essay_question_keywords.html",
        {
            "question": question,
            "english_list": list(edited_english_list),
            "arabic_list": list(edited_arabic_list),
        },
    )


@user_passes_test(teacher_user_test, "teacher")
def delete_question(
    request: HttpRequest,
    q_type: Literal["mcq", "true-false", "essay"],
    question_id: UUID,
) -> HttpResponse:
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if q_type == "mcq":
        question = get_object_or_404(MultipleChoiceQuestion, id=question_id)
    elif q_type == "true-false":
        question = get_object_or_404(TrueFalseQuestion, id=question_id)
    else:
        question = get_object_or_404(EssayQuestion, id=question_id)

    if question.teacher != current_teacher or question.is_finish:
        return HttpResponseForbidden("<h1>403<h1/><h1>Forbidden</h1>")

    question.delete()

    return redirect(request.META["HTTP_REFERER"])


@user_passes_test(teacher_user_test, "teacher")
def remove_question_from_exam(
    request: HttpRequest,
    exam_id: UUID,
    q_type: Literal["mcq", "true-false", "essay"],
    question_id: UUID,
) -> HttpResponse:

    exam = get_object_or_404(Exam, id=exam_id)
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if q_type == "mcq":
        question = get_object_or_404(MultipleChoiceQuestion, id=question_id)
        exam_questions = exam.mcq_questions
    elif q_type == "true-false":
        question = get_object_or_404(TrueFalseQuestion, id=question_id)
        exam_questions = exam.true_false_questions
    else:
        question = get_object_or_404(EssayQuestion, id=question_id)
        exam_questions = exam.essay_questions

    if question.teacher != current_teacher or exam.teacher != current_teacher:
        return HttpResponseForbidden("<h1>403<h1/><h1>Forbidden</h1>")

    if question in exam_questions.all():
        exam_questions.remove(question)

    return redirect(request.META["HTTP_REFERER"])


@user_passes_test(teacher_user_test, "teacher")
def edit_question(
    request: HttpRequest,
    q_type: Literal["mcq", "true-false", "essay"],
    question_id: UUID,
) -> HttpResponse:
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if q_type == "mcq":
        question = get_object_or_404(MultipleChoiceQuestion, id=question_id)
        CurrentForm = MultipleChoiceQuestionForm
    elif q_type == "true-false":
        question = get_object_or_404(TrueFalseQuestion, id=question_id)
        CurrentForm = TrueFalseQuestionForm
    else:
        question = get_object_or_404(EssayQuestion, id=question_id)
        CurrentForm = EssayQuestionForm

    if question.teacher != current_teacher or question.is_finish:
        return HttpResponseForbidden("<h1>403<h1/><h1>Forbidden</h1>")

    if request.method == "POST":
        form = CurrentForm(request.POST, instance=question)
        if form.is_valid():
            form.save()

    form = CurrentForm(instance=question)

    return render(
        request,
        "teacher/exams/edit_question.html",
        {
            "form": form,
            "type": q_type,
        },
    )


@user_passes_test(teacher_user_test, "teacher")
def question_details(
    request: HttpRequest,
    q_type: Literal["mcq", "true-false", "essay"],
    question_id: UUID,
) -> HttpResponse:
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if q_type == "mcq":
        question = MultipleChoiceQuestion.objects.prefetch_related(
            "choiceanswer_set"
        ).get(id=question_id)
    elif q_type == "true-false":
        question = TrueFalseQuestion.objects.get(id=question_id)
    else:
        question = EssayQuestion.objects.prefetch_related(
            "essayquestionkeyword_set"
        ).get(id=question_id)

    if question.teacher != current_teacher:
        return HttpResponseForbidden("<h1>403<h1/><h1>Forbidden</h1>")

    return render(
        request,
        "teacher/exams/question_details.html",
        {
            "question": question,
            "type": q_type,
        },
    )


# * ajax views


@user_passes_test(teacher_user_test, "teacher")
def ajax_add_mcq_choice(request: HttpRequest) -> JsonResponse:

    request_data = json.loads(request.body)
    form = ChoiceAnswerForm(request_data)

    # making sure that there is "question_id" in the body of the request
    if request_data.get("question_id") is None:
        return JsonResponse(
            {
                "message": _("question id should be included in the request"),
                "error": "question_id",
            },
            status=400,
        )

    if form.is_valid():
        instance = form.save(commit=False)

        # here I added the question_id manually because of strange behavior where it is not added to the form
        instance.question_id = request_data["question_id"]

        question = get_object_or_404(MultipleChoiceQuestion, id=instance.question_id)
        current_normal_user = NormalUser.objects.get(user=request.user)
        current_teacher = Teacher.objects.get(normal_user=current_normal_user)

        # verify the identity of the user
        if question.teacher != current_teacher or question.is_finish:
            return JsonResponse({"error": "forbidden"}, status=403)

        # here we will make sure that there is no two true choices at the same question

        right_anwser = question.choiceanswer_set.filter(is_right=True)  # type: ignore

        if right_anwser and instance.is_right:
            return JsonResponse(
                {
                    "message": _("There is already a true answer to this question"),
                    "error": "right_repeated",
                },
                status=400,
            )

        # here we will make sure that the choice is unique

        for choice in question.choiceanswer_set.all():  # type: ignore
            if (
                choice.content_english == instance.content_english
                or choice.content_arabic == instance.content_arabic
            ):
                return JsonResponse(
                    {
                        "message": _(
                            "There is already an answer has this content in this question"
                        ),
                        "error": "choice_repeated",
                    },
                    status=400,
                )

        # if everything went correctly then we will save the instance to the database
        instance.save()

        is_english = get_language() == "en"

        return JsonResponse(
            {
                "message": "success",
                "new_choice": {
                    "id": instance.id,
                    "content": instance.content_english
                    if is_english
                    else instance.content_arabic,
                    "is_right": instance.is_right,
                },
            }
        )

    else:
        return JsonResponse(
            {
                "message": _("There is Might Some Thing Wrong"),
                "error": "non-valid_form",
            },
            status=400,
        )


@user_passes_test(teacher_user_test, "teacher")
def ajax_delete_mcq_choice(request: HttpRequest) -> JsonResponse:
    request_data = json.loads(request.body)

    question_id = request_data.get("question_id")
    choice_id = request_data.get("choice_id")

    if (question_id is None) or (choice_id is None):
        return JsonResponse({"state": "error", "message": "Invalid request payload"})

    question = get_object_or_404(MultipleChoiceQuestion, id=question_id)
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if question.teacher != current_teacher or question.is_finish:
        return JsonResponse({"state": "error", "error": "forbidden"}, status=403)

    choice = get_object_or_404(ChoiceAnswer, id=choice_id)
    choice.delete()

    return JsonResponse(
        {
            "state": "success",
            "message": "choice has been deleted successfully",
        },
        status=200,
    )


@user_passes_test(teacher_user_test, "teacher")
def ajax_add_essay_keyword(request: HttpRequest) -> JsonResponse:
    request_data = json.loads(request.body)

    english_keyword = request_data.get("english_keyword")
    arabic_keyword = request_data.get("arabic_keyword")
    english_keyword_index = request_data.get("english_keyword_index")
    arabic_keyword_index = request_data.get("arabic_keyword_index")
    question_id = request_data.get("question_id")

    if (
        (english_keyword is None)
        or (arabic_keyword is None)
        or (english_keyword_index is None)
        or (arabic_keyword_index is None)
        or (question_id is None)
        or int(english_keyword_index) < 0
        or int(arabic_keyword_index) < 0
    ):
        return JsonResponse({"state": "error", "message": "Invalid request payload"})

    english_keyword_index = int(english_keyword_index)
    arabic_keyword_index = int(arabic_keyword_index)

    question = get_object_or_404(EssayQuestion, id=question_id)
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if question.teacher != current_teacher or question.is_finish:
        return JsonResponse({"state": "error", "message": "forbidden"}, status=403)

    # check if there is any repeated data, either index or the content
    for keyword in question.essayquestionkeyword_set.all():  # type: ignore
        if (
            keyword.english_word_index == english_keyword_index
            or keyword.arabic_word_index == arabic_keyword_index
            or keyword.content_english == english_keyword
            or keyword.content_arabic == arabic_keyword
        ):
            return JsonResponse(
                {
                    "state": "error",
                    "message": _("Repeated Keyword Data"),
                },
                status=403,
            )

    new_keyword = EssayQuestionKeyword.objects.create(
        content_english=english_keyword,
        content_arabic=arabic_keyword,
        english_word_index=english_keyword_index,
        arabic_word_index=arabic_keyword_index,
        question_id=question_id,
    )

    new_keyword_data = {
        "id": new_keyword.pk,
        "keyword_english": new_keyword.content_english,
        "keyword_arabic": new_keyword.content_arabic,
    }

    return JsonResponse({"state": "success", "new_keyword_data": new_keyword_data})


@user_passes_test(teacher_user_test, "teacher")
def ajax_delete_essay_keyword(request: HttpRequest) -> JsonResponse:
    request_data = json.loads(request.body)

    question_id = request_data.get("question_id")
    keyword_id = request_data.get("keyword_id")

    if (question_id is None) or (keyword_id is None):
        return JsonResponse({"state": "error", "message": "Invalid request payload"})

    question = get_object_or_404(EssayQuestion, id=question_id)
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if question.teacher != current_teacher or question.is_finish:
        return JsonResponse({"state": "error", "error": "forbidden"}, status=403)

    # ? here I used "int" with keyword_id because the id in EssayQuestionKeyword model is an integer number
    keyword = get_object_or_404(EssayQuestionKeyword, id=int(keyword_id))
    keyword.delete()

    return JsonResponse({"state": "success"})
