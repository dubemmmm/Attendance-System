# Generated by Django 5.0.6 on 2024-05-26 23:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_studentprofile_encoding"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentprofile",
            name="encoding",
            field=models.TextField(),
        ),
    ]
