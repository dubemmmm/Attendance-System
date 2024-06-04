from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return '@{}'.format(self.username)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    encoding = models.TextField()

    def __str__(self):
        return self.user.username

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.username

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.username

'''from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            StudentProfile.objects.create(user=instance, student_id=str(uuid.uuid4())[:20])
        elif instance.is_teacher:
            TeacherProfile.objects.create(user=instance, teacher_id=str(uuid.uuid4())[:20])
        elif instance.is_admin:
            AdminProfile.objects.create(user=instance, admin_id=str(uuid.uuid4())[:20])
        if instance.is_student:
            # StudentProfile.objects.create(user=instance)
            student_profile = StudentProfile.objects.create(user=instance)
            student_profile.student_id = str(uuid.uuid4())[:20]  # Generate a unique student_id
            print('this student id is ', student_profile.student_id)
            student_profile.save()
            
        elif instance.is_teacher:
            # TeacherProfile.objects.create(user=instance)
            teacher_profile = TeacherProfile.objects.create(user=instance)
            teacher_profile.teacher_id = str(uuid.uuid4())[:20]  # Generate a unique teacher_id
            teacher_profile.save()
            
        elif instance.is_admin:
            #AdminProfile.objects.create(user=instance)
            admin_profile = AdminProfile.objects.create(user=instance)
            admin_profile.admin_id = str(uuid.uuid4())[:20]  # Generate a unique admin_id
            admin_profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_student and hasattr(instance, 'studentprofile'):
        instance.studentprofile.save()
    elif instance.is_teacher and hasattr(instance, 'teacherprofile'):
        instance.teacherprofile.save()
    elif instance.is_admin and hasattr(instance, 'adminprofile'):
        instance.adminprofile.save()
    if instance.is_student:
        instance.studentprofile.save()
    elif instance.is_teacher:
        instance.teacherprofile.save()
    elif instance.is_admin:
        instance.adminprofile.save()'''
