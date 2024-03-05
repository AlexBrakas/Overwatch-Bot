import discord
from discord.ext import commands
from discord import app_commands
import nacl #1.5.0
from random import randint, choice
from asyncio import sleep as sl
from os import listdir
from time import sleep
from youtube_dl import YoutubeDL
from typing import Literal

from main import bot_chan

"""
Follow command, follows an individual and just plays what ever command is ask over and over again
Add now playing command
alias for commands
modulize more?
convert multiple voice lines to simplifed function that calls with just location passed to save space and easy expansion
add single para to FFmpeg to allow error catching, check if para is none (default pass) else reply
fix help
"""

class Music(commands.GroupCog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.vc = discord.VoiceClient()
        self.predicted = False
        self.repeat = False
        self.short = 100
        self.long = 4000
        self.musicVolume = 0.3
        self.music_queue = []
        self.current = None
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    #@commands.Cog.listener()
    async def on_ready(self):
        await self.predict_check(self.predicted)

    @app_commands.command(name="join", description="Bot Joins the VC")
    async def join(self, ctx:discord.Interaction):
        if not ctx.author.voice:
            await ctx.reply("You test my patience, join a vc")
        else:
            if self.vc.is_connected():
                await ctx.reply("You test my patience")
            else:
                self.vc = await ctx.author.voice.channel.connect()
                await ctx.reply("Talk to the fist", delete_after=5)
    
    async def char_voice_line(self, ctx:discord.Interaction, repeat, location):
        if repeat.lower() == "y" or repeat.lower() == "yes":
            self.repeat = True
        try:
            if self.vc.is_connected():
                await ctx.reply("Try me", delete_after=5)
                self.vc.pause()
                audio_scr = discord.FFmpegPCMAudio(location)
                self.vc.play(audio_scr)
                if self.repeat:
                    await self.timed_play(location)
                #self.vc.resume()
            else:
                await ctx.reply("I know you can do better")
        except Exception as e:
            await ctx.reply("I find your lack of belief troubling", delete_after=10)
            await self.bot.get_channel(bot_chan).send(e)

    @app_commands.command(name="conflict", description="Our Future Will Be Forged In Conflict")
    @app_commands.describe(repeat="Repeat the line?")
    async def conflict(self, ctx:discord.Interaction, repeat:Literal['y','n']="n"):
        location ='characters_vc/Doomfist/Our_future_will_be_forged_in_conflict.mp3'
        await self.char_voice_line(ctx, repeat, location)
    
    @app_commands.command(name="dip", description="You Dip Stick")
    @app_commands.describe(repeat="Repeat the line?")
    async def dip(self, ctx:discord.Interaction, repeat:Literal['y','n']="n"):
        location = 'characters_vc/Junkrat/you dip stick.mp3'
        await self.char_voice_line(ctx, repeat, location)  

    @app_commands.command(name="peanut", description="Did someone say peanut butter?")
    @app_commands.describe(repeat="Repeat the line?")
    async def peanut(self, ctx:discord.Interaction, repeat:Literal['y','n']="n"):
        location = 'characters_vc/Winston/Did_someone_say_peanut_butter.mp3'
        await self.char_voice_line(ctx, repeat, location)
        
    @app_commands.command(name="stop", description="stops the repeats and will stop the current music or voice lines")
    async def stop(self, ctx:discord.Interaction):
        self.repeat = False
        self.vc.stop()
        await ctx.reply("Stopping :rolling_eyes:", delete_after=5)

    @app_commands.command(name="leave")
    async def leave(self, ctx:discord.Interaction):
        if self.bot.is_connected():
            await self.vc.disconnect()
            self.vc = discord.VoiceClient()
            await ctx.reply("I am not your savior", delete_after=5)
        else:
            await ctx.reply("You must be jokin, I am not in a vc", delete_after=10)

    @app_commands.command(name="min", description="The number of seconds the minium delay for the repeat")
    @app_commands.describe(number="Number of seconds")
    async def min(self, ctx:discord.Interaction, number:int):
        self.short = number
        await ctx.reply(f"The minium time between plays has been updated to {number}")

    @app_commands.command(name="max", description="The number of seconds the maxium delay for the repeat")
    @app_commands.command(number="Number of seconds")
    async def max(self, ctx:discord.Interaction, number:int):
        self.long = number
        await ctx.reply(f"The maxium time between plays has been updated to {number}")
    
    @app_commands.command(name="vol", description="Sets the music volume")
    @app_commands.describe(volume='Volume')
    async def vol(self, ctx:discord.Interaction, volume:int):
        self.musicVolume = volume/100
        if self.vc.is_connected():
            self.vc.pause()
            self.vc.resume()
        await ctx.reply(f"Music Volume has been set to {volume}", delete_after=25)

    async def timed_play(self, audio):
        while self.vc.is_connected() and self.repeat:
            if not self.vc.is_playing():
                audio_scr = discord.FFmpegPCMAudio(audio)
                self.vc.play(audio_scr)
            await sl(randint(self.short, self.long))

    async def predict_check(self, pred):
        #while True:
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
        self.predicted = False


    async def youtube_search(self, item):
        with YoutubeDL({'format': 'bestaudio', 'audioformat':'mp3'}) as ydl:
            try:
                info_raw = ydl.extract_info("ytsearch:%s" % item, download=False)
                if 'playlist' in item:
                    play_list = ydl.extract_info(info_raw['id'], download=False)
                    info = list()
                    for item in play_list['entries']:
                        info.append({'source': item['formats'][0]['url'], 'title': item['title']})
                    return info

                else:
                    info = info_raw['entries'][0]
                    return [{'source': info['formats'][0]['url'], 'title': info['title']}]
            except Exception as e: 
                return False

    def play_next(self, error=None):
        if error == None:
            if len(self.music_queue) > 0:
                music_url = self.music_queue[0][0]['source']
                self.current = self.music_queue.pop(0)[0]['title']
                self.vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(music_url, **self.FFMPEG_OPTIONS), self.musicVolume), after=self.play_next)
            else:
                self.current = None
        else:
            self.bot.get_channel(bot_chan).send(error)
    
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            music_url = self.music_queue[0][0]['source']
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
                if self.vc == None:
                    await ctx.send("I am not in the vc")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            self.current = self.music_queue.pop(0)[0]['title']
            self.vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(music_url, **self.FFMPEG_OPTIONS), self.musicVolume), after=self.play_next)
        else:
            self.current = None

    @app_commands.command(name="play", description="Resumes the music or adds a new song")
    @app_commands.describe(song="Name or link of song")
    async def play(self, ctx:discord.Interaction, song:str=None):
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.reply("Connect to a voice channel!", delete_after=15)
        elif self.vc.is_paused():
            self.vc.resume()
            await ctx.reply("playing", delete_after=15)
        elif song == None:
            await ctx.reply("Please pass a song that you wish to play", delete_after=10)
        else:
            await ctx.reply("Trying to download", delete_after=20)
            chan = ctx.channel
            song_list = await self.youtube_search(song)
            if type(song_list) == type(True):
                await chan.send("Song could not be download", delete_after=15)
            else:
                if type(song_list) == type(None):
                    await chan.send("An error has occured", delete_after=10)
                else:
                    for song in song_list:
                        await chan.send(f"{song['title']} added to the queue", delete_after=15)
                        self.music_queue.append([song, voice_channel])
                
                if self.vc.is_playing() == False and self.current == None:
                    await self.play_music(ctx)

    @app_commands.command(name="pause", description="Pauses the current song/voice line that is playing")
    async def pause(self, ctx:discord.Interaction):
        try:
            if self.vc.is_playing():
                self.vc.pause()
                await ctx.reply("Paused", delete_after=15)
            else:
                raise Exception("The bot is currently not playing anything")
        except Exception as e:
            await ctx.reply(e, delete_after=5)
            await self.bot.get_channel(bot_chan).send(e)

    @app_commands.command(name="skip", description="skips the current track")
    async def skip(self, ctx:discord.Interaction):
        if self.vc.is_connected() and self.vc:
            self.vc.stop()
            await self.play_music(ctx)
            await ctx.reply("Skipped", delete_after=10)

    @app_commands.command(name="playing", description="Current song playing")
    async def playing(self, ctx:discord.Interaction):
        if self.vc.is_playing():
            await ctx.reply(f"Currently playing: {self.current}", delete_after=15)

    @app_commands.command(name="queue", description="Displays queue of songs")
    async def queue(self, ctx):
        retval = "Currently playing: "+self.current+"\n"
        for i in range(0, len(self.music_queue)):
            if (i > 9): break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.reply(retval, delete_afer=20)
        else:
            await ctx.reply("No music in queue", delete_after=10)

    @app_commands.command(name="clear", description="abliterates the queue")
    async def clear(self, ctx):
        if self.vc.is_connected() and self.vc.is_playing():
            self.vc.stop()
        self.music_queue = []
        await ctx.reply("Music queue cleared", delete_after=10)

def setup(bot: commands.bot):
    bot.add_cog(Music(bot))