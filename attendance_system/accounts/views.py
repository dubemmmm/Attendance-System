from django.shortcuts import render, redirect
from .forms import StudentRegisterForm, TeacherRegisterForm, CustomAuthenticationForm
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import StudentProfile, TeacherProfile, UserProfile
import face_recognition
import uuid
# Create your views here.

# This is the view for creating the student object as well as encoding the student image
def register_student(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True
            print('this is a student registration')
            # Getting the image uploaded by the student
            image = form.cleaned_data.get('encoding')
            image_path = image.temporary_file_path() if hasattr(image, 'temporary_file_path') else image.file
            try:
                # Use the face_recognition library to load the image file
                face_image = face_recognition.load_image_file(image_path)
                # Encode the face image
                face_encodings = face_recognition.face_encodings(face_image)
                if face_encodings:
                    encoding = face_encodings[0]
                    encoding_str = ','.join(map(str, encoding))
                    user.save()
                    # Save the object
                    StudentProfile.objects.create(
                        user=user,
                        student_id=str(uuid.uuid4())[:20],
                        encoding=encoding_str 
                    )
                    UserProfile.objects.create(
                        user=user,
                        image=image
                    )
                    messages.success(request, f'Account created for {user.username}!')
                    return redirect('accounts:student-login')
                else:
                    form.add_error('image', 'No face found in the image. Please upload a clear image of your face.')
            except Exception as e:
                form.add_error('image', f'Error processing the image: {e}')
        else:
            print('Form is invalid:', form.errors)
    else:
        form = StudentRegisterForm()

    return render(request, 'accounts/student_signup.html', {'form': form})
            
            
# This is the view for creating the teacher object
def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            print('form is valid')
            user = form.save()
            user.is_teacher = True
            user.save()
            image = form.cleaned_data.get('encoding')
            print('gotten the image correctly')
            
            print(user.email)
            TeacherProfile.objects.create(
                user=user,
                teacher_id = str(uuid.uuid4())[:20],
            )
            UserProfile.objects.create(
                        user=user,
                        image = image,
                    )
            messages.success(request, f'Account created for {user.username}!')
            return redirect('accounts:teacher-login')
    else:
        print('these is an error somewhere')
        form = TeacherRegisterForm()
    return render(request, 'accounts/teacher_signup.html', {'form': form})



# Using Django's built-in login view for student authentication
class StudentLoginView(auth_views.LoginView):
    template_name = 'accounts/student_login.html'
    form_class = CustomAuthenticationForm
    next_page = reverse_lazy('attendace:student-dashboard')  # The URL name you want to redirect to after login

def student_login(request):
    return StudentLoginView.as_view()(request)


# Using Django's built-in login view for teacher authentication
class TeacherLoginView(auth_views.LoginView):
    template_name = 'accounts/teacher_login.html'
    form_class = CustomAuthenticationForm
    next_page = reverse_lazy('attendace:teacher-dashboard')  # The URL name you want to redirect to after login

def teacher_login(request):
    return TeacherLoginView.as_view()(request)

