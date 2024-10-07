from django.db import models

# Create your models here.
class quizsets(models.Model):
    set_number = models.IntegerField(primary_key=True, default=0)
    topic = models.CharField(max_length=50)
    question_count = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.topic} (Set {self.set_number})"

class questions(models.Model):
    quiz_set = models.ForeignKey('quizsets', related_name='questions', on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True)
    answer = models.CharField(max_length=1)
    A = models.CharField(max_length=255)  # Option A
    B = models.CharField(max_length=255)  # Option B
    C = models.CharField(max_length=255)  # Option C
    D = models.CharField(max_length=255)  # Option D
    def __str__(self):
        return f"Question {self.pk} for {self.quiz_set.topic}"
    
class resposnes(models.Model):
    user_name = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    time = models.IntegerField()
    score = models.IntegerField()
    set = models.ForeignKey('quizsets', related_name= 'responses', on_delete=models.CASCADE)
    def _str_(self):
            return f"Response of {self.user_name}"