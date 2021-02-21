# in utils.py

import discord
from discord.ext import commands
import asyncio

async def reactList(ctx, bot, query, matching):
	matching.sort()

	embed = discord.Embed(color = 0xeeeeee)

	args = ""
	for arg in query:
		if not (arg == '-l'):
			args = arg + " "

	listNumber = 0
	if len(matching) >= 10:
		listNumber = 10
	else:
		listNumber = len(matching)

	oldListNumber = 0


	isFirst = True
	result = '**-----------------------**\n'
	for match in matching[:listNumber]:
		if (len(result) + len(match + '\n')) > 1024:
			if (isFirst):
				embed.add_field(name="Listing Results for: " + args, value=result, inline=False)
				isFirst = False
			else:
				embed.add_field(name="------", value=result, inline=False)
			result = ''
		
		result = result + match + '\n'
	if (isFirst):
		embed.add_field(name="Listing Results for: " + args, value=result, inline=False)
	else:
		embed.add_field(name="------", value=result, inline=False)
	embed.add_field(name="-----------------------", value='Viewing ' + str(oldListNumber + 1) + "-" + str(listNumber) + ' of ' + str(len(matching)), inline=False)


	message = await ctx.send(embed = embed)
	await message.add_reaction('⬅️')
	await message.add_reaction('➡️')

	oldListNumber = 0

	loopBool = True
	while (loopBool):
		reaction, user = await bot.wait_for('reaction_add', check=lambda reaction, user: reaction.emoji == '➡️' or reaction.emoji == '⬅️')
	#print(reaction, user)
	#Right
		if (user == ctx.author and reaction.message == message and reaction.emoji == '➡️'):
			#print('here')
			if len(matching) - listNumber >= 10:
				oldListNumber = listNumber
				listNumber = listNumber + 10
			elif len(matching) - listNumber == 0:
				pass
			else:
				oldListNumber = listNumber
				listNumber = len(matching)

			embed = discord.Embed(color = 0xeeeeee)
					
			isFirst = True
			result = '**-----------------------**\n'
			for match in matching[oldListNumber:listNumber]:
				if (len(result) + len(match + '\n')) > 1024:
					if (isFirst):
						embed.add_field(name="Listing Results for: " + args, value=result, inline=False)
						isFirst = False
					else:
						embed.add_field(name="------", value=result, inline=False)
					result = ''
				
				result = result + match + '\n'
			if (isFirst):
				embed.add_field(name="Listing Results for: " + args, value=result, inline=False)
			else:
				embed.add_field(name="------", value=result, inline=False)
			embed.add_field(name="-----------------------", value='Viewing ' + str(oldListNumber + 1) + "-" + str(listNumber) + ' of ' + str(len(matching)), inline=False)

			await message.edit(embed = embed)
		elif(user == ctx.author and reaction.message == message and reaction.emoji == '⬅️'):
			if listNumber > 10 and (listNumber % 10) != 0:
				extra = listNumber % 10	
				oldListNumber = oldListNumber - 10
				listNumber = listNumber - extra
			if listNumber > 10:
				oldListNumber = oldListNumber - 10
				listNumber = listNumber - 10
			else:
				oldListNumber = oldListNumber
				listNumber = listNumber

			embed = discord.Embed(color = 0xeeeeee)

			isFirst = True
			result = '**-----------------------**\n'
			for match in matching[oldListNumber:listNumber]:
				if (len(result) + len(match + '\n')) > 1024:
					if (isFirst):
						embed.add_field(name="Listing Results for: " + args, value=result, inline=False)
						isFirst = False
					else:
						embed.add_field(name="------", value=result, inline=False)
					result = ''
				
				result = result + match + '\n'
			if (isFirst):
				embed.add_field(name="Listing Results for: " + args, value=result, inline=False)
			else:
				embed.add_field(name="------", value=result, inline=False)
			embed.add_field(name="-----------------------", value='Viewing ' + str(oldListNumber + 1) + "-" + str(listNumber) + ' of ' + str(len(matching)), inline=False)


			await message.edit(embed = embed)


	return
