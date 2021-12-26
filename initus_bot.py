import string
from datetime import date, datetime
import json
import os

import discord
from discord.ext import commands
import config

from mal import MAL
from imdb import IMDB
from slang import SLANG
from help import HELP

def de_emojify(s):
    printable = set(string.printable)
    return ''.join(filter(lambda x: x in printable, str(s)))

TOKEN = config.DISCORD_TOKEN
COMMAND_LOG = config.COMMAND_LOG
CHILL_LOUNGE = config.CHILL_LOUNGE
ERROR_LOG = config.ERROR_LOG

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='_', intents = intents, help_command=None, case_insensitive=True)
bot.launch_time = datetime.utcnow()

@bot.event
async def on_ready():
    log = bot.get_channel(COMMAND_LOG)
    lounge = bot.get_channel(CHILL_LOUNGE)

    bot.add_cog(MAL(bot, log, lounge))
    bot.add_cog(IMDB(bot, log))
    bot.add_cog(SLANG(bot, log))
    bot.add_cog(HELP(bot, log))

    print(f'{bot.user} is connected\n')
    print('Currently on Servers:')
    for guild in bot.guilds:
        print(guild.name)

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'_help in { len(bot.guilds) } servers'))

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
