import os
import csv
import base64
from . import models
from . import forms
from logs.models import Log
from django import template
from datetime import datetime
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from .utils import is_ajax, classify_face
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import StudentProfile, UserProfile
register = template.Library()

#This is the view to create a course
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

#This is the view for students to enroll for a course
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(models.Course, pk=course_id)
    if request.user.is_authenticated and request.user.is_student:
        course.students.add(request.user)
        return redirect('attendace:student-dashboard')
    else:
        return redirect('accounts:student-login')

#This is the view to render the teachers dashboard
@login_required
def teacher_dashboard(request):
    courses = models.Course.objects.filter(teacher=request.user)
    return render(request, 'attendance/teacher_dashboard.html', {'courses': courses})

#This is the view to render the students dashboard
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


#This is the view to display the courses the student isnt enrolled in
@login_required
def available_courses(request):
    student = request.user
    enrolled_courses = student.enrolled_courses.all()
    available_courses = models.Course.objects.exclude(pk__in=[course.pk for course in enrolled_courses])
    context = {
        'available_courses': available_courses,
    }
    return render(request, 'attendance/student_available_courses.html', context)
    

#This is the view to display the details of the course
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(models.Course, id=course_id)
    is_enrolled = False
    if request.user.is_authenticated and request.user.is_student:
        is_enrolled = course.students.filter(id=request.user.id).exists()
    return render(request, 'attendance/course_details.html', {'course': course, 'is_enrolled':is_enrolled})

#This is the view that enables teachers to modify details of the course
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

#This is the view that allows teachers to see students enrolled in a course
@login_required
def enrolled_student(request, course_id):
    course = get_object_or_404(models.Course, id=course_id)
    student = course.students.all()
    context = {
        'course': course,
        'students': student
    }
    return render(request, 'attendance/enrolled_students.html', context)

#This is the view that enables teachers to unenroll students from a course
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
    
#This is the view that enables authenticated users modify their profiles
@login_required
def update_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = forms.ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
          
            return redirect('attendace:update-profile')
        else:
            messages.error(request, 'Please correct the error below')
            message = 'unable to modify profile'
    else:
        form = forms.ProfileUpdateForm(instance=request.user)
    context = {
        'form' : form,
        'user' : user,
        'user_profile' : user_profile,
        }
    return render(request, 'attendance/user_profile.html', context)

@login_required
def attendance_template(request, course_id):
    context = {
        'course_id': course_id,
    }
    return render(request, 'attendance/attendance.html', context)

def find_user_view(request, course_id):
    if is_ajax(request):
        photo = request.POST.get('photo')
        _, str_img = photo.split(';base64')
        decoded_file = base64.b64decode(str_img)
        x = Log()
        x.photo = ContentFile(decoded_file, 'upload.png')
        x.save()
        res = classify_face(x.photo.path, course_id=course_id)
        if res:
            # Keep track of recognized names in session
            if 'recognized_names' not in request.session:
                request.session['recognized_names'] = []
            
            if res not in request.session['recognized_names']:
                request.session['recognized_names'].append(res)
                request.session.modified = True
            
            return JsonResponse({'success': True})
        else:
            print('this user does not exist')
            return JsonResponse({'success': False})


def finish_attendance(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(models.Course, id=course_id)
        current_date = datetime.now().strftime("%Y-%m-%d")
        directory = "attendance_files"
        csv_filename = f'attendance_files/{course.course_code}_{current_date}.csv'
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        recognized_names = request.session.get('recognized_names', [])
        
        # Write recognized names to CSV file
        with open(csv_filename, 'w', newline='') as csvfile:
            lnwriter = csv.writer(csvfile)
            for name in recognized_names:
                current_time = datetime.now().strftime('%H:%M:%S')
                lnwriter.writerow([name, current_time, 'present'])
        
        # Generate list of absent students
        enrolled_students = course.students.all()
        enrolled_student_names = {f'{student.first_name} {student.last_name}' for student in enrolled_students}
        present_students = set(recognized_names)
        absent_students = enrolled_student_names - present_students
        
        # Write absent students to the CSV file
        with open(csv_filename, 'a', newline='') as csvfile:
            lnwriter = csv.writer(csvfile)
            for absent_student in absent_students:
                lnwriter.writerow([absent_student, 'N/A', 'absent'])
        
        # Clear recognized names from session
        if 'recognized_names' in request.session:
            del request.session['recognized_names']
        
        return redirect('attendace:teacher-dashboard')
        
            
@login_required
def get_student_profile(request, student_id):
    student_profile = get_object_or_404(StudentProfile, student_id=student_id)
    user = student_profile.user
    user_profile = get_object_or_404(UserProfile, user=user)
    context = {
        'user': user,
        'profile_image': user_profile.image.url
    }
    return render(request, 'attendance/view_student_profile.html', context)


