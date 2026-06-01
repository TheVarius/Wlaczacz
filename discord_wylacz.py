import os
import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
AUTHORIZED_USER_ID = int(os.getenv('AUTHORIZED_USER_ID'))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('bot is ready!')

@bot.command(name='wylacz')
async def command_shutdown(ctx):
    if ctx.author.id != AUTHORIZED_USER_ID:
        await ctx.send("you are not the owner so you can't do that.")
        return
    
    await ctx.send("shutting down the pc...")
    
    os.system("shutdown /s /t 0")

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
