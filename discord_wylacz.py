import os
import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
# Wstrzykujemy klucze
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
AUTHORIZED_USER_ID = int(os.getenv('AUTHORIZED_USER_ID'))

intents = discord.Intents.default()
intents.message_content = True

# Bot jest gotowy
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('bot is ready!')

# Nasłuchiwanie na komendę wyłączania komputera
@bot.command(name='wylacz')
async def command_shutdown(ctx):
    # Sprawdzenie czy to Ty wysyłasz
    if ctx.author.id != AUTHORIZED_USER_ID:
        await ctx.send("you are not the owner so you can't do that.")
        return
    
    await ctx.send("shutting down the pc...")
    # Wyłączamy komputer
    os.system("shutdown /s /t 0")

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
