#bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import asyncio
import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='s!')
client = discord.Client()

bot.last_song = ""

#Says a message when a new member enters the discord
@bot.event
async def on_ready():
    print(bot.user.name + ' has connected to Discord!')


bot.playlist_counter = 0
bot.musicList = None
bot.currentVC = None
bot.currentSong = "None"
bot.currentList = "memeful/"


#Tuesday at 12:00 pm
bot.reginaldTime = "12:00"
bot.reginaldDay = 1
bot.reginaldBool = True


"""

    Music

"""
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  

    
    #Picks a song from the playlist and plays it
    @commands.command(name='songMeme', help='Play a random song from the playlist')
    async def songMeme(self, ctx):
        if (bot.currentVC == None or not bot.currentVC.is_playing()):
            user = ctx.message.author
            userVC = user.voice.channel

            if userVC != None:
                channelName = userVC.name
                voiceChannel = discord.utils.get(ctx.guild.channels, name=channelName)
                bot.currentVC = await voiceChannel.connect()

                randomChoice = random.choice(os.listdir('./media/mp3/playlist/memeful/'))
                randomSong = './media/mp3/playlist/memeful/' + randomChoice
                
                bot.musicList = [randomChoice]
                bot.playlist_counter = 1

                def my_after(error):
                    bot.currentSong = "None"
                    coro = bot.currentVC.disconnect()
                    fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
                    try:
                        fut.result()
                    except:
                        # an error happened sending the message
                        pass    

                bot.currentList = "memeful/"

                bot.currentSong = bot.musicList[0]
                bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
        else:
            await playingMessage(ctx)


    #Picks songs from the playlist and plays them
    @commands.command(name='playlistMeme', help='Shuffles songs from the playlist')
    async def songsMeme(self, ctx):
        if (bot.currentVC == None or not bot.currentVC.is_playing()):
            user = ctx.message.author
            userVC = user.voice.channel

            if userVC != None:
                channelName = userVC.name
                voiceChannel = discord.utils.get(ctx.guild.channels, name=channelName)
                bot.currentVC = await voiceChannel.connect()


                bot.musicList = os.listdir('./media/mp3/playlist/memeful/')
                random.shuffle(bot.musicList)

                randomSong = './media/mp3/playlist/memeful/' + bot.musicList[0]
            
                bot.playlist_counter = 1



                def my_after(error):
                    if (bot.musicList[bot.playlist_counter] != None and not bot.currentVC.is_playing() and bot.currentVC.is_connected()):
                        if bot.playlist_counter >= len(bot.musicList):
                            server = ctx.message.guild.voice_client
                            server.disconnect()
                            bot.currentSong = "None"
                        else:
                            randomSong = './media/mp3/playlist/memeful/' + bot.musicList[bot.playlist_counter]
                            bot.currentSong = bot.musicList[bot.playlist_counter]
                            bot.playlist_counter = bot.playlist_counter + 1
                            bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
                    
                bot.currentList = "memeful/"
                
                bot.currentSong = bot.musicList[0]
                bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
        else:
            await playingMessage(ctx)

    #Picks a song from the playlist and plays it
    @commands.command(name='song', help='Play a random song from the playlist without memes')
    async def song(self, ctx):
        if (bot.currentVC == None or not bot.currentVC.is_playing()):
            user = ctx.message.author
            userVC = user.voice.channel

            if userVC != None:
                channelName = userVC.name
                voiceChannel = discord.utils.get(ctx.guild.channels, name=channelName)
                bot.currentVC = await voiceChannel.connect()

                randomChoice = random.choice(os.listdir('./media/mp3/playlist/memeless/'))
                randomSong = './media/mp3/playlist/memeless/' + randomChoice
                
                bot.musicList = [randomChoice]
                bot.playlist_counter = 1

                def my_after(error):
                    bot.currentSong = "None"
                    coro = bot.currentVC.disconnect()
                    fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
                    try:
                        fut.result()
                    except:
                        # an error happened sending the message
                        pass    

                bot.currentList = "memeless/"

                bot.currentSong = bot.musicList[0]
                bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
        else:
            await playingMessage(ctx)


    #Picks songs from the playlist and plays them
    @commands.command(name='playlist', help='Shuffles songs from the playlist without memes')
    async def songs(self, ctx):
        if (bot.currentVC == None or not bot.currentVC.is_playing()):
            user = ctx.message.author
            userVC = user.voice.channel

            if userVC != None:
                channelName = userVC.name
                voiceChannel = discord.utils.get(ctx.guild.channels, name=channelName)
                bot.currentVC = await voiceChannel.connect()


                bot.musicList = os.listdir('./media/mp3/playlist/memeless/')
                random.shuffle(bot.musicList)

                randomSong = './media/mp3/playlist/memeless/' + bot.musicList[0]
            
                bot.playlist_counter = 1



                def my_after(error):
                    if (bot.musicList[bot.playlist_counter] != None and not bot.currentVC.is_playing() and bot.currentVC.is_connected()):
                        if bot.playlist_counter >= len(bot.musicList):
                            server = ctx.message.guild.voice_client
                            server.disconnect()
                            bot.currentSong = "None"
                        else:
                            randomSong = './media/mp3/playlist/memeful/' + bot.musicList[bot.playlist_counter]
                            bot.currentSong = bot.musicList[bot.playlist_counter]
                            bot.playlist_counter = bot.playlist_counter + 1
                            bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
                    
                bot.currentList = "memeless/"
                
                bot.currentSong = bot.musicList[0]
                bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
        else:
            await playingMessage(ctx)


    #Skips currently played song
    @commands.command(name='skip', help='Skips currently played song')
    async def skip(self, ctx):
        def my_after(error):
                if (bot.musicList[bot.playlist_counter] != None and not bot.currentVC.is_playing() and bot.currentVC.is_connected()):
                    randomSong = './media/mp3/playlist/' + bot.currentList + bot.musicList[bot.playlist_counter]
                    bot.currentSong = bot.musicList[bot.playlist_counter]
                    bot.playlist_counter = bot.playlist_counter + 1
                    bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)

        if (bot.currentVC.is_playing() and bot.currentVC.is_connected()):
            if (bot.playlist_counter >= len(bot.musicList)):
                server = ctx.message.guild.voice_client
                await server.disconnect()
                bot.currentSong = "None"
            else:
                randomSong = './media/mp3/playlist/' + bot.currentList + bot.musicList[bot.playlist_counter]
                bot.currentSong = bot.musicList[bot.playlist_counter]
                bot.playlist_counter = bot.playlist_counter + 1

                bot.currentVC.stop()
                bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
            
    """
    def getMusicList(self):
        musicList = os.listdir('./media/mp3/playlist/')
        random.shuffle(musicList)

        return musicList
    """

    #Explains what songs is currently playing
    @commands.command(name="playing", help="Tells what song is currently playing")
    async def playing(self, ctx):
        response = "The song: \'" + bot.currentSong + "\' is currently playing"
        await ctx.send(response)


    #Disconnects Bot from Voice Chat
    @commands.command(name='stop', help='Stops music or clips from being played in voice', pass_context=True)
    async def stop(self, ctx):
        server = ctx.message.guild.voice_client
        await server.disconnect()
        bot.currentSong = "None"


"""

    Everyday Classics

"""
class EverydayClassics(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot  

    #Cancels Someone (Probably Drew)
    @commands.command(name='cancel', help='Use this to cancel someone!')
    async def cancelDrew(self, ctx):
        randomUserId = random.choice(ctx.message.guild.members).id

        ran = random.choice(range(10))

        if (ran < 2):
            randomUserId = 159433180036726784

        randomUser = bot.get_user(randomUserId).display_name
        response = randomUser + " is cancelled"
        await ctx.send(response)


    #Posts the Goodnight Video
    @commands.command(name='goodnight', help='Say goodnight to all your friends')
    async def goodnight(self, ctx):
        area = ctx.message.channel
        await ctx.send(file=discord.File('./media/mp4/goodnight.mp4'))


    #Posts a random Classic Meme
    @commands.command(name='meme', help='Pull a classic meme from the archives')
    async def classicMeme(self, ctx):
        randomMeme = './media/classicMemes/' + random.choice(os.listdir('./media/classicMemes/'))
        await ctx.send(file=discord.File(randomMeme))


    #Posts the appropriate meme for the day
    @commands.command(name='dailyMeme', help='Posts the appropriate meme for the day')
    async def dailyMeme(self, ctx):
        day = datetime.date.today().weekday()
        dayMeme = ""

        if (day == 0):
            dayMeme = 'monday.mp4'
        elif(day == 1):
            dayMeme = 'tuesday.mp4'
        elif(day == 2):
            dayMeme = 'wednesday.mp4'
        elif(day == 3):
            dayMeme = 'thursday.mp4'
        elif(day == 4):
            dayMeme = 'friday.mp4'
        elif(day == 5):
            dayMeme = 'saturday.mp4'
        elif(day == 6):
            dayMeme = 'sunday.mp4'

        dayMeme = './media/dayMemes/' + dayMeme
        await ctx.send(file=discord.File(dayMeme)) 


"""

    Miscellaneous

"""
class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Picks a seven dollars clip and plays it
    @commands.command(name='7', help='Seven Dollars')
    async def sevenDollars(self, ctx):
        if (bot.currentVC == None or not bot.currentVC.is_playing()):
            user = ctx.message.author
            userVC = user.voice.channel

            if userVC != None:
                channelName = userVC.name
                voiceChannel = discord.utils.get(ctx.guild.channels, name=channelName)
                bot.currentVC = await voiceChannel.connect()

                randomSong = './media/mp3/shane/' + random.choice(os.listdir('./media/mp3/shane/'))

                def my_after(error):
                    coro = bot.currentVC.disconnect()
                    fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
                    try:
                        fut.result()
                    except:
                        # an error happened sending the message
                        pass    

                bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
        else:
            await playingMessage(ctx)


    #Posts the Bonk Video
    @commands.command(name='bonk', help='Bonk')
    async def bonk(self, ctx):
        await ctx.send(file=discord.File('./media/mp4/bonk.mp4'))


    #Posts a random Pikmin Meme
    @commands.command(name='bulborb', help='Posts a random bulborb')
    async def bulborb(self, ctx):
        bulborb = './media/bulborb/' + random.choice(os.listdir('./media/bulborb/'))
        await ctx.send(file=discord.File(bulborb))


"""

    Random Functions

"""
async def time_check():
    await bot.wait_until_ready()
    message_channel=bot.get_channel(159415088824975360)
    while True:
        day = datetime.date.today().weekday()
        now = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M')
        if (now == bot.reginaldTime and day == bot.reginaldDay):
            if not bot.reginaldBool:
                await message_channel.send(file=discord.File('./media/jpg/reginald.jpg'))
                bot.reginaldBool = True
            else:
                bot.reginaldBool = False
            time = 3600
        elif (now == bot.reginaldTime and day == 2):
            ran = random.choice(range(10))
            if ran == 0 and bot.reginaldBool:
                await message_channel.send(file=discord.File('./media/jpg/reginaldBread.jpg'))
            time = 3600    
        else:
            time = 60
        await asyncio.sleep(time)


async def playingMessage(ctx):
        response = ""
        
        if (bot.currentSong != "None"):
            response = "Song: \'" + bot.currentSong + "\' is currently playing. Either use s!stop or wait for it to finish."
        else:
            response = "A clip is currently playing already. Either use s!stop or wait for it to finish"

        await ctx.send(response)



bot.add_cog(Music(bot))
bot.add_cog(EverydayClassics(bot))
bot.add_cog(Misc(bot))

bot.loop.create_task(time_check())

bot.run(TOKEN)


