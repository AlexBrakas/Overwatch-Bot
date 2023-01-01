import discord #1.7.3
import os
import json
from discord.ext import commands #1.7.3
from discord_slash import SlashCommand, SlashContext #3.0.3
from discord_slash.utils.manage_commands import create_choice, create_option
#from dotenv import load_dotenv

from prefix import get_prefix

#load_dotenv()
creator_id = int(os.getenv('owner_id'))
aaron_id = int(os.getenv('aaron_id'))
bot_chan = int(os.getenv('error_chan'))

owner_id = {creator_id, aaron_id}
TOKEN = os.getenv('Discord_token')
with open("data.json", 'r') as file:
    data = json.load(file)
    pre_fix = data['pre_fix']
    file.close()

def settings(prefix, owner_id):
    global bot
    intents = discord.Intents().all()
    bot = commands.Bot(command_prefix = prefix, owner_ids=owner_id, intents=intents)

settings(get_prefix, owner_id)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

bot.remove_command('help')

@slash.slash(name="add_cog")
@commands.is_owner()
async def add(ctx:SlashContext, file_name):
    try:
        bot.load_extension(f'cogs.{file_name}')
        await ctx.reply(f"{file_name} cog has been loaded", delete_after=5)
    except Exception as e:
        await ctx.reply(e)

@add.error
async def add_error(ctx:SlashContext, e):
    await ctx.reply(e)

@slash.slash(name="remove_cog")
@commands.is_owner()
async def remove(ctx:SlashContext, file_name):
    try:
        bot.unload_extension(f'cogs.{file_name}')
        await ctx.reply(f"{file_name} cog has been unloaded", delete_after=5)
    except Exception as e:
        await ctx.reply(e)

@remove.error
async def remove_error(ctx:SlashContext, e):
    await ctx.reply(e)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

#waits till the bot is ready
@bot.event
async def on_ready():
    print('\nLogged in as ', end="")
    print(bot.user.name)
    print('------\n')

for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')


bot.run(TOKEN)