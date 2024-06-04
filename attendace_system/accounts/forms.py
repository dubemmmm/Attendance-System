from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

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

class TeacherRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'is_teacher': forms.HiddenInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user
    
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
