#bot.py
import os

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv
import random
import asyncio
import datetime
from datetime import timedelta
import traceback
#import time

#time.sleep(5)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='s!')
client = discord.Client()

bot.last_song = ""

bot.acridTime = datetime.datetime.now() - timedelta(minutes=5);

bot.adminId = 170301539020308481;
bot.generalId = 159415088824975360;

#Says a message when a new member enters the discord
@bot.event
async def on_ready():
    print(bot.user.name + ' has connected to Discord!')

#Default if no command is found
@bot.event
async def on_command_error(ctx, error):
	if (isinstance(error, CommandNotFound)):
		await ctx.send("Command does not exist. That is really embarrassing " + ctx.author.display_name);
		return
	#print("error time");
	file=open("log.txt", "a")
	print(error);
	file.write(error)
	file.close()

bot.playlist_counter = 0
bot.musicList = None
bot.currentVC = None
bot.currentSong = "None"
bot.currentList = "memeful/"


#Tuesday at 12:00 pm
bot.reginaldTime = "12:00"
bot.reginaldDay = 1
bot.reginaldBool = False


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
                    bot.currentVC.source.cleanup()
                    coro = bot.currentVC.disconnect()
                    fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
                    try:
                        fut.result()
                    except:
                        # an error happened sending the message
                        pass    

                bot.currentList = "memeful/"

                bot.currentSong = bot.musicList[0]
                
                #try:
                bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
                #except:
                        #return
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

                #print(bot.playlist_counter)
                #print(len(bot.musicList))

                randomSong = './media/mp3/playlist/memeful/' + bot.musicList[0]
            
                bot.playlist_counter = 1



                def my_after(error):
                    if (bot.musicList != None and not bot.currentVC.is_playing() and bot.currentVC.is_connected()):
                        #print(bot.playlist_counter)
                        #print(len(bot.musicList))

                        if bot.playlist_counter >= len(bot.musicList):
                            bot.currentVC.source.cleanup()
                            coro = bot.currentVC.disconnect()
                            fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)

                            bot.currentSong = "None"
                        else:
                            randomSong = './media/mp3/playlist/memeful/' + bot.musicList[bot.playlist_counter]
                            bot.currentSong = bot.musicList[bot.playlist_counter]
                            bot.playlist_counter = bot.playlist_counter + 1
                            #try:
                            bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
                            #except:
                                #return
            
                bot.currentList = "memeful/"
                
                bot.currentSong = bot.musicList[0]
                #try:
                bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
                #except:
                    #return
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
                    bot.currentVC.source.cleanup()
                    coro = bot.currentVC.disconnect()
                    fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
                    try:
                        fut.result()
                    except:
                        # an error happened sending the message
                        pass    

                bot.currentList = "memeless/"

                bot.currentSong = bot.musicList[0]
                #try:
                bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
                #except:
                    #return
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
           
                #print(bot.playlist_counter)
                #print(len(bot.musicList))
 
                bot.playlist_counter = 1

		

                def my_after(error):
                    if (bot.musicList != None and not bot.currentVC.is_playing() and bot.currentVC.is_connected()):
                        
                        #print(bot.playlist_counter)
                        #print(len(bot.musicList))		

                        if bot.playlist_counter >= len(bot.musicList):
                            bot.currentVC.source.cleanup()
                            coro = bot.currentVC.disconnect()
                            fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
                            bot.currentSong = "None"
                        else:
                            randomSong = './media/mp3/playlist/memeful/' + bot.musicList[bot.playlist_counter]
                            bot.currentSong = bot.musicList[bot.playlist_counter]
                            bot.playlist_counter = bot.playlist_counter + 1
                            #try:
                            bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
                            #except:
                                #return

                bot.currentList = "memeless/"
                
                bot.currentSong = bot.musicList[0]
                #try:
                bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
                #except:
                    #return
        else:
            await playingMessage(ctx)


    #Skips currently played song
    @commands.command(name='skip', help='Skips currently played song')
    async def skip(self, ctx):
        def my_after(error):
                if (bot.musicList != None and bot.playlist_counter <= len(bot.musicList) and not bot.currentVC.is_playing() and bot.currentVC.is_connected()):
                    #print(bot.playlist_counter)
                    #print(len(bot.musicList))

                    randomSong = './media/mp3/playlist/' + bot.currentList + bot.musicList[bot.playlist_counter]
                    bot.currentSong = bot.musicList[bot.playlist_counter]
                    bot.playlist_counter = bot.playlist_counter + 1
                    #try:
                    bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
                    #except:
                        #return
	
        if (bot.currentVC.is_playing() and bot.currentVC.is_connected()):
      
            if (bot.musicList == None or bot.playlist_counter >= len(bot.musicList)):
                bot.playlist_counter = 0
                bot.musicList = None
                server = ctx.message.guild.voice_client
                await server.disconnect()
                bot.currentSong = "None"
            else:
                #print(bot.playlist_counter)
                #print(len(bot.musicList))

                randomSong = './media/mp3/playlist/' + bot.currentList + bot.musicList[bot.playlist_counter]
                bot.currentSong = bot.musicList[bot.playlist_counter]
                bot.playlist_counter = bot.playlist_counter + 1

                bot.currentVC.stop()
                #try:
                bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
                #except Exception:
                        #return 
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

	#Make sure Bot is connected to a voice channel
        if bot.currentVC != None and bot.currentVC.is_connected():
                bot.currentVC.source.cleanup()
                coro = bot.currentVC.disconnect()
                fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
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
                    bot.currentVC.source.cleanup()
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

    #Posts a random Warrior Cats Image
    @commands.command(name='cat',help='Posts a random warrior cats image')
    async def cat(self, ctx):
        cat = './media/cats/' + random.choice(os.listdir('./media/cats/'))
        await ctx.send(file=discord.File(cat))

    #Plays the Bruh Sound
    @commands.command(name='bruh', help='Bruh')
    async def bruh(self, ctx):
        bruh = './media/mp3/bruh/bruh.mp3'
        if (bot.currentVC == None or not bot.currentVC.is_playing()):
            user = ctx.message.author
            userVC = user.voice.channel

            if userVC != None:
                channelName = userVC.name
                voiceChannel = discord.utils.get(ctx.guild.channels, name=channelName)
                bot.currentVC = await voiceChannel.connect()
       
                def my_after(error):
                    bot.currentVC.source.cleanup()
                    coro = bot.currentVC.disconnect()
                    fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
                    try:
                        fut.result()
                    except:
                        # an error happened sending the message
                        pass    


 
                #try:
                bot.currentVC.play(discord.FFmpegPCMAudio(source=bruh), after=my_after)
                #except:
                    #return

        else:
            await playingMessage(ctx)

"""

    Random Functions

"""
async def time_check():
    await bot.wait_until_ready()
    message_channel=bot.get_channel(bot.generalId)
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

#Used for hidden commands
@bot.event
async def on_message(ctx):
	if (ctx.author == bot.user):
		return

	user = ctx.author.id


	#Check for s!maintOn
	if (ctx.content == 's!maintOn'):
		#Check if user is an admin	
		if (user == bot.adminId):
			message_channel=bot.get_channel(bot.generalId)
			#await ctx.channel.send("maintOn");
			await message_channel.send("StromBot is currently undergoing maintenance\nPlease refrain from using any commands until further notice")
			
		return	
	
	#Check for s!maintOff
	if (ctx.content == 's!maintOff'):
		#Check if user is an admin	
		if (user == bot.adminId):
			message_channel=bot.get_channel(bot.generalId)
			#await ctx.channel.send("maintOff");
			await message_channel.send("StromBot is no longer undergoing maintenance\nKeep on Stromming")
		return


	#Check for acrid.gif
	url = ctx.content
	url = url.split('/')[-1]
	
	if (url == 'acrid.gif' and getAcridTime()):
		acrid = './media/jpg/acrid.gif'

		#Set the time last acrid was posted
		bot.acridTime = datetime.datetime.now()
		await ctx.channel.send(file=discord.File(acrid));

	#Go to Other Commands
	await bot.process_commands(ctx);

def getAcridTime():
	now = datetime.datetime.now()
	if (bot.acridTime + timedelta(minutes=5) < now):
		return True
	else:
		return False 

bot.add_cog(Music(bot))
bot.add_cog(EverydayClassics(bot))
bot.add_cog(Misc(bot))

bot.loop.create_task(time_check())

bot.run(TOKEN)


