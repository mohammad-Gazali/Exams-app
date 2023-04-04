from django.urls import path
from exams import views



urlpatterns = [

    # normal views urls
    path('teacher/create', views.create_exam, name='exam_create'),
    path('teacher/edit/<uuid:exam_id>', views.edit_exam, name='exam_edit'),
    path('teacher/delete/<uuid:exam_id>', views.delete_exam, name='exam_delete'),
    path('teacher/add-questions/<uuid:exam_id>', views.add_questions, name='exam_add_quastions'),
    path('teacher/add-questions/add-mcq-details/<uuid:question_id>', views.add_mcq_quastion_details, name='exam_add_mcq_details'),


    # ajax urls
    
    path('ajax/add-mcq-choice', views.add_mcq_choice, name='ajax_add_mcq_choice'),
]
