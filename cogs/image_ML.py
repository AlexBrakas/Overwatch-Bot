import discord #1.7.3
from discord.ext import commands
from discord_slash import SlashContext, cog_ext #3.0.3
import tensorflow as tf #2.11.0
import numpy as np #1.21.6
from PIL import Image #9.3.0
from tensorflow import keras 
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import pathlib
import matplotlib as plt #3.5.3
import requests
import shutil
import os

"""
Make the recongize the character by an image and play a voice line from them (folder the audio files)
make the bot learn how to speak as each one and talk on it own (make it's own voice lines)

reaction on image gives away who it is for saving and training purposes
command to retrain the model at any given point

tf.io.decode_gif(
    contents, name=None
)
"""


class MLImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def file_save(self, attach_url, char, ext):
        file = requests.get(attach_url, allow_redirects=True, stream=True)
        file_name = char+str(len(os.listdir(f"characters_img/{char}")))+ext
        file_loc = f"characters_img/{char}/{file_name}"
        with open(file_loc, "wb") as out_file:
            print("Saving file: " +file_name)
            shutil.copyfileobj(file.raw, out_file)
        im = Image.open(file_loc)
        im.thumbnail((500,500))
        im.save(file_loc)
    
    async def set_up_char(self, ctx, char):
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if message.attachments:
            attach_url = message.attachments[0].url
            if "jpg" in attach_url:
                ext = ".jpg"
                self.file_save(attach_url, char, ext)

            elif "png" in attach_url: #convert to jpg
                ext = ".png"
                self.file_save(attach_url, char, ext)

            elif "mp4" in attach_url: #convert tp jpg
                await ctx.send("Video format is not supported at this time")
            
            elif "gif" in attach_url: #conver jpg
                await ctx.send("GIF format is not suppored at this time")

            else:
                await ctx.send("Whatever format you just tried is not allowed")

        elif not message.attachments:
            await ctx.send("This message does not have an attachment")

    @commands.command(pass_context=True, hidden=True)
    async def junkrat(self, ctx):
        if ctx.author.id != 305412029336911872:
            return
        char = "Junkrat"
        await self.set_up_char(ctx, char)
        

    @commands.command(pass_context=True, hidden=True)
    async def doomfist(self, ctx):
        if ctx.author.id != 305412029336911872:
            return
        char = "Doomfist"
        await self.set_up_char(ctx, char)

    @commands.command(pass_context=True, hidden=True)
    async def winston(self, ctx):
        if ctx.author.id != 305412029336911872:
            return
        char = "Winston"
        await self.set_up_char(ctx, char)


def setup(bot):
    bot.add_cog(MLImage(bot))
