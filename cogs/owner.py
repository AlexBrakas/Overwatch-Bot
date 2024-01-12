import discord
from discord.ext import commands
from discord import app_commands
import json
from prefix import get_prefix

class Owner(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @commands.command(pass_context=True, help="Allows the bots owners to backup the flag's languages for safe keeping", breif="Backups flag's languages")
    @commands.is_owner()
    async def backup(self, ctx:commands.Context):
        with open('flags.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            file.close()
        with open('backup_flags.json', 'w+', encoding='utf-8') as file:
            json.dump(data, file, indent=1)
            file.close()
        await ctx.message.channel.send(f"The flags have been backed up")

    @commands.command(pass_context=True, help="Allows the owner to update key bot data like prefix and bot channel log location", breif="Changes key bot data")
    @commands.is_owner()
    async def update_data(self, ctx:commands.Context, first_part, second_part):
        with open("data.json", 'r+') as file:
            data = json.load(file)
            file.close()
        if first_part.lower() == "pre_fix" or first_part.lower() == "prefix":
            data['pre_fix'] = second_part
        elif first_part.lower() == "bot" or first_part.lower() == "botchannel":
            if second_part.lower() == "here" or second_part.lower() == "this":
                second_part = ctx.message.channel.id
            data['bot_channel'] = int(second_part)
        with open("data.json", 'w') as file:
            json.dump(data, file, indent = 1)
            file.close()
        await ctx.message.channel.send(f"The bot's has updated {first_part} to {second_part}")

    @update_data.error
    async def error_update_data(self, ctx:commands.Context, error):
        await ctx.message.channel.send(error)

    @app_commands.command(name="info", description="Gives information about the bot")
    async def info(self, ctx:discord.Interaction):
        await ctx.reply(f"This bot was developed by Alex Brakas\nDiscord tag: Cyepher\nMore information on GitHub about the bot")


def setup(bot):
    bot.add_cog(Owner(bot))