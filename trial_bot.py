import requests
import random
from bs4 import BeautifulSoup
import csv
from datetime import date, datetime

from dotenv import load_dotenv
import os

import discord
from discord.ext import commands

csv_file = open('commandLog.csv', 'a')
csv_writer = csv.writer(csv_file)

load_dotenv()

GUILD = os.getenv('GUILD_NAME')
TOKEN = os.getenv('DISCORD_TOKEN')
APIKEY = os.getenv('NEWS_API')


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
    guild = discord.utils.find(lambda s: s.name == GUILD, bot.guilds)

    print(f'{bot.user} is connected\n')

    print('Server members:')
    for member in guild.members:
        print(member.name)


@bot.command(name='hi', help="Says hi dumbo...")
async def greetings(ctx, name=''):
    print(f'hi command used by { ctx.message.author }')
    csv_writer.writerow([str(datetime.now()), 'hi', ctx.message.author, 'None'])
    if str(ctx.message.author) == 'jayant Vashisth#6685':
        response = f'I don\'t say Hi to dumb people like you! { ctx.message.author.mention }'
    else:
        response = f'Hello { ctx.message.author.mention }'

    await ctx.send(response)

@bot.command(name='news', help="gets news")
async def news(ctx, keyword=''):
    print(f'news command used by { ctx.message.author }  for keyword { keyword }')
    csv_writer.writerow([str(datetime.now()), 'news', ctx.message.author, keyword])
    if keyword == '':
        response = 'You haven\'t entered a topic, thus showing top news for India.'
        keyword = 'India'
        response += f'\n { get_everything(keyword)} '
    else:
        response = get_everything(keyword)
        
    await ctx.send(response)

@bot.command(name='slang', help='Type _slang <word> to get the meaning of the slang')
async def urbandictionary(ctx, keyword=''):
    response = ''

    print(f'slang command used by { ctx.message.author } for keyword { keyword }')
    csv_writer.writerow([str(datetime.now()), 'hi', ctx.message.author, keyword])

    if keyword == '':
        response = 'You haven\'t entered a word, so showing the meaning of dumb\n'
        keyword = 'dumb'

    src = requests.get(f'https://www.urbandictionary.com/define.php?term={ keyword }')

    if src.status_code == 404:
        response += 'That word doesn\'t even exist Smarty Pants!'
    else:
        soup = BeautifulSoup(src.text, 'lxml')

        div = soup.find('div', class_='def-panel')
        meaning = div.find('div', class_='meaning').text
        example = div.find('div', class_='example').text

        response += f'**{ keyword }**\n{ meaning } \n\n**Example**: *{ example }*'

    await ctx.send(response)



bot.run(TOKEN)
csv_file.close()
