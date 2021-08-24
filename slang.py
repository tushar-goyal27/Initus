import discord
from discord.ext import commands

import requests
from bs4 import BeautifulSoup
import string
from datetime import date, datetime

class SLANG(commands.Cog):
    def __init__(self, bot, COMMAND_LOG):
        self.bot = bot
        self.channel = COMMAND_LOG

    def de_emojify(self, s):
        printable = set(string.printable)
        return ''.join(filter(lambda x: x in printable, str(s)))

    @commands.command(name='slang', brief='Gives the meaning of the slang from UrbanDictionary')
    @commands.cooldown(1, 40, commands.BucketType.channel)
    async def urbandictionary(self, ctx, *, keyword=''):
        await self.channel.send(f'slang command used by { self.de_emojify(ctx.author) }  for keyword { keyword } in { ctx.channel }')

        if keyword == '':
            # response = 'You haven\'t entered a word, so showing the meaning of dumb\n'
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
            meaning += '...'
        if len(example) > 1000:
            example = example[:950]

        embed = discord.Embed(
            title = keyword,
            description = f'{ meaning }\n\n**Example**: _{ example }_\n\n**Author:** { author }',
            colour = ctx.author.top_role.color
        )
        embed.set_footer(text = f'Requested by: { self.de_emojify(ctx.author) }\n', icon_url = ctx.author.avatar_url)
        embed.timestamp = datetime.utcnow()

        await ctx.send(embed = embed)
