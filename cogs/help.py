import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        

    @app_commands(name="help")
    async def help(self, ctx:discord.Interaction):
        cogs_desc = ''
        for cog in self.bot.cogs:
            cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'

        commands_desc = ''
        for command in self.bot.walk_commands():
            if not command.cog_name and not command.hidden:
                commands_desc += f'{command.name} - {command.help}\n'
    
        embed = discord.Embed(title="Commands", description="A list of the commands", color=discord.Color.green())
        embed.add_field(name = "Modules", value=cogs_desc, inline=False)
        if commands_desc:
            embed.add_field(name='Other Commands', value=commands_desc, inline=False)
        embed.set_footer(text=f"Requsted by{ctx.author.display_name}")
        await ctx.reply(embed=embed)

    #add slashes for each module

def setup(bot):
    bot.add_cog(Help(bot))