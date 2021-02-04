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
		self.userColumns = ['id', 'total', 'averagerate', 'sumrate', '7', 'bonk', 'bulborb', 'cancel', 'cat', 'coin', 'dailymeme', 'dark', 'goodnight', 'meme', 'patch', 'playing', 'playlist', 'playlistmeme', 'ratememe', 'ratepost', 'skip', 'song', 'songmeme', 'stat', 'stop', 'update', 'yes', 'fail']
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

			for i in range(3):
			
				activeUser = userData['total'].nlargest(4).index[i+1]
				activeUsername = ctx.message.guild.get_member(userData.loc[activeUser, 'id'])

				if (activeUsername == None):
					activeUsername = str(userData.loc[activeUser,'id'])
				else:
					activeUsername = activeUsername.display_name

			
				activeUserTotal = userData.loc[activeUser, 'total']

				active = active + activeUsername + '   -->   *' + str(activeUserTotal) + '*\n'  

			
			#print(userData.loc[userData['id'] == -1, 'total']) 
			#print(activeUsername, activeUserTotal)

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


			top = self.topFive(ctx, './stat/memeData.csv', 'meme')

			embed.add_field(name='Meme:', value=top, inline=True)
		
			top = self.topFive(ctx, './stat/catData.csv', 'cat')

			embed.add_field(name='Cat:', value=top, inline=True)
			
			embed.add_field(name='\u200b', value='\u200b', inline=True)			

			top = self.topFive(ctx, './stat/bulborbData.csv', 'bulborb')

			embed.add_field(name='Bulborb:', value=top, inline=True)

			top = self.topFive(ctx, './stat/cancelData.csv', 'id')
		
			embed.add_field(name='Cancel Victim:', value=top, inline=True)


			embed.add_field(name='\u200b', value='\u200b', inline=True)

			top = self.topFive(ctx, './stat/songData.csv', 'song')

			embed.add_field(name='Song:', value=top, inline=True)

		
			await ctx.send(embed = embed)

		#Gets Stats of User
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
	def topFive(self, ctx, path, index): 
		top = ""

		data = pd.read_csv(path)
		top5 = {}
		if not data.empty:
			for row in data.iterrows():
				top5[row[1][index]] = int(row[1]['count'])

		top5 = sorted(top5.items(), key=lambda item: item[1])

		for i in range(5):
			if (top5[len(top5)-i-1][0] == 'none'):
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
		row = [[userId, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

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












