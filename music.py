#music.py - contains Music class and functions to play songs

import os

import discord
from discord.ext import commands
import random
import asyncio

import traceback
from utils import reactList


"""

    Music

"""
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  
        self.bot.playlist_counter = 0 
        self.bot.musicList = None
        self.bot.currentVC = None
        self.bot.currentSong = "None"
        self.bot.currentList = "memeful/"	
    

    #Picks a song from the playlist and plays it
    @commands.command(name='songMeme', help='Play a random song from the playlist')
    async def songMeme(self, ctx, *query):
        listBool = False
        for arg in query:
            if (arg == '-l'):
                listBool = True

        if(listBool):
             matching = os.listdir('./media/mp3/playlist/memeful/')
             for arg in query:
                 if not (arg == '-l'):
                     matching = [s for s in matching if arg.upper() in s.upper()]

             if (len(matching) == 0):
                 await ctx.send('No results found')
                 return
             else:
                 await reactList(ctx, self.bot, query, matching) 
        elif (self.bot.currentVC == None or not self.bot.currentVC.is_playing()):
            user = ctx.message.author
            userVC = user.voice.channel

            #Check if user is in Voice Chat
            if userVC != None:
                channelName = userVC.name
                voiceChannel = discord.utils.get(ctx.guild.channels, name=channelName)
                                
                #randomChoice = random.choice(os.listdir('./media/mp3/playlist/memeful/'))
                #randomSong = './media/mp3/playlist/memeful/' + randomChoice

                if (len(query)  == 0):
                    randomChoice = random.choice(os.listdir('./media/mp3/playlist/memeful/'))
                    randomSong = './media/mp3/playlist/memeful/' + randomChoice
                else:
                    matching = os.listdir('./media/mp3/playlist/memeful/')
                    
                    listBool = False
                    for arg in query:
                        if (arg == '-l'):
                            listBool = True
                        else:
                            matching = [s for s in matching if arg.upper() in s.upper()]

                    if (len(matching) == 0):
                        await ctx.send('No results found')
                        return
                    else:
                        if (not listBool):
                            randomChoice =  random.choice(matching)
                            randomSong = './media/mp3/playlist/memeful/' + randomChoice
                        else:
                            await reactList(ctx, self.bot, query, matching)
                
                self.bot.currentVC = await voiceChannel.connect()

                self.bot.musicList = [randomChoice]
                self.bot.playlist_counter = 1

                self.bot.Stat.songUpdate(randomChoice)

                #Disconnect from Voice Chat after Song
                def my_after(error):
                    self.bot.musicList = None
                    self.bot.currentSong = "None"
                    self.bot.currentVC.source.cleanup()
                    coro = self.bot.currentVC.disconnect()
                    fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
                    try:
                        fut.result()
                    except:
                        # an error happened sending the message
                        pass    

                self.bot.currentList = "memeful/"
                self.bot.currentSong = self.bot.musicList[0]
               
                self.bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
        else:
            await playingMessage(ctx)


    #Picks songs from the playlist and plays them
    @commands.command(name='playlistMeme', help='Shuffles songs from the playlist')
    async def songsMeme(self, ctx, *query):
        listBool = False
        for arg in query:
            if (arg == '-l'):
                listBool = True

        if(listBool):
             matching = os.listdir('./media/mp3/playlist/memeful/')
             for arg in query:
                 if not (arg == '-l'):
                     matching = [s for s in matching if arg.upper() in s.upper()]

             if (len(matching) == 0):
                 await ctx.send('No results found')
                 return
             else:
                 await reactList(ctx, self.bot, query, matching) 
        elif (self.bot.currentVC == None or not self.bot.currentVC.is_playing()):
            user = ctx.message.author
            userVC = user.voice.channel
 
            #Check if user is in Voice Chat
            if userVC != None:
                channelName = userVC.name
                voiceChannel = discord.utils.get(ctx.guild.channels, name=channelName)

                if (len(query)  == 0):
                    self.bot.musicList = os.listdir('./media/mp3/playlist/memeful/')
                else:
                    matching = os.listdir('./media/mp3/playlist/memeful/')
                    
                    listBool = False
                    for arg in query:
                        if (arg == '-l'):
                            listBool = True
                        else:
                            matching = [s for s in matching if arg.upper() in s.upper()]

                    if (len(matching) == 0):
                        await ctx.send('No results found')
                        return
                    else:
                        if (not listBool):
                            self.bot.musicList = matching
                        else:
                            await reactList(ctx, self.bot, query, matching)
                            return

                self.bot.currentVC = await voiceChannel.connect()

                #self.bot.musicList = os.listdir('./media/mp3/playlist/memeful/')
                random.shuffle(self.bot.musicList)
                
                #print("in playlist Meme start")
                #print(self.bot.playlist_counter)
                #print(len(self.bot.musicList))

                randomSong = './media/mp3/playlist/memeful/' + self.bot.musicList[0]
           
                self.bot.Stat.songUpdate(self.bot.musicList[0])
 
                self.bot.playlist_counter = 1

                #Play next song or Disconnect from VC when finished
                def my_after(error):
                    if (self.bot.musicList != None and not self.bot.currentVC.is_playing() and self.bot.currentVC.is_connected()):
                        #print("in playlist Meme after")
                        #print(self.bot.playlist_counter)
                        #print(len(self.bot.musicList))

			#Check if Playlist has finished
                        if self.bot.playlist_counter >= len(self.bot.musicList):
                            self.bot.currentVC.source.cleanup()
                            coro = self.bot.currentVC.disconnect()
                            fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
                            self.bot.musicList = None
                            self.bot.currentSong = "None"
                        #Play next song
                        else:
                            randomSong = './media/mp3/playlist/memeful/' + self.bot.musicList[self.bot.playlist_counter]
                            self.bot.currentSong = self.bot.musicList[self.bot.playlist_counter]
                            self.bot.Stat.songUpdate(self.bot.musicList[self.bot.playlist_counter])
                            self.bot.playlist_counter = self.bot.playlist_counter + 1
                            
                            self.bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
                            
            
                self.bot.currentList = "memeful/" 
                self.bot.currentSong = self.bot.musicList[0]
                
                self.bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
                
        else:
            await playingMessage(ctx)


    #Picks a song from the playlist and plays it
    @commands.command(name='song', help='Play a random song from the playlist without memes')
    async def song(self, ctx, *query):
        listBool = False
        for arg in query:
            if (arg == '-l'):
                listBool = True

        if(listBool):
             matching = os.listdir('./media/mp3/playlist/memeless/')
             for arg in query:
                 if not (arg == '-l'):
                     matching = [s for s in matching if arg.upper() in s.upper()]

             if (len(matching) == 0):
                 await ctx.send('No results found')
                 return
             else:
                 await reactList(ctx, self.bot, query, matching) 
        elif (self.bot.currentVC == None or not self.bot.currentVC.is_playing()):
            user = ctx.message.author
            userVC = user.voice.channel

            #Check if user is in Voice Chat
            if userVC != None:
                channelName = userVC.name
                voiceChannel = discord.utils.get(ctx.guild.channels, name=channelName)

                #randomChoice = random.choice(os.listdir('./media/mp3/playlist/memeless/'))
                #randomSong = './media/mp3/playlist/memeless/' + randomChoice
               
                if (len(query)  == 0):
                    randomChoice = random.choice(os.listdir('./media/mp3/playlist/memeless/'))
                    randomSong = './media/mp3/playlist/memeless/' + randomChoice
                else:
                    matching = os.listdir('./media/mp3/playlist/memeless/')
                    listBool = False
                    for arg in query:
                        if (arg == '-l'):
                            listBool = True
                        else:
                            matching = [s for s in matching if arg.upper() in s.upper()]

                    if (len(matching) == 0):
                        await ctx.send('No results found')
                        return
                    else:
                        if (not listBool):
                            randomChoice = random.choice(matching)
                            randomSong = './media/mp3/playlist/memeless/' + randomChoice
                        else:
                            await reactList(ctx, self.bot, query, matching) 

                self.bot.currentVC = await voiceChannel.connect()

                self.bot.Stat.songUpdate(randomChoice)

                self.bot.musicList = [randomChoice]
                self.bot.playlist_counter = 1

                #Disconnect from Voice Chat when song finishes
                def my_after(error):
                    self.bot.musicList = None
                    self.bot.currentSong = "None"
                    self.bot.currentVC.source.cleanup()
                    coro = self.bot.currentVC.disconnect()
                    fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
                    try:
                        fut.result()
                    except:
                        pass    

                self.bot.currentList = "memeless/"
                self.bot.currentSong = self.bot.musicList[0]
                
                self.bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
                
        else:
            await playingMessage(ctx)


    #Picks songs from the playlist and plays them
    @commands.command(name='playlist', help='Shuffles songs from the playlist without memes')
    async def songs(self, ctx, *query):
        listBool = False
        for arg in query:
            if (arg == '-l'):
                listBool = True

        if(listBool):
             matching = os.listdir('./media/mp3/playlist/memeless/')
             for arg in query:
                 if not (arg == '-l'):
                     matching = [s for s in matching if arg.upper() in s.upper()]

             if (len(matching) == 0):
                 await ctx.send('No results found')
                 return
             else:
                 await reactList(ctx, self.bot, query, matching) 
        if (self.bot.currentVC == None or not self.bot.currentVC.is_playing()):
            user = ctx.message.author
            userVC = user.voice.channel

            #Check if user is in Voice Chat
            if userVC != None:
                channelName = userVC.name
                voiceChannel = discord.utils.get(ctx.guild.channels, name=channelName)


                self.bot.musicList = os.listdir('./media/mp3/playlist/memeless/')
                
                if (len(query)  == 0):
                    self.bot.musicList = os.listdir('./media/mp3/playlist/memeless/')
                else:
                    matching = os.listdir('./media/mp3/playlist/memeless/')
                    listBool = False
                    for arg in query:
                        if (arg == '-l'):
                            listBool = True
                        else:
                            matching = [s for s in matching if arg.upper() in s.upper()]

                    if (len(matching) == 0):
                        await ctx.send('No results found')
                        return
                    else:
                        if (not listBool):
                            self.bot.musicList = matching
                        else:
                            await reactList(ctx, self.bot, query, matching)

                self.bot.currentVC = await voiceChannel.connect()

                random.shuffle(self.bot.musicList)

                randomSong = './media/mp3/playlist/memeless/' + self.bot.musicList[0]
                #print("in playlist start")
                #print(self.bot.playlist_counter)
                
                self.bot.playlist_counter = 1
		
                #Play next song or Disconnect from VC when finished
                def my_after(error):
                    if (self.bot.musicList != None and not self.bot.currentVC.is_playing() and self.bot.currentVC.is_connected()):
                        #print("in playlist after")
                        #print(self.bot.playlist_counter)
                        #print(len(self.bot.musicList))		

                        if self.bot.playlist_counter >= len(self.bot.musicList):
                            self.bot.currentVC.source.cleanup()
                            coro = self.bot.currentVC.disconnect()
                            fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
                            self.bot.currentSong = "None"
                            self.bot.musicList = None
                        else:
                            randomSong = './media/mp3/playlist/memeless/' + self.bot.musicList[self.bot.playlist_counter]
                            self.bot.currentSong = self.bot.musicList[self.bot.playlist_counter]
                            self.bot.playlist_counter = self.bot.playlist_counter + 1
                            self.bot.Stat.songUpdate(self.bot.musicList[self.bot.playlist_counter])
                            self.bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
                            

                self.bot.currentList = "memeless/"
                self.bot.currentSong = self.bot.musicList[0]
                
                self.bot.Stat.songUpdate(self.bot.musicList[0])

                self.bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
                
        else:
            await playingMessage(ctx)


    #Skips currently played song
    @commands.command(name='skip', help='Skips currently played song')
    async def skip(self, ctx):
        #Check if bot is playing and connected
        if (self.bot.currentVC.is_playing() and self.bot.currentVC.is_connected()):
      
            #Check if we have reached the end of the musicList
            if (self.bot.musicList == None or self.bot.playlist_counter >= len(self.bot.musicList)):
                self.bot.playlist_counter = 0
                self.bot.musicList = None
                server = ctx.message.guild.voice_client
                await server.disconnect()
                self.bot.currentSong = "None"

            #Stop the Current Voice Connection to Get to Next Song
            else:
                #print("in skip start")
                #print(self.bot.playlist_counter)

                self.bot.currentVC.stop()


    #Explains what songs is currently playing
    @commands.command(name="playing", help="Tells what song is currently playing")
    async def playing(self, ctx):
        response = "The song: \'" + self.bot.currentSong + "\' is currently playing"
        await ctx.send(response)


    #Disconnects Bot from Voice Chat
    @commands.command(name='stop', help='Stops music or clips from being played in voice', pass_context=True)
    async def stop(self, ctx):

	#Make sure Bot is connected to a voice channel
        if self.bot.currentVC != None and self.bot.currentVC.is_connected():
                self.bot.musicList = None
                self.bot.currentVC.source.cleanup()
                coro = self.bot.currentVC.disconnect()
                fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
                self.bot.currentSong = "None"

