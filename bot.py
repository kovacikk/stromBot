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
import classics
import misc
import stats
import timeCheck

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
bot.generalId = 159415088824975360 #387360051482066944

#Time 5 Minutes Ago
bot.acridTime = datetime.datetime.now() - timedelta(minutes=5);
bot.bryceTime = bot.acridTime
bot.ballmerTime = bot.acridTime

#Prints When Bot has Connected
@bot.event
async def on_ready():
    print(bot.user.name + ' has connected to Discord!')

#April Fools Bool
isFools = False
foolDay = 0
foolMonth = 0

#Wednesday Before Christmas
weevilChristmas = datetime.datetime.now().month

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
	
	#April Fools Message
	ran = random.choice(range(25))
	d = datetime.date.today().day
	m = datetime.date.today().month

	if ((ctx.content[:2] == 's!' or ctx.content[:2] == 'S!') and d == 1 and m == 4) and (ran < 5): #20% chance
		message = ''
		if ran == 0:
			message = 'No'
		elif ran == 1:
			await ctx.channel.send('https://tenor.com/view/sponge-bob-square-pants-idont-really-feel-like-it-sleeping-sleep-no-thanks-gif-5384362')
			return
		elif ran == 2:
			message = "..."
		elif ran == 3:
			message = "Sorry, I'm too busy reading Frog and Toad Are Friends by Arnold Lobel"
		elif ran == 4:
			await ctx.channel.send('https://tenor.com/view/no-idont-think-iwill-captain-america-old-capt-gif-17162888')
			return
		
		await ctx.channel.send(message)
		return


	#If Shane, Convert Secret s!kek
	if (ctx.content[:27] == 's!extremely_funny_and_based' or ctx.content[:27] == 'S!extremely_funny_and_based'):
		if (ctx.author.id == 256169976379998209):
			ctx.content = 's!kek'
		else:
			await ctx.channel.send('Sorry, only Shane gets based command privileges and you are NOT Shane')
			return

	#If Drew, Convert Secret s!meme walter white.gif
	if (ctx.content[:24] == 's!waltar_my_good_husband' or ctx.content[:24] == 'S!waltar_my_good_husband'):
		if (ctx.author.id == 159433180036726784):
			ctx.content = 's!meme walter white.gif'
		else:
			await ctx.channel.send('Uh oh, this command is reserved for true waltar whit fans only')
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
		await ctx.channel.send('https://tenor.com/view/steve-ballmer-yes-microsoft-gif-4349581')


	#Go to Other Commands
	await bot.process_commands(ctx)


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
bot.add_cog(classics.EverydayClassics(bot))
bot.add_cog(misc.Misc(bot))
bot.add_cog(stats.Stats(bot))
bot.add_cog(timeCheck.timeCheck(bot))



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
	embed.add_field(name='goodnight', value='Say goodnight to all your friends', inline=True)

	embed.add_field(name='kek', value='Displays a video in favor of another post', inline=True)
	embed.add_field(name='cringe', value='Displays a video in horror of another post' + '\n\u200b', inline=True)


	embed.add_field(name='Miscellaneous', value='--------------------', inline=False)

	embed.add_field(name='7', value='Seven Dollars', inline=True)
	embed.add_field(name='bonk', value='Bonk', inline=True)
	embed.add_field(name='bruh', value='Bruh', inline=True)
	embed.add_field(name='bulborb', value='Posts a random bulborb', inline=True)
	embed.add_field(name='cat', value='Posts a random warrior cats image', inline=True)
	embed.add_field(name='coin', value='Flips a coin', inline=True)
	embed.add_field(name='dark', value='Plays a Dark Souls sound', inline = True)
	embed.add_field(name='yes', value='Posts Steve Ballmer funny sweat yes video' + '\n\u200b', inline=True)	
	#embed.add_field(name='test', value="this is kinda weird [test](www.google.com)", inline=True)	

	
	embed.add_field(name='Bot Activities', value='--------------------', inline=False);

	embed.add_field(name='help', value='This page, displays Strombot commands', inline=True)
	embed.add_field(name='stat', value="Displays statistics, works with s!stat @user too!", inline = True)
	embed.add_field(name='patch', value='Explains what new features were added in the last update', inline=True)
	embed.add_field(name='update', value='Checks the Google Drive for new memes and downloads them', inline=True)

	message = await ctx.send(embed = embed)

	listEmbeds = []
	listEmbeds.append(embed)
	listEmbeds.append(musicEmbed)

	pointer = 0

	await message.add_reaction('⬅️')
	await message.add_reaction('➡️')

	while(True):
		reaction, user = await bot.wait_for('reaction_add', check=lambda reaction, user: reaction.emoji == '➡️' or reaction.emoji == '⬅️')
		if (user == ctx.author and reaction.message == message and reaction.emoji == '➡️'):
			pointer = pointer + 1
			if (pointer == len(listEmbeds)):
				pointer = 0

			await message.edit(embed = listEmbeds[pointer])
		elif(user == ctx.author and reaction.message == message and reaction.emoji == '⬅️'):
			pointer = pointer - 1
			if (pointer == -1):
				pointer = len(listEmbeds) - 1
			await message.edit(embed = listEmbeds[pointer])


	
	await ctx.send(embed=embed)

#Run Bot
bot.run(TOKEN)


