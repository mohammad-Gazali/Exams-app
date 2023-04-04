from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseForbidden
from django.utils.translation import gettext_lazy as _
from exams.models import Exam, MultipleChoiceQuestion
from exams.forms import CreateExamForm, UpdateExamForm, CreateMultipleChoiceQuestionForm, CreateChoiceAnswerForm
from main.models import NormalUser, Teacher
from main.user_tests import teacher_user_test
from uuid import UUID
import json



@user_passes_test(teacher_user_test, "teacher")
def create_exam(request: HttpRequest) -> HttpResponse:
    form = CreateExamForm()
    if request.method == "POST":
        form = CreateExamForm(request.POST)
        normal_user = NormalUser.objects.get(user=request.user)
        teacher = Teacher.objects.get(normal_user=normal_user)
        if form.is_valid():
            Exam.objects.create(
                name_english=form.cleaned_data["name_english"],
                name_arabic=form.cleaned_data["name_arabic"],
                description_english=form.cleaned_data["description_english"],
                description_arabic=form.cleaned_data["description_arabic"],
                price=form.cleaned_data["price"],
                is_demo=form.cleaned_data["is_demo"],
                teacher=teacher
            )
            return redirect("teacher")
        
    return render(request, "teacher/exams/create_exam.html", {"form": form})


@user_passes_test(teacher_user_test, "teacher")
def edit_exam(request: HttpRequest, exam_id: UUID) -> HttpResponse:
    exam = get_object_or_404(Exam, id=exam_id)
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if exam.teacher == current_teacher:
        form = UpdateExamForm(instance=exam)
        if request.method == "POST":
            form = UpdateExamForm(request.POST, instance=exam)
            if form.is_valid():
                form.save()
                return redirect("teacher")        
        return render(request, "teacher/exams/edit_exam.html", {"form": form})
    
    # not the same teacher case
    return HttpResponseForbidden("<h1>403<h1/><h1>Forbidden</h1>")
    

@user_passes_test(teacher_user_test, "teacher")
def delete_exam(request: HttpRequest, exam_id: UUID) -> HttpResponse:
    exam = get_object_or_404(Exam, id=exam_id)
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if exam.teacher == current_teacher:
        exam.delete()
        return redirect("teacher") 

    # not the same teacher case
    return HttpResponseForbidden("<h1>403<h1/><h1>Forbidden</h1>")


@user_passes_test(teacher_user_test, "teacher")
def add_questions(request: HttpRequest, exam_id: UUID) -> HttpResponse:
    exam = get_object_or_404(
        Exam.objects.prefetch_related(
            "mcq_questions", "true_false_questions", "essay_questions"
        ), 
        id=exam_id
    )
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if exam.teacher == current_teacher:

        mcq_form = CreateMultipleChoiceQuestionForm()

        if request.method == "POST":
            mcq_form = CreateMultipleChoiceQuestionForm(request.POST)
            
            if mcq_form.is_valid():
                instance = mcq_form.save(commit=False)
                instance.teacher = current_teacher
                instance.save()

                print(instance.id)

                exam.mcq_questions.add(instance)

                return redirect("exam_add_mcq_details", question_id=instance.id)

        quastions_number = exam.mcq_questions.all().count() + exam.true_false_questions.all().count() + exam.essay_questions.all().count()

        return render(request, "teacher/exams/add_questions.html", {
                "exam": exam,
                "quastions_number": quastions_number,
                "mcq_form": mcq_form,
            }
        )

    # not the same teacher case
    return HttpResponseForbidden("<h1>403<h1/><h1>Forbidden</h1>")


@user_passes_test(teacher_user_test, "teacher")
def add_mcq_quastion_details(request: HttpRequest, question_id: UUID) -> HttpResponse:
    question = get_object_or_404(MultipleChoiceQuestion, id=question_id)
    current_normal_user = NormalUser.objects.get(user=request.user)
    current_teacher = Teacher.objects.get(normal_user=current_normal_user)

    if question.teacher == current_teacher:

        form = CreateChoiceAnswerForm()

        return render(request, "teacher/exams/add_mcq_choices.html", {
                "form": form,
                "question": question
            }
        )
    
    # not the same teacher case
    return HttpResponseForbidden("<h1>403<h1/><h1>Forbidden</h1>")




# ajax views

@user_passes_test(teacher_user_test, "teacher")
def add_mcq_choice(request: HttpRequest) -> JsonResponse:

    request_data = json.loads(request.body)
    form = CreateChoiceAnswerForm(request_data)
    
    # making sure that there is "question_id" in the body of the request
    if request_data.get("question_id") is None:
        return JsonResponse({
                "message": _("question id should be included in the request"),
                "error": "question_id"
        }, status=400)

    if form.is_valid():
        instance = form.save(commit=False)

        # here I added the question_id manually because of strange behavior where it is not added to the form
        instance.question_id = request_data["question_id"]

        # verify the identity of the user
        question = get_object_or_404(MultipleChoiceQuestion, id=instance.question_id)
        current_normal_user = NormalUser.objects.get(user=request.user)
        current_teacher = Teacher.objects.get(normal_user=current_normal_user)

        if question.teacher == current_teacher:

            # here we will make sure that there is no two true choices at the same question

            right_anwser =  question.choiceanswer_set.filter(is_right=True)  # type: ignore

            if right_anwser and instance.is_right:
                return JsonResponse({
                    "message": _("There is already a true answer to this question"),
                    "error": "right_repeated"
                }, status=400)

        else:
            # not the same teacher case
            return JsonResponse({
                "error": "forbidden"
            }, status=403)

        instance.save()

        return JsonResponse({
            "message": "success",
            "new_choice": {
                "id": instance.id,
                "content_arabic": instance.content_arabic,
                "content_english": instance.content_english,
                "is_right": instance.is_right
            }
        })
    
    else:
        return JsonResponse({
            "message": _("There is Might Some Thing Wrong"),
            "error": "non-valid_form"
        }, status=400)
