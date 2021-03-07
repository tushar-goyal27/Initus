import requests
import discord
from discord.ext import commands

TOKEN = ''
APIKEY = ''
guild = ''

def get_everything(keyword=''):
    url = 'https://newsapi.org/v2/everything'

    params = {
        'q': keyword,
        'apiKey': APIKEY
    }

    src = requests.get(url, params=params)

    article = src.json()['articles'][0]
    response = f"**{ article['title'] }** \n{ article['description'] } \n{ article['url'] }"

    return response


intents = discord.Intents.all()

bot = commands.Bot(command_prefix='_', intents = intents)

@bot.event
async def on_ready():
    guild = discord.utils.find(lambda s: s.name == guild, bot.guilds)

    print(f'{bot.user} is connected\n')

    print('Server members:')
    for member in guild.members:
        print(member.name)


@bot.command(name='hi', help="Says hi dumbo...")
async def greetings(ctx, name=''):
    print(f'hi command used by { ctx.message.author }')
    if str(ctx.message.author) != 'TusharGoyal#4077':
        response = f'I don\'t say Hi to dumb people like you! { ctx.message.author.mention }'
    else:
        response = f'Hello { ctx.message.author.mention }'

    await ctx.send(response)

@bot.command(name='news', help="gets news")
async def news(ctx, keyword=''):
    print(f'news command used by { ctx.message.author }')
    response = get_everything(keyword)
    await ctx.send(response)

bot.run(TOKEN)
