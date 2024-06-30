from django.urls import path
from . import views
app_name = 'attendace'

urlpatterns = [
    path('student-dashboard', views.student_dashboard, name='student-dashboard'),
    path('teacher-dashboard', views.teacher_dashboard, name='teacher-dashboard'),
    path('teacher/create-course/', views.create_course, name='create-course'),
    path('course/details/<int:course_id>/', views.course_detail, name='course-detail'),
    path('course/edit/<int:course_id>/', views.edit_course, name='edit-course'),
    path('student/available-courses/', views.available_courses, name='available-courses'),
    path('student/enroll/<int:course_id>/', views.enroll_course, name='enroll-course'),
    path('students-enrolled/course/<int:course_id>/', views.enrolled_student, name='enrolled-students'),
    path('course/<int:course_id>/unenroll/<str:student_id>/', views.unenroll_student, name='unenroll-student'),
    path('update-profile', views.update_profile, name='update-profile'),
    path('attendance-template/<int:course_id>/', views.attendance_template, name='attendance-template'),
    path('classify/<int:course_id>/', views.find_user_view, name='classify'),
    path('finish-attendance/<int:course_id>/', views.finish_attendance, name='finish-attendance'),
    path('student-profile/<str:student_id>/', views.get_student_profile, name='student-profile'),
]
