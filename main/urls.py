from django.urls import path
from main import views


urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about_us, name='about_us'),
    path('contact', views.contact, name='contact'),
    path('support', views.support, name='support'),
    path('profile', views.profile, name='profile'),
    path('teacher', views.teacher, name='teacher'),
    path('teacher/exam/create', views.teacher_create_exam, name='teacher_create_exam')
]