# Generated by Django 5.0.1 on 2024-10-03 20:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Discord_admin", "0002_questions_quiz_set"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="questions",
            name="correct_answer",
        ),
    ]
