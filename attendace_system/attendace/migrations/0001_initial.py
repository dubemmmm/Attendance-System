# Generated by Django 5.0.6 on 2024-05-29 14:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("course_code", models.CharField(max_length=50, unique=True)),
                ("description", models.TextField()),
                ("requirements", models.TextField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "students",
                    models.ManyToManyField(
                        related_name="enrolled_courses", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
