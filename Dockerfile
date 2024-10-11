FROM python:3.11.5

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

# Start both the Django server and the bot script
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000 & python bot/bot.py"]
EXPOSE 8000
