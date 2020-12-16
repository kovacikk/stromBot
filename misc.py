#misc.py - 
import os

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import random
import asyncio
import datetime
from datetime import timedelta
import traceback


#Import from battle.py
import battle as bt

"""

    Miscellaneous

"""
class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
                
        #Tuesday at 12:00 pm
        self.bot.reginaldTime = "12:00"
        self.bot.reginaldDay = 1
        self.bot.reginaldBool = False

        self.bot.battleMain = None

        self.bot.battlerOne = None
        self.bot.battlerTwo = None

        self.bot.battleBool = False


    #Picks a seven dollars clip and plays it
    @commands.command(name='7', help='Seven Dollars')
    async def sevenDollars(self, ctx):
        if (self.bot.currentVC == None or not self.bot.currentVC.is_playing()):
            user = ctx.message.author
            userVC = user.voice.channel

            if userVC != None:
                channelName = userVC.name
                voiceChannel = discord.utils.get(ctx.guild.channels, name=channelName)
                self.bot.currentVC = await voiceChannel.connect()

                randomSong = './media/mp3/shane/' + random.choice(os.listdir('./media/mp3/shane/'))

                def my_after(error):
                    self.bot.currentVC.source.cleanup()
                    coro = self.bot.currentVC.disconnect()
                    fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
                    try:
                        fut.result()
                    except:
                        # an error happened sending the message
                        pass    

                self.bot.currentVC.play(discord.FFmpegPCMAudio(source=randomSong), after=my_after)
                
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
        if (self.bot.currentVC == None or not self.bot.currentVC.is_playing()):
            user = ctx.message.author
            userVC = user.voice.channel

            if userVC != None:
                channelName = userVC.name
                voiceChannel = discord.utils.get(ctx.guild.channels, name=channelName)
                self.bot.currentVC = await voiceChannel.connect()
       
                def my_after(error):
                    self.bot.currentVC.source.cleanup()
                    coro = self.bot.currentVC.disconnect()
                    fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
                    try:
                        fut.result()
                    except:
                        # an error happened sending the message
                        pass    


 
                #try:
                self.bot.currentVC.play(discord.FFmpegPCMAudio(source=bruh), after=my_after)
                #except:
                    #return

        else:
            await playingMessage(ctx)


    #Start Battle with Another User
    @commands.command(name = 'battle', help='Battle Someone')
    async def battle(self, ctx):
        if not self.bot.battleBool:
            #Must Wait for Battler
            if (self.bot.battlerOne == None):
                self.bot.battlerOne = ctx.author
                await ctx.send(ctx.author.display_name +  " wants to battle!\nType s!battle to battle them")
        
            #Second Battler is Ready
            else:
                if (ctx.author != self.bot.battlerOne):
                    await ctx.send("First Battler: " + self.bot.battlerOne.display_name + "\nSecond Battler: " + ctx.author.display_name)
            
                    battleDmOne = await self.bot.battlerOne.create_dm()
                    await battleDmOne.send("You are battling with " + ctx.author.display_name)
            
                    self.bot.battlerTwo = ctx.author

                    battleDmTwo = await self.bot.battlerTwo.create_dm()
                    await battleDmTwo.send("You are battling with " + self.bot.battlerOne.display_name)

                    self.bot.battleBool = True
                    
                    self.bot.battleMain = bt.Battle(self.bot.battlerOne, self.bot.battlerTwo, ctx.message.channel)
                    
                    self.bot.battlerOne = None

                else:
                    await ctx.send("You can't battle yourself!!!!")
        else:
            await ctx.send("Battle already started, wait for it to finish")


    #Send Response for Battle
    @commands.command(name = 'move', help = 'Send your Move for battle')
    async def move(self, ctx, choice):
        #Retrieve Move
        if (ctx.author == self.bot.battlerOne):
            if (not isDM(ctx)):
                self.bot.battleMain.stateOne.move = choice
                self.bot.battleMain.checkMove()	    
        elif (ctx.author == self.bot.battlerTwo):
            if (not isDM(ctx)):
                self.bot.battleMain.stateTwo.move = choice
                self.bot.battleMain.checkMove()
        else:
            await ctx.send("Not In a Battle") 

    #Cards Thing
    @commands.command(name = 'drop', help = 'Drops Card')
    async def drop(self, ctx):
        #ID
        await ctx.send("kd")





#Check if user is in a Dm 
async def isDm(ctx):
    if (ctx.message.guild == None):
        await ctx.send("Good to go!")
        return True
    else:
        await ctx.send("Nope DM me") 
        return False


