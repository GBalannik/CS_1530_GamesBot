import os
import discord
from discord.ext import commands
import random
from dotenv import load_dotenv

messageCount = dictionary()

def build_messageCounter():
	with open("database/messagecount.csv", 'r') as file:
		for line in file:
			(key, val) = line.split()
			messageCount[key] = int(val)

@client.event
async def on_message(message):
	if message.author in messageCount:
		messageCount[message.author] += 1
	else
		messageCount[message.author] = 1
	with open("database/messagecount.csv", 'w') as file:
		file.write(str(messageCount))

@client.command()
async def level(ctx, arg):
	if ctx.message.author.server_permissions.administrator and arg: ##admin version
		await ctx.send("{} has sent {} messages.".format(arg, messageCount[arg]))
	else: ##user version
		await ctx.send("You have sent {} messages.".format(messageCount[ctx.author]))
