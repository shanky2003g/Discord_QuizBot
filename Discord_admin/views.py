from django.shortcuts import render, redirect
import google.generativeai as genai
import os
from .forms import QuizSetForm
from .models import *
import json

# Configure API key
genai.configure(api_key=os.environ["API_KEY"])

def dashboard(request):
    return render(request, 'dashboard.html')

def add_sets(request):
    if request.method == 'POST':
        form = QuizSetForm(request.POST)
        if form.is_valid():
            # Get data from the form
            question_count = form.cleaned_data['no_of_questions']
            topic = form.cleaned_data['topic']
            set_number = form.cleaned_data['set_number']
            # Generate questions only once after the form is submitted
            generate_questions(request, question_count, topic, set_number)
            # Redirect after form submission to prevent duplicate form resubmission
            return redirect('dashboard')
    else:
        form = QuizSetForm()

    return render(request, "dashboard.html", {"form": form})

def generate_questions(request, question_count, set_topic, set_number):
    # Check if the request is a POST to avoid multiple responses
    if request.method == 'POST':
        num_questions = question_count
        topic = set_topic

    # Constructing the prompt for generating questions in JSON format
    prompt_message = f"""
    Generate {num_questions} questions with 4 options (A, B, C, D) related to the topic {topic}. 
    The response should be in JSON format with the following structure and don't put ''' at the top and bottom:

    [
        {{
            "question": "Question text",
            "options": {{
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D"
            }},
            "answer": "Correct option"
        }},
    ]
    """

    # Call the Gemini model for content generation
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt_message)
    #print(response.text)
    # Ensure the response is not empty or just whitespace
    if response.text.strip():
        try:
            # Parse the JSON response from the model
            questions_data = json.loads(response.text)
            # Code to add file
            # Define the path where the JSON file will be stored
            file_path = os.path.join(os.getcwd(), 'generated_questions.json')

            # Write the questions to a JSON file
            with open(file_path, 'w') as json_file:
                json.dump(questions_data, json_file, indent=4)  # Write with indentation for readability

            print(f"Questions successfully saved to {file_path}")
            
            #storing in databae:
            quiz_set = quizsets.objects.create(
            set_number=set_number,
            topic=set_topic,
            question_count= question_count
            )
             # Prepare a list for bulk creation of questions
            questions_list = []
    
            for question_data in questions_data:
                # Extracting values from question_data
                question_text = question_data["question"]
                options = question_data["options"]
                answer = question_data["answer"]

                # Create a new question instance
                question = questions(
                    quiz_set=quiz_set,
                    description=question_text,
                    answer=answer,
                    A=options["A"],
                    B=options["B"],
                    C=options["C"],
                    D=options["D"],
                )
                questions_list.append(question)

            # Bulk create the questions
            questions.objects.bulk_create(questions_list)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
    else:
        print("Received an empty or invalid response from the model.")