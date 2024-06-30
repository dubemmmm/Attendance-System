from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, TeacherProfile

# This is the form class used for creating student objects
class StudentRegisterForm(UserCreationForm):
    encoding = forms.ImageField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'encoding']
        widgets = {
            'is_student': forms.HiddenInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
        return user

# This is the form class used for creating teacher objects
class TeacherRegisterForm(UserCreationForm):
    encoding = forms.ImageField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'encoding']
        widgets = {
            'is_teacher': forms.HiddenInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user
    
# This is the forrm class for authenticating student and teacher objects    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form__input', 
            'placeholder': 'Username', 
            'required': 'required', 
            'autofocus': 'autofocus',
            'id': 'id_username'
        }),
        label='',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form__input', 
            'placeholder': 'Password', 
            'required': 'required',
            'id': 'id_password'
        }),
        label='',
    )
