from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import template
from accounts.models import StudentProfile
from . import models
from . import forms
register = template.Library()

@login_required
def create_course(request):
    if request.method == 'POST':
        form = forms.CourseCreationForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('attendace:teacher-dashboard') 
        else:
            print(form.errors)
    else:
        form = forms.CourseCreationForm()
        return render(request, 'attendance/create_course.html', {'form':form})

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(models.Course, pk=course_id)
    if request.user.is_authenticated and request.user.is_student:
        course.students.add(request.user)
        return redirect('attendace:student-dashboard')
    else:
        return redirect('accounts:student-login')

@login_required
def teacher_dashboard(request):
    courses = models.Course.objects.filter(teacher=request.user)
    return render(request, 'attendance/teacher_dashboard.html', {'courses': courses})

@login_required
def student_dashboard(request):
    student = request.user
    enrolled_courses = student.enrolled_courses.all()
    available_courses = models.Course.objects.exclude(pk__in=[course.pk for course in enrolled_courses])
    context = {
        'enrolled_courses': enrolled_courses,
        'available_courses': available_courses,
    }
    return render(request, 'attendance/student_dashboard.html', context)

@login_required
def available_courses(request):
    student = request.user
    enrolled_courses = student.enrolled_courses.all()
    available_courses = models.Course.objects.exclude(pk__in=[course.pk for course in enrolled_courses])
    context = {
        'available_courses': available_courses,
    }
    return render(request, 'attendance/student_available_courses.html', context)
    

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(models.Course, id=course_id)
    is_enrolled = False
    if request.user.is_authenticated and request.user.is_student:
        is_enrolled = course.students.filter(id=request.user.id).exists()
    return render(request, 'attendance/course_details.html', {'course': course, 'is_enrolled':is_enrolled})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(models.Course, id=course_id)
    if request.method == 'POST':
        form = forms.CourseUpdateForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('attendace:teacher-dashboard')
    else:
        form = forms.CourseUpdateForm(instance=course)
    
    return render(request, 'attendance/edit_course.html', {'form': form, 'course': course})

@login_required
def enrolled_student(request, course_id):
    course = get_object_or_404(models.Course, id=course_id)
    student = course.students.all()
    context = {
        'course': course,
        'students': student
    }
    return render(request, 'attendance/enrolled_students.html', context)

@login_required
def unenroll_student(request, course_id, student_id):
    course = get_object_or_404(models.Course, id=course_id)
    student_profile = get_object_or_404(StudentProfile, student_id=student_id)
    student = student_profile.user
    if request.user.is_teacher:
        course.students.remove(student)
        return redirect('attendace:enrolled-students', course_id=course_id)
    else:
        return redirect('accounts:teacher-login')
    
@login_required
def user_profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'attendance/user_profile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = forms.ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('attendace:user-profile')
        else:
            messages.error(request, 'Please correct the error below')
    else:
        form = forms.ProfileUpdateForm(instance=request.user)

    return render(request, 'attendace/user_profile.html', {'form': form})

        