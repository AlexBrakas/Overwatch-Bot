import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
import nacl #1.5.0
from random import randint, choice
from asyncio import sleep as sl
from os import listdir
from time import sleep

from main import bot_chan

'''
option_types:
    Sub_command: 1
    Sub_command_group: 2
    String: 3
    Integer: 4
    Boolean: 5
    User: 6
    Channel: 7
    Role: 8
    Mentionable: 9
    Float: 10
'''

"""
Follow command, follows an individual and just plays what ever command is ask over and over again <- fix this, doesn't work

"""

predicted = False
class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.vc = None
        self.repeat = False
        self.short = 100
        self.long = 4000
    
    @commands.Cog.listener()
    async def on_ready(self):
        global predicted
        await self.predict_check(self, predicted)

    @cog_ext.cog_slash(name="join")
    async def join(self, ctx:SlashContext):
        if not ctx.author.voice:
            await ctx.reply("You test my patience, join a vc")
        else:
            if self.vc != None:
                await ctx.reply("You test my patience")
            else:
                self.vc = await ctx.author.voice.channel.connect()
                await ctx.reply("Talk to the fist", delete_after=5)
    
    @cog_ext.cog_slash(name="conflict", description="Our Future Will Be Forged In Conflict", options=[
        create_option(
            name="repeat",
            description="Repeat?(Y/N)",
            required=False,
            option_type=3
        )])
    async def conflict(self, ctx:SlashContext, repeat:str="n"):
        if repeat.lower() == "y" or repeat.lower() == "yes":
            self.repeat = True
        try:
            if self.vc != None:
                await ctx.reply("Try me", delete_after=5)
                audio_scr = discord.FFmpegPCMAudio('characters_vc/Doomfist/Our_future_will_be_forged_in_conflict.mp3')
                self.vc.play(audio_scr)
                if self.repeat:
                    await self.timed_play('characters_vc/Doomfist/Our_future_will_be_forged_in_conflict.mp3')
            else:
                await ctx.reply("I know you can do better")
        except Exception as e:
            await ctx.reply("I find your lack of belief troubling", delete_after=10)
            await self.bot.get_channel(bot_chan).send(e)  
    
    @cog_ext.cog_slash(name="dip", description="You Dip Stick", options=[
        create_option(
            name="repeat",
            description="Repeat?(Y/N)",
            required=False,
            option_type=3
        )])
    async def dip(self, ctx:SlashContext, repeat:str="n"):
        if repeat.lower() == "y" or repeat.lower() == "yes":
            self.repeat = True
        try:
            if self.vc != None:
                await ctx.reply("Try me", delete_after=5)
                audio_scr = discord.FFmpegPCMAudio('characters_vc/Junkrat/you dip stick.mp3')
                self.vc.play(audio_scr)
                if self.repeat:
                    await self.timed_play('characters_vc/Junkrat/you dip stick.mp3')
            else:
                await ctx.reply("I know you can do better")
        except Exception as e:
            await ctx.reply("I find your lack of belief troubling", delete_after=10)
            await self.bot.get_channel(bot_chan).send(e)    

    @cog_ext.cog_slash(name="peanut", description="Did someone say peanut butter?", options=[
        create_option(
            name="repeat",
            description="Repeat?(Y/N)",
            required=False,
            option_type=3
        )])
    async def peanut(self, ctx:SlashContext, repeat:str="n"):
        if repeat.lower() == "y" or repeat.lower() == "yes":
            self.repeat = True
        try:
            if self.vc != None:
                await ctx.reply("Try me", delete_after=5)
                audio_scr = discord.FFmpegPCMAudio('characters_vc/Winston/Did_someone_say_peanut_butter.mp3')
                self.vc.play(audio_scr)
                if self.repeat:
                    await self.timed_play('characters_vc/Winston/Did_someone_say_peanut_butter.mp3')
            else:
                await ctx.reply("I know you can do better")
        except Exception as e:
            await ctx.reply("I find your lack of belief troubling", delete_after=10)
            await self.bot.get_channel(bot_chan).send(e)   
        
    @cog_ext.cog_slash(name="stop")
    async def stop(self, ctx:SlashContext):
        self.repeat = False
        await ctx.reply("Stopping :rolling_eyes:", delete_after=5)

    @cog_ext.cog_slash(name="leave")
    async def leave(self, ctx:SlashContext):
        if self.vc == None:
            await ctx.reply("You must be jokin, I am not in a vc", delete_after=10)
        else:
            await self.vc.disconnect()
            self.vc = None
            await ctx.reply("I am not your savior", delete_after=5)

    @cog_ext.cog_slash(name="min", description="The number of seconds the minium delay for the repeat")
    async def min(self, ctx:SlashContext, number:int):
        self.short = number
        await ctx.reply(f"The minium time between plays has been updated to {number}")

    @cog_ext.cog_slash(name="max", description="The number of seconds the maxium delay for the repeat")
    async def max(self, ctx:SlashContext, number:int):
        self.long = number
        await ctx.reply(f"The maxium time between plays has been updated to {number}")
    
    async def timed_play(self, audio):
        while self.vc != None and self.repeat:
            if not self.vc.is_playing():
                audio_scr = discord.FFmpegPCMAudio(audio)
                self.vc.play(audio_scr)
            await sl(randint(self.short, self.long))

    async def predict_check(self, pred):
        while True:
            if pred:
                self.play_char(pred)

    async def play_char(self, char):
        if self.vc.is_playing():
            self.vc.pause()
        chr_list=listdir(f"characters_vc/{char}")  
        chosen = choice(chr_list)
        self.vc.play(f"characters_vc/{char}/{chosen}")
        while self.vc.is_playing():
            sleep(0.5)
        self.vc.resume()
        global predicted
        predicted = False

def setup(bot: commands.bot):
    bot.add_cog(Slash(bot))