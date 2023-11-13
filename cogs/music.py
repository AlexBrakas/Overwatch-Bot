import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
import nacl #1.5.0
from random import randint, choice
from asyncio import sleep as sl
from os import listdir
from time import sleep
from youtube_dl import YoutubeDL

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
Follow command, follows an individual and just plays what ever command is ask over and over again
Add now playing command
alias for commands
modulize more?
convert multiple voice lines to simplifed function that calls with just location passed to save space and easy expansion
add single para to FFmpeg to allow error catching, check if para is none (default pass) else reply
fix help
"""

predicted = False
class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.vc = None
        self.repeat = False
        self.short = 100
        self.long = 4000
        self.musicVolume = 0.3
        self.music_queue = []
        self.current = None
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    #@commands.Cog.listener()
    async def on_ready(self):
        global predicted
        await self.predict_check(predicted)

    @cog_ext.cog_slash(name="join", description="Joins the current voice channel that the member is in")
    async def join(self, ctx:SlashContext):
        if not ctx.author.voice:
            await ctx.reply("You test my patience, join a vc")
        else:
            if self.vc != None:
                await ctx.reply("You test my patience")
            else:
                self.vc = await ctx.author.voice.channel.connect()
                await ctx.reply("Talk to the fist", delete_after=5)
    
    async def char_voice_line(self, ctx:SlashContext, repeat, location):
        if repeat.lower() == "y" or repeat.lower() == "yes":
            self.repeat = True
        try:
            if self.vc != None:
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

    @cog_ext.cog_slash(name="conflict", description="Our Future Will Be Forged In Conflict", options=[
        create_option(
            name="repeat",
            description="Repeat?(Y/N)",
            required=False,
            option_type=3
        )])
    async def conflict(self, ctx:SlashContext, repeat:str="n"):
        location ='characters_vc/Doomfist/Our_future_will_be_forged_in_conflict.mp3'
        await self.char_voice_line(ctx, repeat, location)
    
    @cog_ext.cog_slash(name="dip", description="You Dip Stick", options=[
        create_option(
            name="repeat",
            description="Repeat?(Y/N)",
            required=False,
            option_type=3
        )])
    async def dip(self, ctx:SlashContext, repeat:str="n"):
        location = 'characters_vc/Junkrat/you dip stick.mp3'
        await self.char_voice_line(ctx, repeat, location)  

    @cog_ext.cog_slash(name="peanut", description="Did someone say peanut butter?", options=[
        create_option(
            name="repeat",
            description="Repeat?(Y/N)",
            required=False,
            option_type=3
        )])
    async def peanut(self, ctx:SlashContext, repeat:str="n"):
        location = 'characters_vc/Winston/Did_someone_say_peanut_butter.mp3'
        await self.char_voice_line(ctx, repeat, location)
        
    @cog_ext.cog_slash(name="stop", description="stops the repeats and will stop the current music or voice lines")
    async def stop(self, ctx:SlashContext):
        self.repeat = False
        self.vc.stop()
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
    
    @cog_ext.cog_slash(name="vol", description="Sets the music volume", options=[
        create_option(
            name="volume",
            description="The number you want the volume to be set to",
            option_type=4,
            required=True
            )])
    async def vol(self, ctx:SlashContext, volume:int):
        self.musicVolume = volume/100
        if self.vc != None:
            self.vc.pause()
            self.vc.resume()
        await ctx.reply(f"Music Volume has been set to {volume}", delete_after=25)

    async def timed_play(self, audio):
        while self.vc != None and self.repeat:
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
        global predicted
        predicted = False


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

    @cog_ext.cog_slash(name="play", description="Resumes the music or adds a new song", options=[
        create_option(
            name="song",
            description="Name or link of song",
            required=False,
            option_type=3
        )])
    async def play(self, ctx:SlashContext, song:str=None):
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

    @cog_ext.cog_slash(name="pause", description="Pauses the current song/voice line that is playing")
    async def pause(self, ctx:SlashContext):
        try:
            if self.vc.is_playing():
                self.vc.pause()
                await ctx.reply("Paused", delete_after=15)
            else:
                raise Exception("The bot is currently not playing anything")
        except Exception as e:
            await ctx.reply(e, delete_after=5)
            await self.bot.get_channel(bot_chan).send(e)

    @cog_ext.cog_slash(name="skip", description="skips the current track")
    async def skip(self, ctx:SlashContext):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)
            await ctx.reply("Skipped", delete_after=10)

    @cog_ext.cog_slash(name="playing", description="Current song playing")
    async def playing(self, ctx:SlashContext):
        if self.vc.is_playing():
            await ctx.reply(f"Currently playing: {self.current}", delete_after=15)

    @cog_ext.cog_slash(name="queue", description="Displays queue of songs")
    async def queue(self, ctx):
        retval = "Currently playing: "+self.current+"\n"
        for i in range(0, len(self.music_queue)):
            if (i > 9): break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.reply(retval, delete_afer=20)
        else:
            await ctx.reply("No music in queue", delete_after=10)

    @cog_ext.cog_slash(name="clear", description="abliterates the queue")
    async def clear(self, ctx):
        if self.vc != None and self.vc.is_playing():
            self.vc.stop()
        self.music_queue = []
        await ctx.reply("Music queue cleared", delete_after=10)

def setup(bot: commands.bot):
    bot.add_cog(Music(bot))