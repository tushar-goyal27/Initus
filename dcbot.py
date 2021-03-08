import requests
import discord
from discord.ext import commands

TOKEN = ''
APIKEY = ''
guild = ''

def get_everything(keyword=''):
    url = 'https://newsapi.org/v2/top-headlines'

    params = {
        'q': keyword,
        'apiKey': APIKEY
    }

    src = requests.get(url, params=params)

    articles = src.json()['articles']
    i = random.randint(0, len(articles) - 1)
    article = articles[i]
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
    if str(ctx.message.author) == 'jayant Vashisth#6685':
        response = f'I don\'t say Hi to dumb people like you! { ctx.message.author.mention }'
    else:
        response = f'Hello { ctx.message.author.mention }'

    await ctx.send(response)

@bot.command(name='news', help="gets news")
async def news(ctx, keyword=''):
    print(f'news command used by { ctx.message.author }')
    if keyword == '':
        response = 'You haven\'t entered a topic, thus showing top news for India.'
        keyword = 'India'
        response += f'\n { get_everything(keyword)} '
    else:
        response = get_everything(keyword)
    await ctx.send(response)

bot.run(TOKEN)
