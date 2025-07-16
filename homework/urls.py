from django.urls import path
from . import views
from courses.views import generate_quiz, quiz_review

urlpatterns = [
    path('', views.homework_list, name='homework_list'),
    path('quiz/<int:course_id>/', generate_quiz, name='quiz_generate'),
    path("quiz/<int:course_id>/review/", quiz_review, name="quiz_review"),
    path('submit/<int:task_id>/', views.homework_upload, name='homework_upload'),
]