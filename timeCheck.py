"""

timeCheck.py
- Schedules time events to display things like birthday messages and Reginald 

"""

import random
import discord
from discord.ext import tasks, commands
import datetime
from datetime import timedelta
import os
import pandas


class timeCheck(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.fixedDate = datetime.date(1999, 5, 7)
        self.message_channel=self.bot.get_channel(self.bot.generalId)

        self.time_check.start()

    @tasks.loop(minutes=1)
    async def time_check(self):
        await self.bot.wait_until_ready()

        self.day = datetime.date.today().day
        self.month = datetime.date.today().month
        self.weekday = datetime.date.today().weekday()
        self.now = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M')

        delta = (datetime.date.today() - self.fixedDate)
        self.mod = delta.days % 14

        print(self.now, self.weekday, self.day, self.month)

        #General Noon Checks
        if (self.now == "12:00"):
            self.checkReginald(self)
            self.checkHolidays(self)
            self.checkBirthdays(self)
        #Mr Crab Friday at 5
        elif (self.now == "17:00" and self.weekday == 4):
            self.checkFriday(self)
        #Weevil Wednesday at 4 am
        elif (self.now == "04:00" and self.weekday == 2):
            self.checkWeevils(self)
            
    async def checkReginald(self):
        #Use a fixed date to find the Wednesday that shows up once every other week
        if (self.mod == 11):
            await self.message_channel.send(file=discord.File('./media/jpg/reginald.jpg'))
        elif (self.mod == 12):
            ran = random.choice(range(10))
            if ran == 0:
                await self.message_channel.send(file=discord.File('./media/jpg/reginaldBread.jpg'))

    async def checkHolidays(self):
        #Christmas
        if (self.month == 12 and self.day == 25):
            await self.message_channel.send("Merry Christmas!")
            await self.message_channel.send(file=discord.File('./media/mp4/catmas.mp4'))
        #April 30th?!
        elif (self.month == 4 and self.day == 30):
            await self.message_channel.send(file=discord.File('./media/mp4/4_30th.mp4'))

    async def checkFriday(self):
        await self.message_channel.send("You guys survived to the weekend! Here's a random meme to celebrate:")

        memeName = random.choice(os.listdir('./media/classicMemes/'))
        randomMeme = './media/classicMemes/' + memeName
        
        message = await self.message_channel.send("Uploading ...")

        try:
            await self.message_channel.send(file=discord.File(randomMeme))
            await message.delete()
        except:
            await self.message_channel.send(memeName + ': file is too big')
            await message.delete()

    async def checkWeevils(self):
        #Christmas
        if (self.month == 12 and self.day <= 25 and self.day > 18):
            await self.message_channel.send(file=discord.File('./media/weevil/special/weevil_wednesday_christmas.png'))
        #Default
        else:
            weevilName = random.choice(os.listdir('./media/weevil/wednesday/'))
            randomWeevil = './media/weevil/wednesday/' + weevilName

            await self.message_channel.send(file=discord.File(randomWeevil))

    async def checkBirthdays(self):
        bd = pandas.read_csv('./stat/birthdays.csv')
        for index, row in bd.iterrows():
            if (self.day == row['day'] and self.month == row['month']):

                if (' ' in row['name']):
                    firstName = row['name'].split()[0]
                    lastName = row['name'].split()[1]
                else:
                    firstName = row['name']
                    lastName = ''

                embed = discord.Embed(color = 0xeeeeee, title='Happy Birthday' + '!', url='https://itsyourbirthday.today/#' + firstName + '%20' + lastName)
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/387360051482066944/813515560955674664/cake.jpg')
                embed.add_field(name='Happy Birthday', value="! Strombot thinks it is your birthday and wishes you a happy birthday!!! Everyone wish, " + row['name'] + " a happy birthday!!!", inline=False) 
                message = await self.message_channel.send(embed = embed)
                await message.add_reaction('🎂')
                await message.add_reaction('🍨')

                if (firstName == 'Drew' and lastName == 'Crawford'):
                    await self.message_channel.send(file=discord.File('./media/gif/rats-warning.gif'))
