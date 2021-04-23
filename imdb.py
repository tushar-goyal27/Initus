import discord
from discord.ext import commands

import requests
from bs4 import BeautifulSoup
import string
from datetime import date, datetime

class IMDB(commands.Cog):
    def __init__(self, bot, COMMAND_LOG):
        self.bot = bot
        self.command_id = COMMAND_LOG
        self.enable = True

    def de_emojify(self, s):
        printable = set(string.printable)
        return ''.join(filter(lambda x: x in printable, str(s)))

    @commands.command(name='imdb', help='Type _imdb "tv show or movie" to get the info of the movie or show', aliases=['IMDB'])
    async def imdb(self, ctx, keyword=''):
        channel = self.bot.get_channel(int(self.command_id))
        await channel.send(f'imdb command used by { self.de_emojify(ctx.author) }  for keyword { keyword } in { ctx.channel }')

        if keyword == '':
            response = 'Try again, but this time with a name!'
            await ctx.reply(response)
            return

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
        embed.set_footer(text = f'Requested by: { self.de_emojify(ctx.author) }\n', icon_url = ctx.author.avatar_url)
        embed.timestamp = datetime.utcnow()

        await ctx.send(embed = embed)
