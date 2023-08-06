#misc.py - 
import os

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
#from discord.ext.commands import HTTPException
import random
import asyncio
import datetime
from datetime import timedelta
import traceback
from datetime import date

import drive
from utils import reactList
"""

    Miscellaneous

"""
class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
                
        #Tuesday at 12:00 pm
        self.bot.reginaldTime = "12:00"
        self.bot.reginaldDay = 1
        self.bot.reginaldBool = True

        self.bot.fixedDate = date(1999, 5, 7)

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


    #Posts the Yes Gif
    @commands.command(name='yes', help='Steve Ballmer sweaty reaction')
    async def yes(self, ctx):
       
        await ctx.send('https://tenor.com/view/steve-ballmer-yes-microsoft-gif-4349581')
       
    #Posts a random Pikmin Meme
    @commands.command(name='bulborb', help='Posts a random bulborb')
    async def bulborb(self, ctx, *query):
        if (len(query)  == 0):
            bulborbName = random.choice(os.listdir('./media/bulborb/'))
            randomMeme = './media/bulborb/' + bulborbName
            await ctx.send(file=discord.File(randomMeme))
            self.bot.Stat.bulborbUpdate(bulborbName)
        else:
            matching = os.listdir('./media/bulborb/')
            
            listBool = False
            for arg in query:
                if (arg == '-l'):
                    listBool = True
                else:
                    matching = [s for s in matching if arg.upper() in s.upper()]

            if (len(matching) == 0):
                await ctx.send('No results found')
            else:
                if (not listBool):
                    bulborbName =  random.choice(matching)
                    randomMeme = './media/bulborb/' + bulborbName
                    await ctx.send(file=discord.File(randomMeme))
                    self.bot.Stat.bulborbUpdate(bulborbName)
                else:
                    await reactList(ctx, self.bot, query, matching)


    #Posts a random Warrior Cats Image
    @commands.command(name='cat',help='Posts a random warrior cats image')
    async def cat(self, ctx, *query):
        #cat = './media/cats/' + random.choice(os.listdir('./media/cats/'))
        #await ctx.send(file=discord.File(cat))

        if (len(query)  == 0):
            catName = random.choice(os.listdir('./media/cats/'))
            cat = './media/cats/' + catName
            await ctx.send(file=discord.File(cat))
            self.bot.Stat.catUpdate(catName)
        else:
            matching = os.listdir('./media/cats/')
            
            listBool = False
            for arg in query:
                if (arg == '-l'):
                    listBool = True
                else:
                    matching = [s for s in matching if arg.upper() in s.upper()]

            if (len(matching) == 0):
                await ctx.send('No results found')
            else:
                if (not listBool):
                    catName = random.choice(matching)
                    cat= './media/cats/' + catName
                    await ctx.send(file=discord.File(cat))
                    self.bot.Stat.catUpdate(catName)
                else:
                    await reactList(ctx, self.bot, query, matching)

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


    #Coin Flip
    @commands.command(name = 'coin', help = 'Flips a coin')
    async def coin(self, ctx):
        flip = random.choice(range(2));

        if (flip):
            await ctx.send("Heads")
        else:
            await ctx.send("Tails")

    #Dark
    @commands.command(name = 'dark', help = 'Plays a random Dark Souls Sound')
    async def dark(self, ctx, *query):
        dark = ""
        if (len(query)  == 0):
            dark = './media/dark/' + random.choice(os.listdir('./media/dark/'))
        else:
            matching = os.listdir('./media/dark/')
            for arg in query:

                matching = [s for s in matching if arg.upper() in s.upper()]

            if (len(matching) == 0):
                await ctx.send('No results found')
            else:
                dark = './media/dark/' + random.choice(matching)

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
                self.bot.currentVC.play(discord.FFmpegPCMAudio(source=dark), after=my_after)
                #except:
                #return

        else:
            await playingMessage(ctx)


    #Update
    @commands.command(name = 'update', help = 'Downloads any new files from the google drive')
    async def update(self, ctx):
        messageStart = "Searching the Google Drive .\n-----------------------------------\n"
        post = await ctx.send(messageStart)

        message = ''
        memeUpdate = await drive.update('./media/classicMemes/', "Classic Memes", messageStart, message, post);
        messageStart = "Searching the Google Drive ..\n-----------------------------------\n"
        if not (memeUpdate[:2] == 'No'):
            message = message + memeUpdate	
        await post.edit(content = messageStart + message)
        
        

        catUpdate = await drive.update('./media/cats/', "Warrior Cats", messageStart, message, post);
        messageStart = "Searching the Google Drive ...\n-----------------------------------\n"
        if not (catUpdate[:2] == 'No'):
            message = message + catUpdate	
        await post.edit(content = messageStart + message)


        bulborbUpdate = await drive.update('./media/bulborb/', "Bulborbs", messageStart, message, post);
        messageStart = "Searching the Google Drive ....\n-----------------------------------\n"
        if not (bulborbUpdate[:2] == 'No'):
            message = message + bulborbUpdate	
        await post.edit(content = messageStart + message)


        dailySum = int(await drive.update('./media/dayMemes/monday/', "Monday", messageStart, message, post)); 
        messageStart = "Searching the Google Drive *\n-----------------------------------\n"
        await post.edit(content = messageStart + message)

        dailySum = dailySum + int(await drive.update('./media/dayMemes/tuesday/', "Tuesday", messageStart, message, post));
        messageStart = "Searching the Google Drive *.\n-----------------------------------\n"
        await post.edit(content = messageStart + message)

        dailySum = dailySum + int(await drive.update('./media/dayMemes/wednesday/', "Wednesday", messageStart, message, post));
        messageStart = "Searching the Google Drive *..\n-----------------------------------\n"
        await post.edit(content = messageStart + message)

        dailySum = dailySum + int(await drive.update('./media/dayMemes/thursday/', "Thursday", messageStart, message, post));
        messageStart = "Searching the Google Drive *...\n-----------------------------------\n"
        await post.edit(content = messageStart + message)

        dailySum = dailySum + int(await drive.update('./media/dayMemes/friday/', "Friday", messageStart, message, post));
        messageStart = "Searching the Google Drive *....\n-----------------------------------\n"
        await post.edit(content = messageStart + message)

        dailySum = dailySum + int(await drive.update('./media/dayMemes/saturday/', "Saturday", messageStart, message, post));
        messageStart = "Searching the Google Drive **\n-----------------------------------\n"
        await post.edit(content = messageStart + message)

        dailySum = dailySum + int(await drive.update('./media/dayMemes/sunday/', "Sunday", messageStart, message, post));
        messageStart = "Searching the Google Drive **.\n-----------------------------------\n"
       
        if not (dailySum == 0):
            message = message + "Added: Daily Memes: " + str(dailySum) + "\n"
        await post.edit(content = messageStart + message)


        knuckSum = int(await drive.update('./media/rateMeme/good/', "Good Rates", messageStart, message, post)); 
        messageStart = "Searching the Google Drive **..\n-----------------------------------\n"
        await post.edit(content = messageStart + message)

        knuckSum = knuckSum + int(await drive.update('./media/rateMeme/bad/', "Bad Rates", messageStart, message, post));
        messageStart = "Searching the Google Drive **...\n-----------------------------------\n"
        await post.edit(content = messageStart + message)

        knuckSum = knuckSum + int(await drive.update('./media/rateMeme/other/', "Other Rates", messageStart, message, post));
        messageStart = "Searching the Google Drive **....\n-----------------------------------\n"
       
        if not (knuckSum == 0):
            message = message + "Added: Knuckles Memes: " + str(knuckSum) + "\n"
        await post.edit(content = messageStart + message)


        kcSum = int(await drive.update('./media/kekOrCringe/kek/', "Kek", messageStart, message, post));
        messageStart = "Searching the Google Drive ***\n-----------------------------------\n"
        await post.edit(content = messageStart + message)

        kcSum = kcSum + int(await drive.update('./media/kekOrCringe/cringe/', "Cringe", messageStart, message, post));
        messageStart = "Searching the Google Drive ***.\n-----------------------------------\n"
        if not (kcSum == 0):
            message = message + "Added: Kek Or Cringe Memes: " + str(kcSum) + "\n"
        await post.edit(content = messageStart + message)

        weevilSum = int(await drive.update('./media/weevil/wednesday/', "Weevil Wednesday", messageStart, message, post));
        messageStart = "Searching the Google Drive ***..\n-----------------------------------\n"
        if not (weevilSum == 0):
            message = message + "Added: Weevil Wednesday Memes: " + str(weevilSum) + "\n"
        await post.edit(content = messageStart + message)

        weevilSpecialSum = int(await drive.update('./media/weevil/special/', "Special Days", messageStart, message, post));
        messageStart = "Searching the Google Drive ***...\n-----------------------------------\n"
        if not (weevilSpecialSum == 0):
            message = message + "Added: Weevil Special Memes: " + str(weevilSpecialSum) + "\n"
        

        if message == '':
            message = 'No New Content Found'


        await post.edit(content = message)

    #Patch
    @commands.command(name='patch', help='Shows most recent updates')
    async def patch(self, ctx):
        embed = discord.Embed(color= 0xeeeeee)
        
        embed.add_field(name='Patch 4/9/21', value='-------------------------', inline=False)
        
        #embed.add_field(name='New Commands', value='------', inline=False)
        #embed.add_field(name='s!kek', value='Posts a meme to congratulate another user\'s post. Contains search and list functionality', inline=True)
        #embed.add_field(name='s!cringe', value='Posts a meme to bad-mouth another user\'s post. Contains search and list functionality', inline=True)
       
        embed.add_field(name='\u200b\nChanges to Existing Commands', value='------', inline=False)
        embed.add_field(name='More Updating', value='s!update can now update dailymemes. You can now upload your own daily memes by uploading them in the correct google drive folder.', inline=True)
        embed.add_field(name='Daily Search and List', value='s!dailyMeme now be searched and listed with "-l" and any query. Will only show memes for the correct day. Also, files have been properly named.', inline=True)

        embed.add_field(name='\u200b\nNew Background Effects', value='------', inline=False)
        embed.add_field(name='Crab Friday Rework', value='Crab Friday has been replaced with an end of the week random meme. Will show up every Friday at 5 EST to post an s!meme', inline=True)

        #embed.add_field(name='\u200b\nOther', value='I honestly changed a lot more, but I forgot what it was over the course of like 2 weeks, so sorry', inline = False)

        await ctx.send(embed=embed)

#Check if user is in a Dm 
async def isDm(ctx):
    if (ctx.message.guild == None):
        await ctx.send("Good to go!")
        return True
    else:
        await ctx.send("Nope DM me") 
        return False


