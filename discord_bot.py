import socket
import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
AUTHORIZED_USER_ID = int(os.getenv('AUTHORIZED_USER_ID', '0'))
PC_MAC_ADDRESS = os.getenv('PC_MAC_ADDRESS')
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def wake_on_lan(mac_address):
    clean_mac = mac_address.replace(':', '').replace('-', '').replace('.', '')
    
    if len(clean_mac) != 12:
        return False
        
    try:
        mac_bytes = bytes.fromhex(clean_mac)
        magic_packet = b'\xff' * 6 + mac_bytes * 16
        
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic_packet, ('255.255.255.255', 9))
            
        return True
    except Exception:
        return False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='wlacz')
async def command_wake(ctx):
    if ctx.author.id != AUTHORIZED_USER_ID:
        await ctx.send("you are not the owner so you can't do that.")
        return
    
    await ctx.send("waking up the pc now...")
    
    success = wake_on_lan(PC_MAC_ADDRESS)
    
    if success:
        await ctx.send("done!")
    else:
        await ctx.send("something went wrong.")

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
