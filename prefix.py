import json
import discord
from discord.ext import commands
async def get_prefix(bot, message):
    with open("data.json", 'r') as file:
        data = json.load(file)
        pre_fix = data['pre_fix']
        file.close()
    return(pre_fix)