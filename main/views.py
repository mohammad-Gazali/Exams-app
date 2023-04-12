from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.paginator import Paginator
from main.forms import SendingEmailForm, CreateNormalUserForm, CreateTeacherForm
from main.models import NormalUser, Teacher
from main.user_tests import normal_user_test, teacher_user_test
from exams.models import Exam, MultipleChoiceQuestion, TrueFalseQuestion, EssayQuestion
from typing import Literal



def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')


def about_us(request: HttpRequest) -> HttpResponse:
    return render(request, 'about_us.html')


def contact(request: HttpRequest) -> HttpResponse:

    form = SendingEmailForm()

    sended = False

    if request.method == "POST":

        if not request.user.is_authenticated:
            return redirect("contact")
        

        form = SendingEmailForm(request.POST)

        if form.is_valid():

            if not request.user.is_authenticated:
                form.add_error(field=None, error=_("Please Login Firstly, You Should Login Before Sending a Contact Email."))


            else:
                subject = form.cleaned_data.get("subject")
                message = form.cleaned_data.get("message")


                msg_html = render_to_string('email/contact.html', {
                    "subject": subject,
                    "message": message
                    })

                send_mail(
                    subject=subject,
                    html_message=msg_html,
                    message=msg_html,
                    from_email=request.user.email, # type: ignore
                    recipient_list= [settings.CONTACT_EMAIL]
                )

                sended = True

                form = SendingEmailForm()


    return render(request, 'contact.html', {"form": form, "sended": sended})


def support(request: HttpRequest) -> HttpResponse:
    return render(request, 'support.html')


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    normal_user = NormalUser.objects.filter(user=request.user).first()

    if normal_user:
        is_teacher = bool(Teacher.objects.filter(normal_user=normal_user))

        return render(request, "profile/profile_main.html", {"normal_user": normal_user, "is_teacher": is_teacher})
    
    else:
        form = CreateNormalUserForm()
        if request.method == "POST":
            form = CreateNormalUserForm(request.POST, request.FILES)

            if form.is_valid():
                normal_user = NormalUser.objects.create(
                    gender=form.cleaned_data["gender"],
                    nationality=form.cleaned_data["nationality"],
                    birthdate=form.cleaned_data["birthdate"],
                    phone_number=form.cleaned_data["phone_number"],
                    personal_image=form.cleaned_data["personal_image"],
                    user_id=request.user.id  # type: ignore
                )

                return render(request, "profile/profile_main.html", {"normal_user": normal_user})

        return render(request, "profile/profile_make.html", {"form": form})
    

@user_passes_test(normal_user_test, "profile")
def teacher_main(request: HttpRequest) -> HttpResponse:
    normal_user = NormalUser.objects.get(user=request.user)
    teacher = Teacher.objects.filter(normal_user_id=normal_user).first()
    if teacher:
        exams = Exam.objects.filter(teacher=teacher).order_by("-created_at")
        paginator = Paginator(exams, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "teacher/teacher_dashboard.html", {"teacher": teacher, "page_obj": page_obj})

    else:
        form = CreateTeacherForm()
        if request.method == "POST":
            form = CreateTeacherForm(request.POST, request.FILES)

            if form.is_valid():
                teacher = Teacher.objects.create(
                    bio=form.cleaned_data["bio"],
                    cv=form.cleaned_data["cv"],
                    certificate=form.cleaned_data["certificate"],
                    normal_user=normal_user
                )

                return render(request, "teacher/teacher_dashboard.html", {"teacher": teacher})
            
        return render(request, "teacher/teacher_make.html", {"form": form})
    

@user_passes_test(teacher_user_test, "teacher")
def teacher_exams(request: HttpRequest) -> HttpResponse:
    normal_user = NormalUser.objects.get(user=request.user)
    teacher = Teacher.objects.get(normal_user_id=normal_user)
    
    exams = Exam.objects.filter(teacher=teacher).order_by("-created_at")
    paginator = Paginator(exams, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "teacher/my_exams.html", {"teacher": teacher, "page_obj": page_obj})


@user_passes_test(teacher_user_test, "teacher")
def teacher_questions(request: HttpRequest, q_type: Literal["mcq", "true-false", "essay"]) -> HttpResponse:
    normal_user = NormalUser.objects.get(user=request.user)
    teacher = Teacher.objects.prefetch_related().get(normal_user_id=normal_user)

    page_number = request.GET.get("page")


    mcq_questions = MultipleChoiceQuestion.objects.filter(teacher=teacher)
    mcq_paginator = Paginator(mcq_questions, 12)
    mcq_page_obj = mcq_paginator.get_page(page_number)

    true_false_questions = TrueFalseQuestion.objects.filter(teacher=teacher)
    true_false_paginator = Paginator(true_false_questions, 12)
    true_false_page_obj = true_false_paginator.get_page(page_number)

    essay_questions = EssayQuestion.objects.filter(teacher=teacher)
    essay_paginator = Paginator(essay_questions, 12)
    essay_page_obj = essay_paginator.get_page(page_number)

    if q_type == "mcq":
        return render(request, "teacher/my_questions.html", {
                "teacher": teacher,
                "page_obj": mcq_page_obj,
                "type": "mcq"
            }
        )
    
    elif q_type == "true-false":
        return render(request, "teacher/my_questions.html", {
                "teacher": teacher,
                "page_obj": true_false_page_obj,
                "type": "true-false"
            }
        )
    
    else:
        return render(request, "teacher/my_questions.html", {
                "teacher": teacher,
                "page_obj": essay_page_obj,
                "type": "essay"
            }
        )