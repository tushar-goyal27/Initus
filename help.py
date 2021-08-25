import discord
from discord.ext import commands

class HELP(commands.Cog):
    def __init__(self, bot, COMMAND_LOG):
        self.bot = bot

    @commands.command(name='help', brief='Shows this message')
    async def help(self, ctx, cmd=''):
        if cmd == '':
            response = ''
            for command in self.bot.commands:
                response += f'**{ command.name }:** { command.brief }\n\n'
            embed = discord.Embed(
                title = 'Initus Help',
                description = response,
                colour = discord.Color.blurple()
            )
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            await ctx.send(embed = embed)
            return

        for command in self.bot.commands:
            if cmd == command.name:
                params = ''
                for key, value in command.params.items():
                    if key not in ('self', 'ctx'):
                        params += f'<{ key }>'
                aliases = '|'.join(i for i in command.aliases)
                syntax = f'**{ cmd } { params }**' if aliases == '' else f'**{ cmd }|{ aliases } { params }**'
                embed = discord.Embed(
                    title = f'{ cmd } Help',
                    description = f'{ syntax }\n\n { command.brief }',
                    colour = discord.Color.from_rgb(0, 0, 0)
                )
                await ctx.send(embed = embed)
                return

        embed = discord.Embed(
            title = 'Command not found',
            description = f'Unknown command `{ cmd }`',
            color = discord.Color.from_rgb(255, 0, 0)
        )
        await ctx.send(embed = embed)
