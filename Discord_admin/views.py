from django.shortcuts import render, HttpResponse
import google.generativeai as genai
import os
from .forms import QuizSetForm
genai.configure(api_key=os.environ["API_KEY"])
# Create your views here.

# model = genai.GenerativeModel("gemini-1.5-flash")
# response = model.generate_content("Give me 2 questions along with 4 options related to OS topic with answer")
# print(response.text)

def dashboard(request):
    return render(request, 'dashboard.html')

def add_sets(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request:
        form = QuizSetForm(request.POST)
        # Check whether the form is valid
        if form.is_valid():
            print("heloo")
            # Save the new QuizSet to the database
            # form.save()
            question_count =  form.cleaned_data['no_of_questions']
            topic = form.cleaned_data['topic']
            generate_questions(request, question_count, topic)
    else:
        form = QuizSetForm()  # Create an empty form for GET requests
    
    return render(request, "dashboard.html", {"form": form})

def generate_questions(request, question_count, set_topic):
    if request.method == 'POST':
        num_questions = question_count
        topic = set_topic
        #Constructing the prompt
        prompt_message = f"Generate {num_questions} questions with 4 options A,B,C,D with answer related to {topic} topic"
        #Now make prompt to gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt_message)
        # print(response.text)