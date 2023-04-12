from django.urls import path
from exams import views



urlpatterns = [

    # normal views urls
    path('teacher/create', views.create_exam, name='exam_create'),
    path('teacher/edit/<uuid:exam_id>', views.edit_exam, name='exam_edit'),
    path('teacher/delete/<uuid:exam_id>', views.delete_exam, name='exam_delete'),
    path('teacher/finish/<uuid:exam_id>', views.finish_exam, name='exam_finish'),
    path('teacher/details/<uuid:exam_id>', views.exam_details, name='exam_details'),
    path('teacher/create-question/<str:q_type>', views.create_question, name='exam_create_question'),
    path('teacher/add-questions/<uuid:exam_id>/<str:q_type>', views.add_questions, name='exam_add_quastions'),
    path('teacher/add-questions/add-mcq-choices/<uuid:question_id>', views.add_mcq_quastion_choices, name='exam_add_mcq_choices'),
    path('teacher/add-questions/add-essay-keywords/<uuid:question_id>', views.add_essay_question_keyword, name='exam_add_essay_keywords'),
    path('teacher/add-questions-created-before/<uuid:exam_id>', views.add_questions_created_before, name='exam_add_quastions_created_before'),
    path('teacher/delete-question/<str:q_type>/<uuid:question_id>', views.delete_question, name='exam_question_delete'),
    path('teacher/remove-question-from-exam/<uuid:exam_id>/<str:q_type>/<uuid:question_id>', views.remove_question_from_exam, name='exam_remove_question_from_exam'),
    path('teacher/edit-question/<str:q_type>/<uuid:question_id>', views.edit_question, name='exam_question_edit'),
    path('teacher/question-details/<str:q_type>/<uuid:question_id>', views.question_details, name='exam_question_details'),

    path('take-exam/<uuid:exam_id>', views.take_exam, name='exam_take_exam'),

    # ajax urls
    
    path('ajax/add-mcq-choice', views.ajax_add_mcq_choice, name='ajax_add_mcq_choice'),
    path('ajax/delete-mcq-choice', views.ajax_delete_mcq_choice, name='ajax_delete_mcq_choice'),
    path('ajax/add-essay-keyword', views.ajax_add_essay_keyword, name='ajax_add_essay_keyword'),
    path('ajax/delete-essay-keyword', views.ajax_delete_essay_keyword, name='ajax_delete_essay_keyword'),
]
