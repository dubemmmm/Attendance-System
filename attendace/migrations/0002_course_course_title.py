# Generated by Django 5.0.6 on 2024-05-31 15:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("attendace", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="course_title",
            field=models.CharField(default="", max_length=50),
        ),
    ]
