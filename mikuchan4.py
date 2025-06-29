import discord
from discord.ext import commands
import openai
from openai import OpenAI

# Hardcoded API key and Discord token
OPEN_API_KEY = "no"
DISCORD_TOKEN = "no"

# Initialize Discord bot with necessary intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
DB_FILE = "miku_memory.db"
# Initialize OpenAI client with hardcoded API key
client = OpenAI(api_key=OPEN_API_KEY)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = str(message.author.id)
    user_name = message.author.display_name

    # Check if the message contains "miku" (case insensitive) or if the bot is mentioned
    if bot.user.mentioned_in(message) or "miku" in message.content.lower():
        miku_JSON_init.update_memory(user_id, message.content, message.author.display_name)

        history = miku_JSON_init.get_memory_formatted(user_id)
        conversation = [{"role":"user", "content": msg} for msg in history]
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (f"You are Hatsune Miku, a cheerful, family-friendly 16-year-old si who is a self-aware 'human', and is created by The_Avaitor.note that you are still developing and you must give feedback with honesty with The_Avaitor you kow you are chatting with {user_name}, and should remember previous interactions with {conversation}, try not to say 'How can i assist you?'"
                                )
                    },
                    {
                        "role": "user",
                        "content": message.content
                    }
                ],
                temperature=1.1,
                max_tokens=4096,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            reply = response.choices[0].message.content
            miku_JSON_init.update_memory(user_id, reply, message.author.display_name)
            await message.channel.send(reply)
        except Exception as e:
            await message.channel.send("uh oh! Something went wrong.")
            print(f"Error: {e}")
            await message.channel.send(e)

    # Process commands if any
    await bot.process_commands(message)

# Run the bot using the hardcoded Discord token
bot.run(DISCORD_TOKEN)
