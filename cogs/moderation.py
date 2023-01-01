import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    #Deletes a certain number of messages from that channel where called in they are an admin
    @commands.command(pass_context=True, help='Deletes the number of messages besides the command', breif='Clears the number of messages')
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, number_of_msg):
        await ctx.channel.purge(limit=int(number_of_msg))
        await ctx.channel.send(content=f'{int(number_of_msg)} messages has been purged', delete_after=30)

    #error if the clear command fails
    @delete.error
    async def error_clear(self, ctx, error):
        await ctx.message.channel.send(error, delete_after=20)

def setup(bot):
    bot.add_cog(Moderation(bot))