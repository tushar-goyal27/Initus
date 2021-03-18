import requests
import random
from bs4 import BeautifulSoup
import csv
from datetime import date, datetime

from dotenv import load_dotenv
import os

import discord
from discord.ext import commands

csv_file = open('commandLog.csv', 'a', newline="")
csv_writer = csv.writer(csv_file)

load_dotenv()

GUILD = os.getenv('GUILD_NAME')
TOKEN = os.getenv('DISCORD_TOKEN')
APIKEY = os.getenv('NEWS_API')
CHANNEL = os.getenv('CHANNEL_ID')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='_', intents = intents)

@bot.event
async def on_ready():
    guild = discord.utils.find(lambda s: s.name == GUILD, bot.guilds)

    print(f'{bot.user} is connected\n')

    print('Server members:')
    for member in guild.members:
        print(member.name)

    for channel in guild.channels:
        print(f'{ channel.name } { channel.id }')

    channel = bot.get_channel(int(CHANNEL))
    await channel.send('The Bot is online')

# hi command
@bot.command(name='hi', help="Says hi dumbo...")
async def greetings(ctx, name=''):
    print(f'hi command used by { ctx.message.author }')
    csv_writer.writerow([str(date.today()), str(datetime.now().time()), 'hi', ctx.message.author, 'None'])

    if str(ctx.message.author) == 'jayant Vashisth#6685':
        response = f'I don\'t say Hi to dumb people like you! { ctx.message.author.mention }'
    else:
        response = f'Hello { ctx.message.author.mention }'

    await ctx.send(response)

# news command
@bot.command(name='news', help="gets news")
async def news(ctx, keyword=''):
    response = ''

    print(f'news command used by { ctx.message.author }  for keyword { keyword }')
    csv_writer.writerow([str(date.today()), str(datetime.now().time()), 'news', ctx.message.author, keyword])

    if keyword == '':
        response = 'You haven\'t entered a topic, thus showing top news for India.'
        keyword = 'India'

    url = 'https://newsapi.org/v2/top-headlines'

    params = {
        'q': keyword,
        'apiKey': APIKEY
    }

    src = requests.get(url, params=params)
    articles = src.json()['articles']

    if len(articles) == 0:
        url = 'https://newsapi.org/v2/everything'
        src = requests.get(url, params=params)
        articles = src.json()['articles']

    if len(articles) == 0:
        response += f'Sorry no news for keyword { keyword }'
    else:
        i = random.randint(0, len(articles) - 1)
        article = articles[i]
        response += f"**{ article['title'] }** \n{ article['description'] } \n{ article['url'] }"

    await ctx.send(response)

# slang command
@bot.command(name='slang', help='Type _slang <word> to get the meaning of the slang')
async def urbandictionary(ctx, keyword=''):
    response = ''

    print(f'slang command used by { ctx.message.author } for keyword { keyword }')
    csv_writer.writerow([str(date.today()), str(datetime.now().time()), 'slang', ctx.message.author, keyword])

    if keyword == '':
        response = 'You haven\'t entered a word, so showing the meaning of dumb\n'
        keyword = 'dumb'

    src = requests.get(f'https://www.urbandictionary.com/define.php?term={ keyword }')

    if src.status_code == 404:
        response += 'That word doesn\'t even exist Smarty Pants!'
        await ctx.send(response)
        return
    else:
        soup = BeautifulSoup(src.text, 'lxml')

        div = soup.find('div', class_='def-panel')
        meaning = div.find('div', class_='meaning').text
        example = div.find('div', class_='example').text
        author = div.find('div', class_='contributor').text

    if len(meaning) > 1000:
        meaning = meaning[:950]
    if len(example) > 1000:
        example = example[:950]

    # response += f'**{ keyword }**\n{ meaning } \n\n**Example**: *{ example }*\n**Author**: { author }'

    embed = discord.Embed(
        title = keyword,
        description = f'{meaning}\n\n**Example**: _{example}_\n\n**Author:** {author}',
        colour = ctx.author.top_role.color
    )
    embed.set_footer(text = f'Requested by: {ctx.author}\n', icon_url = ctx.author.avatar_url)

    await ctx.send(embed = embed)

bot.run(TOKEN)
csv_file.close()
