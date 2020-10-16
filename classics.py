#classics.py - contains EverydayClassics class and generally useful functions 
import os

import discord
from discord.ext import commands
import random
import asyncio
import datetime
from datetime import timedelta
import traceback




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

        #print(ctx.message.guild.members)

        ran = random.choice(range(10))

        if (ran < 2):
            randomUserId = 159433180036726784

        randomUser = ctx.message.guild.get_member(randomUserId).display_name
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

    #Posts a Knuckle Video to Rate your meme
    @commands.command(name='rateMeme', help='Rates your meme!')
    async def rateMeme(self, ctx):
        randomRate = './media/mp4/rateMeme/' + random.choice(os.listdir('./media/mp4/rateMeme/'))
        await ctx.send(file=discord.File(randomRate))

    #Rates The Previous Post from 1 to 10
    @commands.command(name='ratePost', help="Rates the latest Post from 1 to 10")
    async def ratePost(self, ctx):
        rating = 0
        message = ""
        	
        post = await ctx.channel.history(limit = 2).flatten()
        if (post[1].author == self.bot.user):
            rating = 10
        else:
            rating = random.choice(range(10)) + 1
        
        if (rating == 10):
            message = "**10/10**\n" + post[1].author.display_name + ", I absolutely love that post!!!! Perfection! That should go in the world record for best discord posts!!! You deserve a medal right now!!"
        elif (rating == 9):
            message =  "**9/10**\n" + post[1].author.display_name + ", I really like that post, almost a near perfect one at that. You should try other skills like bowling."
        elif (rating == 8):
            message = "**8/10**\n" + post[1].author.display_name + ", I think that post was really good, thoroughly enjoyable. Next Time try really hard to break those limits to get a perfect post."
        elif (rating == 7):
            message = "**7/10**\n" + post[1].author.display_name + ", that post was pretty good, almost great. Like a good ham sandwhich, but not too good of a ham sandwhich."
        elif (rating == 6):
            message = "**6/10**\n" + post[1].author.display_name + ", I  think that post was pretty okay, could use some work. I have a feeling that you could do better with a bit more effort."
        elif (rating == 5):
            message = "**5/10**\n" + post[1].author.display_name + ", pretty meh post, doesn't really stand out to me. Kinda disappointed not gonna lie."
        elif (rating == 4):
            message = "**4/10**\n" + post[1].author.display_name + ", not a good post. I think you really need to re-evaluate your posts. It reminds of that time I bought a lobster, but the lobster wasn't a pure bred."
        elif (rating == 3):
            message = "**3/10**\n" + post[1].author.display_name + ", what an awful post. I hated it. You need to up your game a LOT. Not looking forward to your next post."
        elif (rating == 2):
            message = "**2/10**\n" + post[1].author.display_name + ", I feel like that post was trying to make me mad. Well, you succeeded. That was a terrible post. Please don't ever post again. This is way worse than that lobster time."
        elif (rating == 1):
            message = "**1/10**\n" + post[1].author.display_name + ", or should I say " + post[1].author.display_name[:len(post[1].author.display_name) // 2] + "Dumb, WOW!!!! RING RING RING!!!!! You are a terrible poster, terrible person for even thinking about that post. AND then you sent it!!!!!! I am so appalled right now. Your lucky there aren't ban privileges in this command. Because you WOULD be banned right now." 
        
        await ctx.send(message)

