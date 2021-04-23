import discord
from discord.ext import commands

import requests
from bs4 import BeautifulSoup
import string
from datetime import date, datetime

class MAL(commands.Cog):
    def __init__(self, bot, COMMAND_LOG, CHILL_LOUNGE):
        self.bot = bot
        self.command_id = COMMAND_LOG
        self.chill_lounge = CHILL_LOUNGE
        self.enable = True

    def de_emojify(self, s):
        printable = set(string.printable)
        return ''.join(filter(lambda x: x in printable, str(s)))

    @commands.command(name = 'mal', help='_mal "name of the anime" to get the info about the anime', aliases=['anime', 'MAL', 'ANIME'])
    async def mal(self, ctx, keyword = ''):
        if ctx.channel.id == int(self.chill_lounge):
            response = 'You can\'t use this command on this channel :('
            await ctx.reply(response)
            return

        channel = self.bot.get_channel(int(self.command_id))
        await channel.send(f'mal command used by { self.de_emojify(ctx.author) } for keyword { keyword } in { ctx.channel }')

        if keyword == '':
            response = 'Try again, but this time with a name!'
            await ctx.reply(response)
            return

        keyword = keyword.replace(' ', '%20')
        url = f'https://myanimelist.net/search/prefix.json?type=anime&keyword={ keyword }&v=1'

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
            response = 'Bonk! Go to Horny Jail or use this keyword in an NSFW channel!'
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
