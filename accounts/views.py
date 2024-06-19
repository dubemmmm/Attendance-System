from django.shortcuts import render, redirect
from .forms import StudentRegisterForm, TeacherRegisterForm, CustomAuthenticationForm
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import StudentProfile, TeacherProfile, UserProfile
import face_recognition
import uuid
# Create your views here.

def register_student(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True
            print('this is a student registration')
            image = form.cleaned_data.get('encoding')
            image_path = image.temporary_file_path() if hasattr(image, 'temporary_file_path') else image.file
            try:
                face_image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(face_image)
                if face_encodings:
                    encoding = face_encodings[0]
                    encoding_str = ','.join(map(str, encoding))
                    user.save()
                    print('User saved:', user)

                    StudentProfile.objects.create(
                        user=user,
                        student_id=str(uuid.uuid4())[:20],
                        encoding=encoding_str  # Set the encoding field here
                    )
                    UserProfile.objects.create(
                        user=user,
                        image=image
                    )
                    print('StudentProfile created for user:', user)
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
            


def register_teacher(request):
    
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
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
            print('Teacher Profile successfully created.', user)
            print('Teacher Profile successfully created.', user.email)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('accounts:teacher-login')
    else:
        print('these is an error somewhere')
        form = TeacherRegisterForm()
    return render(request, 'accounts/teacher_signup.html', {'form': form})



# You can use Django's built-in login view for student login
class StudentLoginView(auth_views.LoginView):
    template_name = 'accounts/student_login.html'
    form_class = CustomAuthenticationForm
    next_page = reverse_lazy('attendace:student-dashboard')  # The URL name you want to redirect to after login

def student_login(request):
    return StudentLoginView.as_view()(request)


class TeacherLoginView(auth_views.LoginView):
    template_name = 'accounts/teacher_login.html'
    form_class = CustomAuthenticationForm
    next_page = reverse_lazy('attendace:teacher-dashboard')  # The URL name you want to redirect to after login

def teacher_login(request):
    return TeacherLoginView.as_view()(request)


'''def register_student(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('accounts:student-login')
    else:
        form = StudentRegisterForm()
    return render(request, 'accounts/student_signup.html', {'form': form})'''