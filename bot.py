"""
bot.py

- Contains main discord bot functions, loads other files and connects

"""

import os
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands import MissingRequiredArgument
from dotenv import load_dotenv
import random
import asyncio
import datetime
from datetime import timedelta
import traceback
import sys
import pandas

sys.path.insert(1, './drive/')
sys.path.insert(1, './stat/')

#Import Other Files
import music
import classics
import misc
import drive
import stats
import utils

#Encoding for Playing Music
#import ctypes
#import ctypes.util
#opusLocation = ctypes.util.find_library('opus')
#a = discord.opus.load_opus(opusLocation)



#Intents for Discord Permissions
intents = discord.Intents.default()
intents.members = True



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=['s!', 'S!'], intents=intents, case_insensitive=True)
client = discord.Client()

bot.Stat = stats.Stats(bot)

#ID of the Admin
bot.adminId = 170301539020308481;
#ID for general text channel
bot.generalId = 159415088824975360;

#Time 5 Minutes Ago
bot.acridTime = datetime.datetime.now() - timedelta(minutes=5);
bot.bryceTime = bot.acridTime
bot.ballmerTime = bot.acridTime


#Prints When Bot has Connected
@bot.event
async def on_ready():
    print(bot.user.name + ' has connected to Discord!')



#Default if no command is found
@bot.event
async def on_command_error(ctx, error):
	if (isinstance(error, CommandNotFound)):
		await ctx.send("Command does not exist. That is really embarrassing " + ctx.author.display_name);
		return
	elif (isinstance(error, MissingRequiredArgument)):
		await ctx.send("Missing arguments buddy, not cool " + ctx.author.display_name);		

	file=open("log.txt", "a+")
	output = str(datetime.datetime.now()) + ": " + repr(error) + "\n"; 
	print(error)
	file.write(output)
	file.close()



"""

    General Helper Functions

"""

#Used for Checking the Time for Reginald
async def time_check():
    await bot.wait_until_ready()
    message_channel=bot.get_channel(bot.generalId)
    while True:
        day = datetime.date.today().weekday()
        now = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M')

        #now = "12:00"

        delta = (datetime.date.today() - bot.fixedDate)
        mod = delta.days % 14

        #print(now, day)
        #Use a fixed date to find the Wednesday that shows up once every other week
        if (now == bot.reginaldTime and mod == 11):
            await message_channel.send(file=discord.File('./media/jpg/reginald.jpg'))
            time = 3600
        elif (now == bot.reginaldTime and mod == 12):
            ran = random.choice(range(10))
            if ran == 0:
                await message_channel.send(file=discord.File('./media/jpg/reginaldBread.jpg'))
            time = 3600    
        #Mr Crab Friday at 5
        elif (now == "17:00" and day == 4):
            #print('crab')
            await message_channel.send("You guys made it to Friday, this ones on me:")
            await message_channel.send(file=discord.File('./media/jpg/crab_friday.mp4'))
        else:
            time = 50

        d = datetime.date.today().day
        m = datetime.date.today().month
        #Check for Birthdays
        if (now == "12:00"):
            bd = pandas.read_csv('./stat/birthdays.csv')
            for index, row in bd.iterrows():
                if (d == row['day'] and m == row['month']):

                     firstName = row['name'].split()[0]
                     lastName = row['name'].split()[1]

                     embed = discord.Embed(color = 0xeeeeee, title='Happy Birthday' + '!', url='https://itsyourbirthday.today/#' + firstName + '%20' + lastName)
                     embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/387360051482066944/813515560955674664/cake.jpg')
                     embed.add_field(name='Happy Birthday', value="! Strombot thinks it is your birthday and wishes you a happy birthday!!! Everyone wish, " + row['name'] + " a happy birthday!!!", inline=False) 
                     message = await ctx.send(embed = embed)
                     await message.add_reaction('🎂')
                     await message.add_reaction('🍨')

        await asyncio.sleep(time)


#Sends a message if someone tries to play something while it is already playing
async def playingMessage(ctx):
        response = ""
        
        if (bot.currentSong != "None"):
            response = "Song: \'" + bot.currentSong + "\' is currently playing. Either use s!stop or wait for it to finish."
        else:
            response = "A clip is currently playing already. Either use s!stop or wait for it to finish"

        await ctx.send(response)



#First Command Manager
@bot.event
async def on_message(ctx):
	if (ctx.author == bot.user):
		return

	user = ctx.author.id

	#Check if bot Command
	if (ctx.content[:2] == 's!' or ctx.content[:2] == 'S!'):
	#Store command in CSV file
		bot.Stat.commandUpdate(user, ctx.content[2:].split(' ')[0].lower())
		#print(ctx.content[2:].split(' ')[0])	



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

	if (url == 'bryce.gif' and getBryceTime()):
		bryce = './media/gif/bryce.gif'

		#Set the time last bryce was posted
		bot.bryceTime = datetime.datetime.now()
		await ctx.channel.send(file=discord.File(bryce));


	if (ctx.content == 'https://tenor.com/view/steve-ballmer-yes-microsoft-gif-4349581' and getBallmerTime()):

		#Set the time last ballmer was posted
		bot.ballmerTime = datetime.datetime.now()
		await ctx.channel.send('https://tenor.com/view/steve-ballmer-yes-microsoft-gif-4349581');


	#Go to Other Commands
	await bot.process_commands(ctx);


#Checks enough time has passed to post Acrid
def getAcridTime():
	now = datetime.datetime.now()
	if (bot.acridTime + timedelta(minutes=5) < now):
		return True
	else:
		return False 

#Checks enough time has passed to post Ballmer
def getBallmerTime():
	now = datetime.datetime.now()
	if (bot.ballmerTime + timedelta(minutes=5) < now):
		return True
	else:
		return False 

#Checks enough time has passed to post Bryce
def getBryceTime():
	now = datetime.datetime.now()
	if (bot.bryceTime + timedelta(minutes=5) < now):
		return True
	else:
		return False 


#Add commands from other files
bot.add_cog(music.Music(bot))
bot.add_cog(classics.EverydayClassics(bot))
bot.add_cog(misc.Misc(bot))
bot.add_cog(stats.Stats(bot))

bot.loop.create_task(time_check())

bot.remove_command("help")


#Custom Help Command
@bot.command(name='help')
async def help(ctx):
	embed = discord.Embed(color =  0xeeeeee)

	embed.add_field(name='Everyday Classics', value='--------------------', inline=False)
	
	embed.add_field(name='cancel', value='Use this to cancel someone!', inline=True)
	embed.add_field(name='dailyMeme', value='Posts the appropriate meme for the day', inline=True)
	embed.add_field(name='meme', value='Pull a classic meme from the archives', inline=True)
	embed.add_field(name='ratePost', value="Rates the latest post from 1-10", inline=True)
	embed.add_field(name='rateMeme', value='Rates your meme!', inline=True)
	embed.add_field(name='goodnight', value='Say goodnight to all your friends' + '\n\u200b', inline=True)

	
	embed.add_field(name='Music', value='--------------------', inline=False);
	
	embed.add_field(name='song', value='Play a random song from the playlist without memes', inline=True)
	embed.add_field(name='songMeme', value='Play a random song from the playlist with memes', inline=True)
	embed.add_field(name='playlist', value='Shuffles songs from the playlist without memes', inline=True)	
	embed.add_field(name='playlistMeme', value='Shuffles songs from the playlist with memes', inline=True)
	embed.add_field(name='playing', value='Tells what song is currently playing', inline=True)
	embed.add_field(name='skip', value='Skips currently playing song', inline=True)
	embed.add_field(name='stop', value='Stops currently playing songs or clips' + '\n\u200b', inline=True)


	embed.add_field(name='Miscellaneous', value='--------------------', inline=False)

	embed.add_field(name='7', value='Seven Dollars', inline=True)
	embed.add_field(name='bonk', value='Bonk', inline=True)
	embed.add_field(name='bruh', value='Bruh', inline=True)
	embed.add_field(name='bulborb', value='Posts a random bulborb', inline=True)
	embed.add_field(name='cat', value='Posts a random warrior cats image', inline=True)
	embed.add_field(name='coin', value='Flips a coin', inline=True)
	embed.add_field(name='dark', value='Plays a Dark Souls sound', inline = True)
	embed.add_field(name='patch', value='Explains what new features were added in the last update', inline=True)
	embed.add_field(name='stat', value="Displays statistics, works with s!stat @user too!", inline = True)
	embed.add_field(name='update', value='Checks the Google Drive for new memes and downloads them', inline=True)
	embed.add_field(name='yes', value='Posts Steve Ballmer funny sweat yes video', inline=True)	
	#embed.add_field(name='test', value="this is kinda weird [test](www.google.com)", inline=True)	
	await ctx.send(embed=embed)

#Run Bot
bot.run(TOKEN)


