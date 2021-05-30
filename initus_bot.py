import requests
import random
import string
from bs4 import BeautifulSoup
import csv
from datetime import date, datetime
import json

from dotenv import load_dotenv
import os

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

from mal import MAL
from imdb import IMDB
from slang import SLANG
from link import LINK
from help import HELP

def de_emojify(s):
    printable = set(string.printable)
    return ''.join(filter(lambda x: x in printable, str(s)))

load_dotenv()

GUILD_ID = os.getenv('GUILD_ID')
TOKEN = os.getenv('DISCORD_TOKEN')
APIKEY = os.getenv('NEWS_API')
CHANNEL = os.getenv('CHANNEL_ID')
COMMAND_LOG = os.getenv('COMMAND_LOG_ID')
CHILL_LOUNGE = os.getenv('CHILL_LOUNGE')
ERROR_LOG = os.getenv('ERROR_LOG')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='_', intents = intents, help_command=None)
bot.launch_time = datetime.utcnow()

mal_obj = MAL(bot, COMMAND_LOG, CHILL_LOUNGE)
imdb_obj = IMDB(bot, COMMAND_LOG)
slang_obj = SLANG(bot, COMMAND_LOG)
link_obj = LINK(bot, GUILD_ID)
help_obj = HELP(bot, COMMAND_LOG)

bot.add_cog(mal_obj)
bot.add_cog(imdb_obj)
bot.add_cog(slang_obj)
bot.add_cog(link_obj)
bot.add_cog(help_obj)

@bot.event
async def on_ready():
    print(f'{bot.user} is connected\n')
    print('Currently on Servers:')
    for guild in bot.guilds:
        print(guild.name)

    channel = bot.get_channel(int(CHANNEL))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'_help'))
    # await channel.send('The Bot is online')
    # await channel.send('Initus Test time')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        response = f"Slow it down bro! Try again in { int(error.retry_after) }s."
        await ctx.reply(response)
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        channel = bot.get_channel(int(ERROR_LOG))
        await channel.send(error)
        raise error


# hi command
@bot.command(name='hi', brief="Says hi dumbo...")
async def greetings(ctx):
    channel = bot.get_channel(int(COMMAND_LOG))
    await channel.send(f'hi command used by { de_emojify(ctx.author) } in { ctx.channel } in { ctx.channel }')

    if ctx.author.id == 741159441092837427:
        response = f'I don\'t say Hi to dumb people like you! { ctx.author.mention }'
    else:
        response = f'Hello { ctx.author.mention }'

    await ctx.send(response)

bot.run(TOKEN)
