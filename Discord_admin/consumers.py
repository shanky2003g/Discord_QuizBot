# your_app/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
import asyncio

class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        if data['action'] == 'get_quiz_sets':
            quiz_sets = await self.get_quiz_sets()
            await self.send_quiz_sets(quiz_sets)


        if data['action'] == 'get_quiz_questions':
            set_number = data['set_number']
            questions_all = await self.get_questions_for_set(set_number)
            # print(questions_all)
            for question in questions_all:
                await self.send(json.dumps({"description": question["description"], "options": question["options"]}))
                await asyncio.sleep(2)  # Delay of 2 seconds for each question

    async def get_quiz_sets(self):
        try:
            quiz_sets = await database_sync_to_async(self.fetch_quiz_sets)()
            return quiz_sets
        except Exception as e:
            # Handle exceptions (e.g., logging)
            print(f"Error fetching quiz sets: {e}")
            return []
        
    def fetch_quiz_sets(self):
        # Fetch quiz sets objects from database
        from .models import quizsets
        return [str(quiz_set) for quiz_set in quizsets.objects.all()]

    async def send_quiz_sets(self,quiz_sets):
        await self.send(text_data=json.dumps({
            'quiz_sets': quiz_sets
        }))
    
    @database_sync_to_async
    def get_questions_for_set(self, set_number):
        from .models import questions
        # Fetch questions for the specified set number
        questions_queryset = questions.objects.filter(quiz_set=set_number)  # Filter by quiz_set
        question_data = []

        for question in questions_queryset:
            question_data.append({
                "description": question.description,
                "options": {
                    "A": question.A,  # Option A
                    "B": question.B,  # Option B
                    "C": question.C,  # Option C
                    "D": question.D   # Option D
                }
            })

        return question_data