from django.urls import path
from main import views


urlpatterns = [
    # normal views urls
    path("", views.index, name="home"),
    path("about", views.about_us, name="about_us"),
    path("contact", views.contact, name="contact"),
    path("support", views.support, name="support"),
    path("profile", views.profile, name="profile"),
    path("teacher", views.teacher_main, name="teacher"),
    path("teacher/exams", views.teacher_exams, name="teacher_exams"),
    path(
        "teacher/questions/<str:q_type>",
        views.teacher_questions,
        name="teacher_questions",
    ),
]
