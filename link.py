import discord
from discord.ext import commands
import json, string

class LINK(commands.Cog):
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.GUILD_ID = guild_id
        self.enable = True

    def de_emojify(self, s):
        printable = set(string.printable)
        return ''.join(filter(lambda x: x in printable, str(s)))

    @commands.command(name='link', help='Type _link Subject')
    async def link(self, ctx, keyword=''):

        with open("links.json") as links_json:
            link_dict = json.load(links_json)
            if ctx.guild.id == int(self.GUILD_ID):
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
                    embed.set_footer(text = f'Requested by: { self.de_emojify(ctx.author) }\n', icon_url = ctx.author.avatar_url)
                    await ctx.send(embed = embed)
            else:
                response = 'You don\'t have permission to use this command on this server!'
                await ctx.reply(response)
