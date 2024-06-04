from django.urls import path, include
from . import views
app_name = 'accounts'

urlpatterns = [
    path('student/signup/', views.register_student, name='student-signup'),
    path('teacher/signup/', views.register_teacher, name='teacher-signup'),
    path('student/login/', views.student_login, name='student-login'),
    path('teacher/login/', views.teacher_login, name='teacher-login'),
    # Add other paths such as login, logout, etc.
]

