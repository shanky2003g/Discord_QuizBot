import discord
from discord.ext import commands
import json
import websockets
from dotenv import load_dotenv
load_dotenv() 
import os
token = os.getenv('TOKEN')
c_id = os.getenv('ID')
print(c_id)
# Enable necessary intents
intents = discord.Intents.default()
intents.messages = True  # Enable the messages intent
intents.presences = True  # Enable the presence intent
intents.members = True    # Enable the members intent

# Creating instance of bot
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print("Hello there! I am the bot, and I am ready to go!!")
    print("********************************************")

# Listening for command - "hello"
@client.command()
async def hello(ctx):
    await ctx.send("Hello")
    print("SUCCESS1")

@client.event
async def on_member_join(member):
    channel_id = int (c_id)
    channel = client.get_channel(channel_id)  # Retrieve the channel object using the ID

    if channel is not None:
        await channel.send(f"{member.mention} has joined the server!")  # Send the message
    else:
        print("Channel not found!")

    # Send a DM to the new member
    try:
        await member.send("Welcome to the server! Enjoy your Quiz!")
        print(f"Sent DM to {member.name}.")
    except discord.Forbidden:
        print(f"Could not send DM to {member.name}. They might have DMs disabled.")
    except discord.HTTPException as e:
        print(f"Failed to send DM to {member.name}: {e}")


@client.event
async def on_member_remove(member):
    channel_id = int(c_id)
    channel = client.get_channel(channel_id)  # Retrieve the channel object using the ID

    if channel is not None:
        await channel.send(f"{member.mention} Goodbye")  # Send the message
    else:
        print("Channel not found!")

@client.command()
async def goodbye(ctx):
    await ctx.send("Demo message2")
    print("SUCCESS2")

#Fetching available quiz sets
async def fetch_quiz_sets():
    async with websockets.connect('ws://localhost:8000/ws/quiz/') as websocket:
        await websocket.send(json.dumps({"action": "get_quiz_sets"}))
        response = await websocket.recv()
        return json.loads(response)

@client.command()
async def sets(ctx):
    try:
        quiz_sets = await fetch_quiz_sets()
        sets_message = "Available Quiz Sets:\n"
        for quiz_set in quiz_sets["quiz_sets"]:
             sets_message += f"{quiz_set}\n"
        await ctx.send(sets_message)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")  


#Fetching questions and opions present in set as demanded by user 
async def fetch_quiz_questions(set_number):
    # print("weferver")
    async with websockets.connect('ws://localhost:8000/ws/quiz/') as websocket:
        await websocket.send(json.dumps({"action": "get_quiz_questions", "set_number": set_number}))
        #  print("22222")
        count = await websocket.recv()
        data = json.loads(count)
        count = int(data["count"])
        print(data)
        questions = []
        print(count)
        while count > 0:
            response = await websocket.recv()
            count -= 1
            #print(response)
            data = json.loads(response)
            if "description" in data and "options" in data:
                questions.append(data)
            else:
                break  # Stop receiving when there's no more questions
        return questions 

@client.command()
async def set(ctx, set_number: str):
    try:
        # Validate that the input is a digit
        if not set_number.isdigit():
            await ctx.send("Please provide a valid set number (e.g., !set 1, !set 2).")
            return

        set_number = int(set_number)  # Convert to integer

        # Fetch the questions for the specified quiz set
        quiz_questions = await fetch_quiz_questions(set_number)

        # Check if there are questions in the set
        if not quiz_questions:
            await ctx.send(f"No questions found for set number {set_number}.")
            return

        for question in quiz_questions:
            # Constructing the message with question and options
            question_message = f"**{question['description']}**\n"
            options = question['options']
            for key in ['A', 'B', 'C', 'D']:
                question_message += f"{key}: {options[key]}\n"
            await ctx.send(question_message)

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


client.run(token)


