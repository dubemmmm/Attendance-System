from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Course(models.Model):
    course_title = models.CharField(max_length=50, default='')
    course_code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    requirements = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='enrolled_courses')

    def __str__(self):
        return self.course_code
    