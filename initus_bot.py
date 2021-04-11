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

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='_', intents = intents)
bot.add_cog(MAL(bot, COMMAND_LOG, CHILL_LOUNGE))

@bot.event
async def on_ready():
    guild = discord.utils.find(lambda s: s.id == int(GUILD_ID), bot.guilds)

    print(f'{bot.user} is connected\n')

    channel = bot.get_channel(int(CHANNEL))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'_help'))
    await channel.send('The Bot is online')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        response = f"Slow it down bro! Try again in { int(error.retry_after) }s."
        await ctx.reply(response)
    else:
        raise error

# hi command
@bot.command(name='hi', help="Says hi dumbo...")
async def greetings(ctx):
    channel = bot.get_channel(int(COMMAND_LOG))
    await channel.send(f'hi command used by { de_emojify(ctx.author) } in { ctx.channel } in { ctx.channel }')

    if str(ctx.author) == 'jayant Vashisth#6685':
        response = f'I don\'t say Hi to dumb people like you! { ctx.author.mention }'
    else:
        response = f'Hello { ctx.author.mention }'

    await ctx.send(response)

# news command
@bot.command(name='news', help="gets news")
async def news(ctx, keyword=''):
    channel = bot.get_channel(int(COMMAND_LOG))
    await channel.send(f'news command used by { de_emojify(ctx.author) }  for keyword { keyword } in { ctx.channel }')

    response = ''

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
@commands.cooldown(1, 60, commands.BucketType.user)
async def urbandictionary(ctx, keyword=''):
    channel = bot.get_channel(int(COMMAND_LOG))
    await channel.send(f'slang command used by { de_emojify(ctx.author) }  for keyword { keyword } in { ctx.channel }')

    if keyword == '':
        response = 'You haven\'t entered a word, so showing the meaning of dumb\n'
        keyword = 'dumb'

    src = requests.get(f'https://www.urbandictionary.com/define.php?term={ keyword }')

    if src.status_code == 404:
        response = 'That word doesn\'t even exist Smarty Pants!'
        await ctx.reply(response)
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

    embed = discord.Embed(
        title = keyword,
        description = f'{ meaning }\n\n**Example**: _{ example }_\n\n**Author:** { author }',
        colour = ctx.author.top_role.color
    )
    embed.set_footer(text = f'Requested by: { de_emojify(ctx.author) }\n', icon_url = ctx.author.avatar_url)
    embed.timestamp = datetime.utcnow()

    await ctx.send(embed = embed)

# imdb command
@bot.command(name='imdb', help='Type _imdb "tv show or movie" to get the info of the movie or show')
async def imdb(ctx, keyword=''):
    channel = bot.get_channel(int(COMMAND_LOG))
    await channel.send(f'imdb command used by { de_emojify(ctx.author) }  for keyword { keyword } in { ctx.channel }')

    keyword = keyword.replace(" ", "+")
    url = f"https://www.imdb.com/find?q={ keyword }"
    source = requests.get(url, timeout=20)
    soup = BeautifulSoup(source.text, 'lxml')
    td = soup.find('td', class_='result_text')

    if td == None:
        response = f'No such movie or tv show'
        await ctx.reply(response)
        return

    ttl = td.a['href']
    keyword = keyword.replace("+", " ")
    # Have reached the page of Title
    url = f"https://www.imdb.com{ttl}"
    source = requests.get(url, timeout=20)
    soup = BeautifulSoup(source.text, 'lxml')

    title = soup.find('div', class_='title_wrapper').h1.text.strip()
    title = title.replace('(', ' (')

    poster = soup.find('div', class_='poster')
    poster_link = poster.find('img')['src']

    subtext = soup.find('div', class_='subtext')

    if subtext == None:
        response = f'No such movie or tv show as { keyword }'
        await ctx.reply(response)
        return

    data = subtext.find_all('a')
    genre = data[:-1]
    genre = ', '.join([i.text for i in genre])

    release = data[-1].text.strip()
    time = subtext.find('time')
    if time:
        runtime = subtext.find('time').text.strip()
    else:
        runtime = 'ND'

    rating = soup.find('div', class_='ratingValue').text.strip()
    synopsis = soup.find('div', class_='summary_text').text.strip()

    slate = soup.find('div', class_='slate')
    trailer = slate.find('a')['href']
    trailer = f'https://www.imdb.com{ trailer }'

    embed = discord.Embed(
        title = title,
        description = f"""**Rating**: :star: { rating }\n
        **Genre**: { genre }\n
        **Release**: { release }\n
        **Runtime**: { runtime }\n
        **Synopsis**: { synopsis }\n
        **Trailer**: { trailer }\n
        For more info click [here]({ url })""",
        colour = ctx.author.top_role.color
    )

    embed.set_thumbnail(url = poster_link)
    embed.set_footer(text = f'Requested by: { de_emojify(ctx.author) }\n', icon_url = ctx.author.avatar_url)
    embed.timestamp = datetime.utcnow()

    await ctx.send(embed = embed)

@bot.command(name='link', help='Type _link Subject', aliases=['LINK', 'Link'])
async def link(ctx, keyword=''):

    channel = bot.get_channel(int(COMMAND_LOG))
    await channel.send(f'link command used by { de_emojify(ctx.author) }  for keyword { keyword } in { ctx.channel }')

    with open("links.json") as links_json:
        link_dict = json.load(links_json)
        if ctx.guild.id == int(GUILD_ID):
            keyword = keyword.upper()
            if keyword in link_dict:
                response = link_dict[keyword]
                await ctx.reply(response)
            else:
                response = 'No subject like this!\n\n**Available Subjects**\n'
                for key in link_dict.keys():
                    response += f'\n> { key }'
                embed = discord.Embed(
                    description = response,
                    colour = ctx.author.top_role.color
                )
                embed.set_footer(text = f'Requested by: { de_emojify(ctx.author) }\n', icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed)
        else:
            response = 'You don\'t have permission to use this command on this server!'
            await ctx.reply(response)

bot.run(TOKEN)
