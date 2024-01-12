import discord 
import os
import json
from discord.ext import commands 
from discord import app_commands
#from dotenv import load_dotenv

from prefix import get_prefix

#load_dotenv()
creator_id = int(os.getenv('owner_id'))
owner2_id = int(os.getenv('owner2_id'))
bot_chan = int(os.getenv('error_chan'))
app_id = int(os.getenv('app_id'))
my_guild = discord.Object(id=os.getenv('server_id'))

owner_ids = {creator_id, owner2_id}
TOKEN = os.getenv('Discord_token')
with open("data.json", 'r') as file:
    data = json.load(file)
    pre_fix = data['pre_fix']
    file.close()

def settings(prefix, owner_id):
    global bot
    intents = discord.Intents().all()
    bot = commands.Bot(command_prefix = commands.when_mentioned, owner_ids=owner_ids, intents=intents, application_id=app_id)

settings(get_prefix, owner_ids)
intents = discord.Intents().all()
bot = commands.Bot(command_prefix = commands.when_mentioned, owner_ids=owner_ids, intents=intents, application_id=app_id)
tree = bot.tree

bot.remove_command('help')

@tree.command(name="add", description="Adds the file to the cog files", guild=my_guild)
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(file_name="File to add")
async def add(ctx: discord.Interaction, file_name:str):
    try:
        bot.load_extension(f'cogs.{file_name}')
        await ctx.reply(f"{file_name} cog has been loaded", delete_after=5)
    except Exception as e:
        await ctx.reply(e)

@add.error
async def add_error(ctx:discord.Integration, e):
    await ctx.reply(e)

@tree.command(name="remove", description="Removes the file to the cog files", guild=my_guild)
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(file_name="File to remove")
async def remove(ctx:discord.Interaction, file_name:str):
    try:
        bot.unload_extension(f'cogs.{file_name}')
        await ctx.reply(f"{file_name} cog has been unloaded", delete_after=5)
    except Exception as e:
        await ctx.reply(e)

@remove.error
async def remove_error(ctx:discord.Interaction, e):
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

    #won't work need to alter to load commands different way
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')


bot.run(TOKEN)