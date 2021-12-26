import string
from datetime import date, datetime

import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup


class MAL(commands.Cog):
    def __init__(self, bot, COMMAND_LOG, CHILL_LOUNGE):
        self.bot = bot
        self.channel = COMMAND_LOG
        self.chill_lounge = CHILL_LOUNGE
        self.enable = True

    def de_emojify(self, s):
        printable = set(string.printable)
        return ''.join(filter(lambda x: x in printable, str(s)))

    @commands.command(name='anime', brief='Gets the info of the anime from myanimelist', aliases=['mal'])
    async def anime(self, ctx, *, anime_name = ''):
        if ctx.channel == self.chill_lounge:
            response = 'You can\'t use this command on this channel :('
            await ctx.reply(response)
            return

        await self.channel.send(f'mal command used by { self.de_emojify(ctx.author) } for anime_name { anime_name } in { ctx.channel }')

        if anime_name == '':
            response = 'Try again, but this time with a name!'
            await ctx.reply(response)
            return

        anime_name = anime_name.replace(' ', '%20')
        url = f'https://myanimelist.net/search/prefix.json?type=anime&keyword={ anime_name }&v=1'

        src = requests.get(url)

        data = src.json()
        try:
            top_result = data['categories'][0]['items'][0]

            anime_data = {}

            anime_data['name'] = top_result['name']
            anime_data['status'] = top_result['payload']['status']
            anime_data['score'] = top_result['payload']['score']
            anime_data['aired'] = top_result['payload']['aired']
            url = top_result['url']

            src = requests.get(url)
            soup = BeautifulSoup(src.content, 'lxml')

            anime_data['rank'] = soup.find('span', class_='numbers ranked').strong.text[1:]
            anime_data['popularity'] = soup.find('span', class_='numbers popularity').strong.text[1:]

            anime_data['eng-ttl'] = soup.find('div', class_='spaceit_pad').text[10:-3]
            anime_data['synopsis'] = soup.find('p', itemprop='description').text[:500].replace('\n', '')
            anime_data['img_url'] = soup.find('img', alt = anime_data['name'])['data-src']
            anime_data['genre'] = ', '.join(x.text for x in soup.find_all('span', itemprop='genre'))
        except:
            response = 'This anime doesn\'t exist! :('
            await ctx.reply(response)
            return

        if 'Hentai' in anime_data['genre'] and not ctx.channel.is_nsfw():
            response = 'Bonk! Go to Horny Jail or use this anime_name in an NSFW channel!'
            await ctx.reply(response)
            return

        embed = discord.Embed(
            title = anime_data['name'],
            description = f"""
            **English title**: { anime_data['eng-ttl'] }\n
            **MAL Score**: { anime_data['score'] }\n
            **Rank**: #{ anime_data['rank'] }
            **Popularity**: #{ anime_data['popularity'] }\n
            **Aired**: { anime_data['aired'] }
            **Status**: { anime_data['status'] }\n
            **Genre**: { anime_data['genre'] }\n
            **Synopsis**: { anime_data['synopsis'] }[[...]]({ url })\n""",
            colour = ctx.author.top_role.color
        )

        embed.set_image(url = anime_data['img_url'])
        embed.set_footer(text = f'Requested by: { self.de_emojify(ctx.author) }\n', icon_url = ctx.author.avatar_url)
        embed.timestamp = datetime.utcnow()

        await ctx.send(embed = embed)

    @commands.command(name = 'manga', brief='Gets the info of the manga from myanimelist', case_insensitive=True)
    async def manga(self, ctx, *, manga_name = ''):
        if ctx.channel == self.chill_lounge:
            response = 'You can\'t use this command on this channel :('
            await ctx.reply(response)
            return

        await self.channel.send(f'manga command used by { self.de_emojify(ctx.author) } for manga_name { manga_name } in { ctx.channel }')

        if manga_name == '':
            response = 'Try again, but this time with a name!'
            await ctx.reply(response)
            return

        manga_name = manga_name.replace(' ', '%20')
        url = f'https://myanimelist.net/search/prefix.json?type=manga&keyword={ manga_name }&v=1'

        src = requests.get(url)

        data = src.json()
        try:
            top_result = data['categories'][0]['items'][0]

            anime_data = {}

            anime_data['name'] = top_result['name']
            anime_data['status'] = top_result['payload']['status']
            anime_data['score'] = top_result['payload']['score']
            anime_data['published'] = top_result['payload']['published']
            url = top_result['url']

            src = requests.get(url)
            soup = BeautifulSoup(src.content, 'lxml')

            anime_data['rank'] = soup.find('span', class_='numbers ranked').strong.text[1:]
            anime_data['popularity'] = soup.find('span', class_='numbers popularity').strong.text[1:]

            anime_data['eng-ttl'] = soup.find('div', class_='spaceit_pad').text[9:]
            anime_data['synopsis'] = soup.find('span', itemprop='description').text[:500].replace('\n', '')
            anime_data['img_url'] = soup.find('img', alt = anime_data['name'])['data-src']
            anime_data['genre'] = ', '.join(x.text for x in soup.find_all('span', itemprop='genre'))
        except:
            response = 'This manga doesn\'t exist! :('
            await ctx.reply(response)
            return

        if 'Hentai' in anime_data['genre'] and not ctx.channel.is_nsfw():
            response = 'Bonk! Go to Horny Jail or use this manga_name in an NSFW channel!'
            await ctx.reply(response)
            return

        embed = discord.Embed(
            title = anime_data['name'],
            description = f"""
            **English title**: { anime_data['eng-ttl'] }\n
            **MAL Score**: { anime_data['score'] }\n
            **Rank**: #{ anime_data['rank'] }
            **Popularity**: #{ anime_data['popularity'] }\n
            **Published**: { anime_data['published'] }
            **Status**: { anime_data['status'] }\n
            **Genre**: { anime_data['genre'] }\n
            **Synopsis**: { anime_data['synopsis'] }[[...]]({ url })\n""",
            colour = ctx.author.top_role.color
        )

        embed.set_image(url = anime_data['img_url'])
        embed.set_footer(text = f'Requested by: { self.de_emojify(ctx.author) }\n', icon_url = ctx.author.avatar_url)
        embed.timestamp = datetime.utcnow()

        await ctx.send(embed = embed)
