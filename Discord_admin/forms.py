from django import forms

class QuizSetForm(forms.Form):
    set_number = forms.IntegerField(label='Set Number', min_value=1)
    no_of_questions = forms.IntegerField(label='Number of Questions', min_value=1)
    topic = forms.CharField(label='Topic', max_length=100)
    per_question_duration = forms.IntegerField(label='Per Question Duration (in seconds)', min_value=1, help_text="Enter duration in seconds")
