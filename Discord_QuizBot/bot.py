import discord
from discord.ext import commands
import json
import websockets,asyncio
from dotenv import load_dotenv
from discord.ui import Button, View
import time
from settings import BASE_DIR
load_dotenv(BASE_DIR/".env") 
import os
token = str(os.getenv('TOKEN'))
c_id = os.getenv('ID')
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
    #print("SUCCESS1")

@client.event
async def on_member_join(member):
    channel_id = int (c_id)
    channel = client.get_channel(channel_id)  # Retrieve the channel object using the ID

    if channel is not None:
        await channel.send(f"{member.mention} has joined the server!")  # Send the message
    else:
        print("Channel not found!")

    # Send a DM to the new member
    welcome_message = f"""
    Welcome to the server, {member.name}! Enjoy your Quiz!

    Here are some commands you can use:
    - **!hello**: Say hello to the bot!
    - **!goodbye**: Say goodbye!
    - **!sets**: Show the current available quiz sets.
    - **!set "set_number"**: Choose the set you want to attend. For example: `!set 1`
    - **!leaderboard "set_number"**: Check the leaderboard for a specific set. For example: `!leaderboard 1`
    - Each question carry 1 mark.
    """
    try:
        
        await member.send(welcome_message)
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
        await channel.send(f"{member.mention} left the channel")  # Send the message
    else:
        print("Channel not found!")

@client.command()
async def goodbye(ctx):
    await ctx.send("Demo message2")
    print("BYE")

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
    async with websockets.connect('ws://localhost:8000/ws/quiz/') as websocket:
        await websocket.send(json.dumps({"action": "get_quiz_questions", "set_number": set_number}))
        count = await websocket.recv()
        data = json.loads(count)
        count = int(data["count"])
        # print(data)
        questions = []
        # print(count)
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
    responses = ""
    start_time = time.time()
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
            # await ctx.send(question_message)
            buttons = [
                Button(label = 'A', style = discord.ButtonStyle.primary, custom_id ='A'),
                Button(label = 'B', style = discord.ButtonStyle.primary, custom_id ='B'),
                Button(label = 'C', style = discord.ButtonStyle.primary, custom_id ='C'),
                Button(label ='D', style = discord.ButtonStyle.primary, custom_id ='D'),
                Button(label = "SKIP", style = discord.ButtonStyle.secondary, custom_id = 'SKIP')
            ]
            #creating view for buttons
            view = View()
            for button in buttons:
                view.add_item(button)
            
            #Defining callbsck when user interact with button(user hits the button)
            async def button_callback(interaction: discord.Interaction):
                nonlocal responses
                button_label = interaction.data['custom_id']
                if button_label == "SKIP":
                    responses+= ' '
                else:
                    responses += button_label
                await interaction.response.send_message(f'You selected: {button_label}', ephemeral=True)
                view.stop()  # Stop the view after interaction


            ##attach callbacks for each button
            for button in buttons:
                button.callback = button_callback

            await ctx.send(question_message, view = view)
            # Wait for either the user to press any button or 5 seconds to pass
            try:
                await asyncio.wait_for(view.wait(), timeout=100.0)
            except asyncio.TimeoutError:
                await ctx.send("Time's up! Moving to the next question.")
                view.stop()
        end_time = time.time()
        total_time = end_time - start_time
        await ctx.send("Quiz Ends! Processing  your rank and leaderboard.......")
        # await leaderboard(ctx, str(set_number)
        await send_user_response(responses, total_time, str(ctx.author), set_number)
        await asyncio.sleep(2)
        await leaderboard(ctx, str(set_number))

    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
    
async def send_user_response(responses, total_time, user_name, set_number):
    async with websockets.connect('ws://localhost:8000/ws/quiz/') as websocket:
        await websocket.send(json.dumps({"action": "user_response", "responses" : responses, "total_time":total_time, "user_name":user_name,
                                         "set_number" :set_number}))
        response = await websocket.recv()
        data = json.loads(response)
        score = data['score']
        # print(score)
    

@client.command()
async def leaderboard(ctx, set_number:str):
    if not set_number.isdigit():
            await ctx.send("Please provide a valid set number (e.g., !set 1, !set 2).")
            return

    set_number = int(set_number)  # Convert to integer
    quiz_leaderboard = await fetch_leaderboard(set_number, ctx)
    await ctx.send(quiz_leaderboard)


async def fetch_leaderboard(set_number, ctx):
    async with websockets.connect('ws://localhost:8000/ws/quiz/') as websocket:
        await websocket.send(json.dumps({"action": "fetch_leaderboard", "set_number" :set_number}))
        response = await websocket.recv()
        data = json.loads(response)
        leaderboard = "LEADERBOARD:\n"
        leaderboard += f"**{'Rank':<5} {'Name':<20} {'Score':<6} {'Time':<4}**\n" 
        for index, x in enumerate(data['leaderboard']):
            rank = index + 1 
            leaderboard += f"{rank:<5} {x['name']:<20} {x['score']:<6} {x['time']:<4}\n"
            
            if x['name'] == str(ctx.author): 
                user_rank = rank 

        # print(str(ctx.author))
        # print(leaderboard)
        await ctx.send(f"Your rank is: {user_rank}")
        return leaderboard


client.run(token)


