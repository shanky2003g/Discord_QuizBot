from django.db import models

# Create your models here.
class quizsets(models.Model):
    set_id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=50)
    question_count = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.topic} (Set {self.set_id})"

class questions(models.Model):
    quiz_set = models.ForeignKey('quizsets', related_name='questions', on_delete=models.CASCADE, null=True)
    description = models.TextField
    answer = models.CharField(max_length=1)
    A = models.CharField(max_length=255)  # Option A
    B = models.CharField(max_length=255)  # Option B
    C = models.CharField(max_length=255)  # Option C
    D = models.CharField(max_length=255)  # Option D
    def __str__(self):
        return f"Question {self.pk} for {self.quiz_set.topic}"