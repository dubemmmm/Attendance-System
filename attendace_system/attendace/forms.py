from django import forms
from django.forms.widgets import DateInput
from .models import Course
from django.contrib.auth.models import User

class CourseCreationForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Start Date'
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='End Date'
    )
    class Meta:
        model = Course
        fields = ['course_title','course_code', 'description', 'requirements', 'start_date', 'end_date']
        def clean(self):
            cleaned_data = super().clean()
            start_date = cleaned_data.get('start_date')
            end_date = cleaned_data.get('end_date')

            if start_date and end_date and start_date >= end_date:
                raise forms.ValidationError("End date must be after the start date.")

            return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        
        
class CourseUpdateForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Start Date'
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='End Date'
    )
    class Meta:
        model = Course
        fields = ['course_title', 'course_code', 'description', 'requirements', 'start_date', 'end_date']
        def clean(self):
            cleaned_data = super().clean()
            start_date = cleaned_data.get('start_date')
            end_date = cleaned_data.get('end_date')

            if start_date and end_date and start_date >= end_date:
                raise forms.ValidationError("End date must be after the start date.")

            return cleaned_data