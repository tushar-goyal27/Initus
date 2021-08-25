import string
from datetime import date, datetime
import json

from dotenv import load_dotenv
import os

import discord
from discord.ext import commands

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

bot = commands.Bot(command_prefix='_', intents = intents, help_command=None, case_insensitive=True)
bot.launch_time = datetime.utcnow()

@bot.event
async def on_ready():
    log = bot.get_channel(int(COMMAND_LOG))
    lounge = bot.get_channel(int(CHILL_LOUNGE))
    guild = bot.get_guild(int(GUILD_ID))

    bot.add_cog(MAL(bot, log, lounge))
    bot.add_cog(IMDB(bot, log))
    bot.add_cog(SLANG(bot, log))
    bot.add_cog(LINK(bot, guild))
    bot.add_cog(HELP(bot, log))

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
