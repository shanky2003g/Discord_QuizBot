# Generated by Django 5.0.1 on 2024-10-03 20:35

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="questions",
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
                ("answer", models.CharField(max_length=1)),
                ("A", models.CharField(max_length=255)),
                ("B", models.CharField(max_length=255)),
                ("C", models.CharField(max_length=255)),
                ("D", models.CharField(max_length=255)),
                ("correct_answer", models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name="quizsets",
            fields=[
                ("set_id", models.AutoField(primary_key=True, serialize=False)),
                ("topic", models.CharField(max_length=50)),
                ("question_count", models.IntegerField(default=0)),
            ],
        ),
    ]
