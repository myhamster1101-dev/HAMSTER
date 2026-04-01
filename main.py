import discord
from discord.ext import commands
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'==========================================')
    print(f'🚀 NAO-BOT STATUS EDITION ONLINE!')
    print(f'👤 Developer: p.hxmster')
    print(f'📅 Date: 30/03/2026')
    print(f'==========================================')
    
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
            except Exception as e:
                print(f'❌ Failed to load {filename}: {e}')

bot.run(os.getenv('TOKEN'))
