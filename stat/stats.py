#stat.py

import os
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import random
import asyncio
import pandas as pd

#Stat Class
class Stats(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.userColumns = ['id', 'total', 'averagerate', 'sumrate', '7', 'bonk', 'bulborb', 'cancel', 'cat', 'coin', 'dailymeme', 'dark', 'goodnight', 'meme', 'patch', 'playing', 'playlist', 'playlistmeme', 'ratememe', 'ratepost', 'skip', 'song', 'songmeme', 'stat', 'stop', 'update', 'yes', 'fail', 'kek', 'cringe']
		self.memeColumns = ['meme', 'count']
		self.catColumns = ['cat', 'count']
		self.bulborbColumns = ['bulborb', 'count']
		self.songColumns = ['song', 'count']
		self.cancelColumns = ['id', 'count']

	#Get Server Statistics
	@commands.command(name = 'stat', help = 'Get Server Statistics')
	async def stat(self, ctx, *query):
		#Get Stats of Bot
		if (len(query) == 0):
			embed = discord.Embed(color = 0xeeeeee)
			embed.add_field(name='Commands', value='--------------------', inline=False)

			userData = pd.read_csv('./stat/userData.csv')	

			active = ''

			for i in range(5):
				#print(i)	
				activeUser = userData['total'].nlargest(6).index[i+1]
				activeUsername = ctx.message.guild.get_member(userData.loc[activeUser, 'id'])

				if (activeUsername == None):
					activeUsername = str(userData.loc[activeUser,'id'])
				else:
					activeUsername = activeUsername.display_name

			
				activeUserTotal = userData.loc[activeUser, 'total']

				active = active + activeUsername + '   -->   *' + str(activeUserTotal) + '*\n'  

		
			#print('out')
	
			embed.add_field(name='Total Commands:', value=str(userData.loc[userData['id'] == -1, 'total'].values[0]), inline=True)
			embed.add_field(name='Most Active Strom-Users:', value=active, inline=True)

			total = {}
			for column in userData:
				if not (column == 'id' or column == 'total' or column =='averagerate' or column == 'sumrate'):
					total[column] = (userData.loc[0,column])

			total = sorted(total.items(), key=lambda item: item[1])
			top = ""
			bottom = ""
			for i in range(5):
				top = top + total[len(total)-i-1][0] + "   -->   *" + str(total[len(total)-i-1][1]) + "*\n"
				bottom = bottom + total[i][0] + "   -->   *" + str(total[i][1]) + "*\n"

			embed.add_field(name='\u200b', value='\u200b', inline=True)

			embed.add_field(name='Top Five Commands:', value=top, inline=True)
			embed.add_field(name='Bottom Five Commands:', value=bottom, inline=True)

			embed.add_field(name='\u200b', value='\u200b', inline=True)

			embed.add_field(name='\u200b\nMost Frequent', value='---------------------', inline=False)


			top = self.topFive(ctx, './stat/memeData.csv', 'meme',0,5)

			embed.add_field(name='Meme:', value=top, inline=True)
		
			top = self.topFive(ctx, './stat/catData.csv', 'cat',0,5)

			embed.add_field(name='Cat:', value=top, inline=True)
			
			embed.add_field(name='\u200b', value='\u200b', inline=True)			

			top = self.topFive(ctx, './stat/bulborbData.csv', 'bulborb',0,5)

			embed.add_field(name='Bulborb:', value=top, inline=True)

			top = self.topFive(ctx, './stat/cancelData.csv', 'id',0,5)
		
			embed.add_field(name='Cancel Victim:', value=top, inline=True)


			embed.add_field(name='\u200b', value='\u200b', inline=True)

			top = self.topFive(ctx, './stat/songData.csv', 'song',0,5)

			embed.add_field(name='Song:', value=top, inline=True)

		
			message = await ctx.send(embed = embed)
			hubStat = embed

			#print('yo')	

			listEmbeds = []
			listEmbeds.append(hubStat)
			listEmbeds.append(self.getEmbeds(ctx,'user'))
			listEmbeds.append(self.getEmbeds(ctx,'command'))
			listEmbeds.append(self.getEmbeds(ctx,'meme'))
			listEmbeds.append(self.getEmbeds(ctx,'cat'))
			listEmbeds.append(self.getEmbeds(ctx,'bulborb'))
			listEmbeds.append(self.getEmbeds(ctx,'cancel'))
			listEmbeds.append(self.getEmbeds(ctx,'song'))

			pointer = 0

			#print(pointer)
			await message.add_reaction('⬅️')
			await message.add_reaction('➡️')

			while(True):
				reaction, user = await self.bot.wait_for('reaction_add', check=lambda reaction, user: reaction.emoji == '➡️' or reaction.emoji == '⬅️')
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

		#Gets Stats of User
		else:
			embed = self.getEmbeds(ctx, query[0])
			#Stat Page
			if (embed != None):
				await ctx.send(embed = embed)
			#User Stat Page
			else:
				userId = query[0]
				#print(userId)
				#Remove Everything but the id
				replace = "<>!@"
				for char in replace:
					userId = userId.replace(char, "")

				try:
					userId = int(userId)
				except:
					await ctx.send('Invalid User please try again')
					return

				userData = pd.read_csv('./stat/userData.csv')
			
				user = userData.loc[userData['id'] == userId]
				if user.empty:
					await ctx.send('User not found in database')
				else:
					embed = discord.Embed(color = 0xeeeeee)
				
					activeUsername = ctx.message.guild.get_member(userId)

					if (activeUsername == None):
						activeUsername = str(userId)
					else:
						activeUsername = activeUsername.display_name



					embed.add_field(name=activeUsername, value='--------------------', inline=False)
				
					field = ""
				
					total = {}
					for column in userData:
						if not (column == 'id' or column == 'total' or column =='averagerate' or column == 'sumrate'):
							total[column] = (userData.loc[userData['id'] == userId ,column].values[0])

					total = sorted(total.items(), key=lambda item: item[1])


					for i in range(len(total)):
						field = field + total[len(total)-i-1][0] + "   -->   *" + str(total[len(total)-i-1][1]) + '*\n'

					embed.add_field(name='total = *' + str(userData.loc[userData['id'] == userId, 'total'].values[0]) + '*\n', value=field, inline=False)
					await ctx.send(embed = embed)
			
	#Helper function for Getting Top 5
	def topFive(self, ctx, path, index, lindex, rindex): 
		top = ""

		data = pd.read_csv(path)
		top5 = {}
		if not data.empty:
			for row in data.iterrows():
				top5[row[1][index]] = int(row[1]['count'])

		top5 = sorted(top5.items(), key=lambda item: item[1])

		for i in range(rindex):
			if (top5[len(top5)-i-1][0] == 'none') and (i >= lindex):
				pass
			elif (index == 'id'):
				activeUsername = ctx.message.guild.get_member(int(top5[len(top5)-i-1][0]))
				if (activeUsername == None):
					activeUsername = str(int(top5[len(top5)-i-1][0]))
				else:
					activeUsername = activeUsername.display_name
				top = top + activeUsername + "   -->   *" + str(top5[len(top5)-i-1][1]) + "*\n"

			else:
				top = top + top5[len(top5)-i-1][0] + "   -->   *" + str(top5[len(top5)-i-1][1]) + "*\n"
		return top

	#Helper function for list of data
	def listData(self, ctx, path, index, lindex, rindex):
		top = ""

		data = pd.read_csv(path)
		top5 = {}
		if not data.empty:
			for row in data.iterrows():
				top5[row[1][index]] = int(row[1]['count'])

		top5 = sorted(top5.items(), key=lambda item: item[1])

		dataList = []
		for i in range(rindex):
			if (top5[len(top5)-i-1][0] == 'none') and (i >= lindex):
				pass
			elif (index == 'id'):
				activeUsername = ctx.message.guild.get_member(int(top5[len(top5)-i-1][0]))
				if (activeUsername == None):
					activeUsername = str(int(top5[len(top5)-i-1][0]))
				else:
					activeUsername = activeUsername.display_name
				
				dataList.append((activeUsername,str(top5[len(top5)-i-1][1]))) 	
				#top = top + activeUsername + "   -->   *" + str(top5[len(top5)-i-1][1]) + "*\n"

			else:
				dataList.append((top5[len(top5)-i-1][0],str(top5[len(top5)-i-1][1])))
				#top = top + top5[len(top5)-i-1][0] + "   -->   *" + str(top5[len(top5)-i-1][1]) + "*\n"
		return dataList

	#Gets Embeds for Stat Pages
	def getEmbeds(self, ctx, page):
		if (page == 'user'):
			userData = pd.read_csv('./stat/userData.csv')
			userStat = discord.Embed(color = 0xeeeeee)	
			
			active = ''
			for i in range(30):
				#print(i)
				#print(i, len(userData['total'].nlargest(41).index) - 1)
				if (not (i >= len(userData['total'].nlargest(41).index) -1 )): 
					activeUser = userData['total'].nlargest(41).index[i+1]
					activeUsername = ctx.message.guild.get_member(userData.loc[activeUser, 'id'])
				
					if (activeUsername == None):
						activeUsername = str(userData.loc[activeUser,'id'])
					else:
						activeUsername = activeUsername.display_name
					activeUserTotal = userData.loc[activeUser, 'total']

					active = active + activeUsername + '   -->   *' + str(activeUserTotal) + '*\n'
			
			userStat.add_field(name='Top 30 Users', value='-------------', inline=False)
			userStat.add_field(name='Users', value=active, inline=False)

			return userStat
		elif(page == 'command'):
			userData = pd.read_csv('./stat/userData.csv')
		
			commandStat = discord.Embed(color = 0xeeeeee)
			commandStat.add_field(name='Top 20 and Bottom 20 Commands', value='----------------', inline=False)

			total = {}
			for column in userData:
				if not (column == 'id' or column == 'total' or column =='averagerate' or column == 'sumrate'):
					total[column] = (userData.loc[0,column])
			total = sorted(total.items(), key=lambda item: item[1])


			top = ''
			bottom = ''
			for i in range(20):
				top = top + str(i+1) + ": " +  total[len(total)-i-1][0] + "   -->   *" + str(total[len(total)-i-1][1]) + "*\n"			
				bottom = bottom + str(i+1) + ": " +  total[i][0] + "   -->   *" + str(total[i][1]) + "*\n"

			commandStat.add_field(name='Top Commands', value=top)
			commandStat.add_field(name='Bottom Commands', value=bottom)

			return commandStat
		elif(page == 'meme'):
			memeStat = discord.Embed(color = 0xeeeeee)
			#memeStat.add_field(name='Most Used Memes', value='----------------', inline=False)
			memeList = self.listData(ctx, './stat/memeData.csv', 'meme', 0, 30)
			counter = 0
			value = ''
			for name, count in memeList:
				counter = counter + 1
				newEntry = str(counter) + ': ' + name + "   -->   *" + count + "*\n"
				if (len(value) + len(newEntry) > 1024) or ((counter > 2) and ((counter-1)%10 == 0)) :
					if (counter <= 11):
						memeStat.add_field(name='Top 30 Memes\n-------------------', value=value,inline=False)
					else:
						memeStat.add_field(name='-----', value=value,inline=False)

					value = ''

				value = value + newEntry
	
			memeStat.add_field(name='-----', value=value,inline=False)

			return memeStat
		elif(page == 'cat'):
			catStat = discord.Embed(color = 0xeeeeee)
			#catStat.add_field(name='Most Used Cats', value='---------------', inline=False)
			catList = self.listData(ctx, './stat/catData.csv', 'cat', 0, 30)
			counter = 0
			value = ''
			for name, count in catList:
				counter = counter + 1
				newEntry = str(counter) + ': ' + name + "   -->   *" + count + "*\n"	
				if (len(value) + len(newEntry) > 1024) or ((counter > 2) and ((counter-1)%10 == 0)):
					if (counter <= 11):
						catStat.add_field(name='Top 30 Cats\n-------------------', value=value,inline=False)
					else:
						catStat.add_field(name='-----', value=value,inline=False)

					value = ''

				value = value + newEntry
	
			catStat.add_field(name='-----', value=value,inline=False)

			return catStat
		elif(page == 'bulborb'):
			bulborbStat = discord.Embed(color = 0xeeeeee)
			#bulborbStat.add_field(name='Most Used Bulborb', value='---------------', inline=False)
			bulborbList = self.listData(ctx, './stat/bulborbData.csv', 'bulborb', 0, 30)
			counter = 0
			value = ''
			for name, count in bulborbList:
				counter = counter + 1
				newEntry = str(counter) + ': ' + name + "   -->   *" + count + "*\n"	
				if (len(value) + len(newEntry) > 1024) or ((counter > 2) and ((counter-1)%10 == 0)):
					if (counter <= 11):
						bulborbStat.add_field(name='Top 30 Bulborbs\n-------------------', value=value,inline=False)
					else:
						bulborbStat.add_field(name='-----', value=value,inline=False)	
					value = ''

				value = value + newEntry
	
			bulborbStat.add_field(name='-----', value=value,inline=False)

			return bulborbStat
		elif(page == 'cancel'):
			cancelStat = discord.Embed(color = 0xeeeeee)
			#cancelStat.add_field(name='Most Used Cancel Victims', value='---------------', inline=False)
			cancelList = self.listData(ctx, './stat/cancelData.csv', 'id', 0, 30)
			counter = 0
			value = ''
			for name, count in cancelList:
				counter = counter + 1
				newEntry = str(counter) + ': ' + name + "   -->   *" + count + "*\n"	
				if (len(value) + len(newEntry) > 1024) or ((counter > 2) and ((counter-1)%10 == 0)):
					if (counter <= 11):
						cancelStat.add_field(name='Top 30 Victims\n-------------------', value=value,inline=False)
					else:
						cancelStat.add_field(name='-----', value=value,inline=False)
					value = ''

				value = value + newEntry
	
			cancelStat.add_field(name='-----', value=value,inline=False)
		
			return cancelStat
		elif(page == 'song'):
			songStat = discord.Embed(color = 0xeeeeee)
			#songStat.add_field(name='Most Played Songs', value='---------------', inline=False)
			songList = self.listData(ctx, './stat/songData.csv', 'song', 0, 30)
			counter = 0
			value = ''
			for name, count in songList:
				counter = counter + 1
				newEntry = str(counter) + ': ' + name + "   -->   *" + count + "*\n"	
				if (len(value) + len(newEntry) > 1024) or ((counter > 2) and ((counter-1)%10 == 0)):
					if (counter <= 11):
						songStat.add_field(name='Top 30 Songs\n-------------------', value=value,inline=False)
					else:
						songStat.add_field(name='-----', value=value,inline=False)
					value = ''

				value = value + newEntry
	
			songStat.add_field(name='-----', value=value,inline=False)

			return songStat	
		else:
			return None
	
	#Updates User and Total Commands Data
	def commandUpdate(self, userId, command):
		df = pd.read_csv('./stat/userData.csv')
		user = df[df['id'].isin([userId])]

		for col in df.columns:
			if col == 'fail':
				command = 'fail'
			elif col == command:
				break
					

		if user.empty:
			data = self.newUserRow(userId, command)
			newRow = pd.DataFrame(data, columns=self.userColumns)
			df = df.append(newRow)

		else:
			df.loc[df['id'] == userId, command] = df.loc[df['id'] == userId, command] + 1
			df.loc[df['id'] == userId, 'total'] = df.loc[df['id'] == userId, 'total'] + 1

		df.loc[df['id'] == -1, command] = df.loc[df['id'] == -1, command] + 1
		df.loc[df['id'] == -1, 'total'] = df.loc[df['id'] == -1, 'total'] + 1
			 
		df.to_csv('./stat/userData.csv', mode='w', header=True, index=False)		
			
	#Generate New User Row
	def newUserRow(self, userId, command):
		row = [[userId, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

		for i in range(len(self.userColumns)):
			if self.userColumns[i] == command:
				row[0][i] = 1

		return row				


	#Updates Memes Database
	def memeUpdate(self, memeName):
		df = pd.read_csv('./stat/memeData.csv')
		isNew = df[df['meme'].isin([memeName])]
		
		#New Meme
		if isNew.empty:
			data = [[memeName, 1]]
			newRow = pd.DataFrame(data, columns=self.memeColumns)
			df = df.append(newRow)
		#Existing Meme	
		else:	
			df.loc[df['meme'] == memeName, 'count'] = df.loc[df['meme'] == memeName, 'count'] + 1

		df.to_csv('./stat/memeData.csv', header=True, index=False)

	
	#Updates Cat Database
	def catUpdate(self, catName):
		df = pd.read_csv('./stat/catData.csv')
		isNew = df[df['cat'].isin([catName])]

		#New Cat
		if isNew.empty:
			data = [[catName, 1]]
			newRow = pd.DataFrame(data, columns=self.catColumns)
			df = df.append(newRow)
		#Existing Cat
		else:
			df.loc[df['cat'] == catName, 'count'] = df.loc[df['cat'] == catName, 'count'] + 1

		df.to_csv('./stat/catData.csv', header=True, index=False)

	#Updates Bulborb Database
	def bulborbUpdate(self, bulborbName):
		df = pd.read_csv('./stat/bulborbData.csv')
		isNew = df[df['bulborb'].isin([bulborbName])]

		#New Bulborb
		if isNew.empty:
			data = [[bulborbName, 1]]
			newRow = pd.DataFrame(data, columns=self.bulborbColumns)
			df = df.append(newRow)
		#Existing Bulborb
		else:
			df.loc[df['bulborb'] == bulborbName, 'count'] = df.loc[df['bulborb'] == bulborbName, 'count'] + 1

		df.to_csv('./stat/bulborbData.csv', header=True, index=False)


	#Updates Song Database
	def songUpdate(self, songName):
		df = pd.read_csv('./stat/songData.csv')
		isNew = df[df['song'].isin([songName])]

		#New Song
		if isNew.empty:
			data = [[songName, 1]]
			newRow = pd.DataFrame(data, columns=self.songColumns)
			df = df.append(newRow)
		#Existing Song
		else:
			df.loc[df['song'] == songName, 'count'] = df.loc[df['song'] == songName, 'count'] + 1

		df.to_csv('./stat/songData.csv', header=True, index=False)


	
	#Updates Cancel Database
	def cancelUpdate(self, cancelName):
		df = pd.read_csv('./stat/cancelData.csv')
		isNew = df[df['id'].isin([cancelName])]

		print(cancelName)

		#New Cancel
		if isNew.empty:
			data = [[cancelName, 1]]
			newRow = pd.DataFrame(data, columns=self.cancelColumns)
			df = df.append(newRow)
		#Existing Cancel
		else:
			df.loc[df['id'] == cancelName, 'count'] = df.loc[df['id'] == cancelName, 'count'] + 1

		df.to_csv('./stat/cancelData.csv', header=True, index=False)












