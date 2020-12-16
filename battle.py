#battle.py - 
import os

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import random
import asyncio
import datetime
from datetime import timedelta
import traceback



#Battle Class
class Battle():
	def __init__(self, battlerOne, battlerTwo, channel):
		self.battlerOne = battlerOne
		self.battlerTwo = battlerTwo

		self.turn = 0
		self.stateOne = Battler(battlerOne)
		self.stateTwo = Battler(battlerTwo)

		self.channel = channel

	#Checks if both moves have been made, then calls makeMove()
	def checkMove(self):
		if (self.stateOne.move != 0 and self.stateTwo.move != 0):
			self.makeMove()

	#Performs Moves
	def makeMove(self):
		#P1 Attack
		if (self.stateOne.move == 1):
			#P2 Attack
			if (self.stateOne.move == 1):
				self.move11()			
			#P2 Defend
			elif (self.stateOne.move == 2):
				self.move12()
			#P2 Charge
			elif (self.stateOne.move == 3):
				self.move13()
			#P2 Talk
			elif (self.stateOne.move == 4):
				self.move14()	
		#P1 Defend
		elif (self.stateOne.move == 2):
			#P2 Attack
			if (self.stateOne.move == 1):
				self.move21()	
			#P2 Defend
			elif (self.stateOne.move == 2):
				self.move22()
			#P2 Charge
			elif (self.stateOne.move == 3):
				self.move23()
			#P2 Talk
			elif (self.stateOne.move == 4):
				self.move24()	

		#P1 Charge
		elif (self.stateOne.move == 3):
			#P2 Attack
			if (self.stateOne.move == 1):
				self.move31()	
			#P2 Defend
			elif (self.stateOne.move == 2):
				self.move32()
			#P2 Charge
			elif (self.stateOne.move == 3):
				self.move33()
			#P2 Talk
			elif (self.stateOne.move == 4):
				self.move34()	

		#P1 Talk
		elif (self.stateOne.move == 4):
			#P2 Attack
			if (self.stateOne.move == 1):
				self.move41()	
			#P2 Defend
			elif (self.stateOne.move == 2):
				self.move42()
			#P2 Charge
			elif (self.stateOne.move == 3):
				self.move43()
			#P2 Talk
			elif (self.stateOne.move == 4):
				self.move44()	
		
		self.checkWin()


	#Returns the User if they Won, otherwise None
	def checkWin(self):
		if (stateOne.health <= 0):
			return stateTwo.user
		elif (stateOne.health <= 0):
			return stateOne.user
		else:
			return None

	#P1 Attacks P2 Attacks
	def move11():
		return	
	
	#P1 Attacks P2 Defends
	def move12():
		return

	#P1 Attacks P2 Charges
	def move13():
		return
	
	#P1 Attacks P2 Talks
	def move14():
		return
	
	#P1 Defends P2 Attacks
	def move21():
		return
	
	#P1 Defends P2 Defends
	def move22():
		return

	#P1 Defends P2 Charges
	def move23():
		return
	
	#P1 Defends P2 Talks
	def move24():
		return
	
	#P1 Charges P2 Attacks
	def move31():
		return
	
	#P1 Charges P2 Defends
	def move32():
		return

	#P1 Charges P2 Charges
	def move33():
		return
	
	#P1 Charges P2 Talks
	def move34():
		return
	
	#P1 Talks P2 Attacks
	def move41():
		return
	
	#P1 Talks P2 Defends
	def move42():
		return

	#P1 Talks P2 Charges
	def move43():
		return
	
	#P1 Talks P2 Talks
	def move44():
		return
	


#Class for Users
class Battler():
	def __init__(self, battler):
		self.user = battler
		self.health = 50
		self.attack = 20
		self.defense = 10
		self.isCharged = False
		self.talkCount = 0
		self.move = 0
